# -*- coding: utf-8 -*-
"""P1 Riesgo de sucesion/jubilacion | P2 Genero: dotacion, techo de cristal, brecha salarial"""
import pandas as pd, numpy as np
from pathlib import Path
D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
T = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\tablas_soporte")
pd.set_option("display.width",220); pd.set_option("display.max_columns",60)

ult = pd.read_parquet(D/"empleados_nivel_persona.parquet")
act = ult[~ult.salio].copy()          # 562 activos al ultimo snapshot
print(f"Universo de analisis: {len(act)} empleados ACTIVOS a {act.mes_snapshot.max().date()}\n")

print("="*100); print("P1 — RIESGO DE SUCESION / JUBILACION"); print("="*100)
print(f"\nJubilaciones proximas (sobre {len(act)} activos):")
for k,lab in [(12,"<= 12 meses"),(24,"<= 24 meses"),(36,"<= 36 meses"),(60,"<= 60 meses")]:
    m = act.meses_hasta_jubilacion <= k
    print(f"  {lab:14s}: {m.sum():3d} empleados ({m.mean()*100:4.1f}%) | de ellos criticos: {int((m & act.es_posicion_critica).sum())}")

crit = act[act.es_posicion_critica]
print(f"\nPosiciones criticas activas: {len(crit)} ({len(crit)/len(act)*100:.1f}% de la dotacion)")

print("\n--- Criticos que se jubilan en <=12m, por area y puesto ---")
r12 = crit[crit.meses_hasta_jubilacion<=12]
if len(r12):
    t = (r12.groupby(["area","puesto"])
           .agg(n=("empleado_id","size"), edad_prom=("edad","mean"),
                antig_anios=("antiguedad_anios","mean"),
                meses_rest=("meses_hasta_jubilacion","min"),
                salario=("salario_base_mensual","mean"))
           .sort_values("n",ascending=False).round(1))
    print(t.to_string())
print(f"\n  TOTAL criticos en riesgo <=12m: {len(r12)}")

print("\n--- Cobertura: para cada puesto critico en riesgo, cuanta gente hay en el mismo puesto? ---")
pool = act.groupby(["area","puesto"]).empleado_id.size().rename("dotacion_puesto")
rr = (crit[crit.meses_hasta_jubilacion<=24]
      .groupby(["area","puesto"]).agg(en_riesgo_24m=("empleado_id","size"),
                                      antig_prom=("antiguedad_anios","mean")).round(1))
rr = rr.join(pool)
rr["pct_puesto_en_riesgo"] = (rr.en_riesgo_24m/rr.dotacion_puesto*100).round(1)
rr["sucesor_potencial"] = rr.dotacion_puesto - rr.en_riesgo_24m
print(rr.sort_values("pct_puesto_en_riesgo",ascending=False).to_string())
rr.to_csv(T/"P1_riesgo_sucesion_por_puesto.csv", encoding="utf-8-sig")

print("\n--- Concentracion de conocimiento: puestos criticos con UNA sola persona (single point of failure) ---")
spof = act.groupby(["area","puesto"]).agg(n=("empleado_id","size"),
        criticos=("es_posicion_critica","sum"),
        jub24=("jubila_24m","sum"), edad=("edad","mean"), antig=("antiguedad_anios","mean")).round(1)
sp = spof[(spof.n==1)&(spof.criticos==1)]
print(f"  Puestos criticos unipersonales: {len(sp)}")
print(sp.sort_values("edad",ascending=False).head(20).to_string())
spof.to_csv(T/"P1_dotacion_por_puesto.csv", encoding="utf-8-sig")

print("\n"+"="*100); print("P2 — GENERO: DOTACION, TECHO DE CRISTAL Y BRECHA SALARIAL"); print("="*100)
print(f"\nDotacion global: {dict(act.genero.value_counts())} | %F = {(act.genero=='F').mean()*100:.1f}%")

print("\n--- Mix de genero por AREA ---")
g = pd.crosstab(act.area, act.genero)
g["total"]=g.sum(1); g["pct_F"]=(g.get("F",0)/g.total*100).round(1)
print(g.sort_values("pct_F").to_string())
g.to_csv(T/"P2_genero_por_area.csv", encoding="utf-8-sig")

print("\n--- Techo de cristal: mix por NIVEL JERARQUICO ---")
n = pd.crosstab(act.nivel_jerarquico, act.genero)
n["total"]=n.sum(1); n["pct_F"]=(n.get("F",0)/n.total*100).round(1)
print(n.to_string())
n.to_csv(T/"P2_genero_por_nivel.csv", encoding="utf-8-sig")

print("\n--- Brecha salarial CRUDA vs AJUSTADA (mismo nivel + area + antiguedad) ---")
b = act.groupby("genero").salario_base_mensual.agg(["size","mean","median"]).round(0)
print(b.to_string())
cruda = (1 - act[act.genero=="F"].salario_base_mensual.mean()/act[act.genero=="M"].salario_base_mensual.mean())*100
print(f"\n  Brecha CRUDA (media): {cruda:.1f}%  <- NO controla por puesto/nivel, no usar sola")

print("\n  Brecha DENTRO de cada nivel jerarquico (like-for-like parcial):")
for lv, sub in act.groupby("nivel_jerarquico"):
    f, m = sub[sub.genero=="F"], sub[sub.genero=="M"]
    if len(f)>=5 and len(m)>=5:
        gap = (1 - f.salario_base_mensual.mean()/m.salario_base_mensual.mean())*100
        print(f"    Nivel {lv}: nF={len(f):3d} nM={len(m):3d} | brecha={gap:+5.1f}%  (F={f.salario_base_mensual.mean():,.0f} M={m.salario_base_mensual.mean():,.0f})")

print("\n  Brecha por AREA (solo areas con >=10 de cada genero):")
rows=[]
for ar, sub in act.groupby("area"):
    f, m = sub[sub.genero=="F"], sub[sub.genero=="M"]
    if len(f)>=10 and len(m)>=10:
        gap=(1-f.salario_base_mensual.mean()/m.salario_base_mensual.mean())*100
        rows.append({"area":ar,"nF":len(f),"nM":len(m),"brecha_pct":round(gap,1)})
print(pd.DataFrame(rows).sort_values("brecha_pct",ascending=False).to_string(index=False))

print("\n--- Regresion OLS log(salario) ~ genero + nivel + area + antiguedad + edad + performance ---")
X = act[["genero","nivel_jerarquico","area","antiguedad_meses","edad","rating_performance","salario_base_mensual"]].dropna()
Xd = pd.get_dummies(X, columns=["genero","area"], drop_first=True).astype(float)
y = np.log(Xd.pop("salario_base_mensual"))
Xd.insert(0,"const",1.0)
beta, *_ = np.linalg.lstsq(Xd.values, y.values, rcond=None)
resid = y.values - Xd.values@beta
dof = len(y)-Xd.shape[1]
se = np.sqrt(np.diag(np.linalg.pinv(Xd.values.T@Xd.values))*(resid@resid/dof))
co = pd.DataFrame({"coef":beta,"se":se}, index=Xd.columns)
co["t"]=(co.coef/co.se).round(2)
co["efecto_pct"]=((np.exp(co.coef)-1)*100).round(2)
print(co.loc[[c for c in co.index if "genero" in c or c in ("nivel_jerarquico","antiguedad_meses","rating_performance","edad")]].to_string())
print(f"  R2 = {1-resid.var()/y.values.var():.3f} | n = {len(y)}")
