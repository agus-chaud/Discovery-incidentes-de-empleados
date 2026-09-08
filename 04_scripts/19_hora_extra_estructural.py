# -*- coding: utf-8 -*-
"""Hora extra: estructural (dotacion corta permanente) vs demanda (sube con la produccion).

Mejora 2 aplicada: se verifica primero que contiene `horas_trabajadas`, se usa una
base de horas estandar limpia como denominador, y la traduccion a dotacion se
reporta como PROPORCION (sin supuestos) y como RANGO de FTE (con el supuesto de
rampa escrito al lado), nunca como un numero de cabezas puntual.
"""
import pandas as pd, numpy as np
from pathlib import Path

D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
T = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\tablas_soporte")
panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
pa = panel[panel.activo].copy()
MESES = pa.mes_snapshot.nunique()
AREAS_PROD = ["Estampado", "Ensamble", "Pintura"]        # unicas con unidades_producidas propias
RAMPA = 0.70   # supuesto EXPLICITO: un ingresante rinde ~70% durante el primer trimestre (N2 no medido)

print("=" * 96)
print("HORA EXTRA: ESTRUCTURAL vs DEMANDA   |   meses:", pa.mes_snapshot.min().date(), "->", pa.mes_snapshot.max().date())
print("=" * 96)

# ---------------------------------------------------------------------------
print("\n### 0. Que contiene `horas_trabajadas`? (define el denominador de la mejora 2)")
# a) nivel: comparar contra el turno teorico (duracion_turno_horas * dias habiles ~21)
teorico = (pa.duracion_turno_horas * 21).median()
htrab_med = pa.horas_trabajadas.median()
# b) la HE, esta DENTRO de horas_trabajadas o es aparte? -> correlacion intra-persona
#    (si estuviera dentro, en los meses de mas HE subiria tambien horas_trabajadas)
def _corr_ht_he(gp):
    if len(gp) < 3 or gp.horas_trabajadas.std() == 0 or gp.horas_extra.std() == 0:
        return np.nan
    return gp.horas_trabajadas.corr(gp.horas_extra)
with np.errstate(all="ignore"):
    corr = pa.groupby("empleado_id")[["horas_trabajadas", "horas_extra"]].apply(_corr_ht_he).dropna()
frac_pos = (corr > 0.3).mean()
print(f"  turno teorico (duracion_turno x 21 dias) mediana : {teorico:6.1f} h/mes")
print(f"  horas_trabajadas mediana                          : {htrab_med:6.1f} h/mes")
print(f"  horas_extra mediana                               : {pa.horas_extra.median():6.1f} h/mes")
print(f"  correlacion intra-persona horas_trabajadas ~ horas_extra: mediana {corr.median():.2f} | "
      f"{frac_pos*100:.0f}% de las personas > 0.3")
# la correlacion es ~0 -> la HE NO esta dentro de horas_trabajadas, es aditiva.
# Base estandar = horas_trabajadas tal cual (jornada normal observada, ~165 h/mes, coherente
# con el turno teorico de 168). No se le resta la HE. Denominador limpio para la mejora 2.
pa["horas_estandar"] = pa.horas_trabajadas
print(f"  -> HE aditiva (corr ~ 0). Base estandar = horas_trabajadas tal cual "
      f"(~{htrab_med:.0f} h/mes, coherente con el turno teorico de {teorico:.0f}).")

# ---------------------------------------------------------------------------
print("\n### 1. Nivel y planitud de la hora extra por area (dotacion activa)")
g = (pa.groupby(["area", "mes_snapshot"])
     .agg(headcount=("empleado_id", "nunique"),
          he_total=("horas_extra", "sum"),
          he_emp=("horas_extra", "mean"),
          std_total=("horas_estandar", "sum"),
          costo_he=("costo_horas_extra", "sum"),
          unidades=("unidades_producidas", "sum"))
     .reset_index())
plant_unid = g.groupby("mes_snapshot").unidades.sum().rename("plant_unid")
g = g.merge(plant_unid, on="mes_snapshot")
g["unid_emp"] = g.unidades / g.headcount


def r2_slope(y, x):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 5 or np.std(x) == 0:
        return np.nan, np.nan
    b1, b0 = np.polyfit(x, y, 1)
    yhat = b0 + b1 * x
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - np.sum((y - yhat) ** 2) / ss_tot if ss_tot > 0 else np.nan
    return r2, b1


rows = []
for area, sub in g.groupby("area"):
    if sub.headcount.mean() < 8:
        continue
    sub = sub.sort_values("mes_snapshot")
    he = sub.he_emp
    driver = sub.unid_emp if area in AREAS_PROD else sub.plant_unid
    r2, b1 = r2_slope(he, driver)
    rows.append(dict(
        area=area, headcount=round(sub.headcount.mean()),
        he_emp_prom=round(he.mean(), 1), he_min=round(he.min(), 1), he_max=round(he.max(), 1),
        CV=round(he.std() / he.mean(), 2) if he.mean() else np.nan,
        R2_vs_volumen=round(r2, 2) if np.isfinite(r2) else np.nan,
        # etiqueta HEURISTICA (no testeada; ver mejora 1 pendiente). Solo orienta la lectura.
        patron_aprox=("sigue-al-volumen" if (np.isfinite(r2) and r2 >= 0.5 and b1 > 0)
                      else "carga-creciente" if (np.isfinite(r2) and r2 >= 0.5 and b1 <= 0)
                      else "plano" if (he.std() / he.mean() if he.mean() else 1) < 0.10
                      else "intermedio"),
        costo_he_anual_MM=round(sub.costo_he.sum() / MESES * 12 / 1e6, 1),
    ))
r = pd.DataFrame(rows).sort_values("he_emp_prom", ascending=False)
print(r.to_string(index=False))
print("  Nota: 'patron_aprox' usa umbrales heuristicos (R2>=0.5, CV<0.10), NO un test. "
      "Ponerle intervalo de confianza a la pendiente queda pendiente (mejora 1).")

# ---------------------------------------------------------------------------
print("\n### 2. Traduccion a dotacion  (MEJORA 2: proporcion sin supuestos + rango de FTE)")
areas_ok = r.area.tolist()
gg = g[g.area.isin(areas_ok)]
tot_he = gg.he_total.sum()
tot_std = gg.std_total.sum()
prop = tot_he / tot_std * 100
print(f"  Horas extra como % de las horas-plantel ESTANDAR (sin ningun supuesto): {prop:.1f}%")
print(f"    -> por cada 100 h de jornada normal se trabajan {prop:.1f} h extra.\n")

# rango de FTE-equivalente por area: piso (a rendimiento pleno) y techo (con rampa)
per = []
for area, sub in gg.groupby("area"):
    he_mes = sub.he_total.mean()
    std_pers_mes = (sub.std_total / sub.headcount).mean()      # horas estandar por persona-mes en el area
    fte_piso = he_mes / std_pers_mes
    fte_techo = fte_piso / RAMPA                               # cubrir esas horas con ingresantes que rinden 70%
    per.append({"area": area, "headcount": round(sub.headcount.mean()),
                "he_pct_plantel": round(sub.he_total.sum() / sub.std_total.sum() * 100, 1),
                "FTE_equiv_piso": round(fte_piso, 1), "FTE_equiv_techo": round(fte_techo, 1),
                "costo_he_anual_MM": round(sub.costo_he.sum() / MESES * 12 / 1e6, 1)})
fte = pd.DataFrame(per).sort_values("costo_he_anual_MM", ascending=False)
print(fte.to_string(index=False))
piso, techo = fte.FTE_equiv_piso.sum(), fte.FTE_equiv_techo.sum()
piso_p = fte.loc[fte.area.isin(AREAS_PROD), "FTE_equiv_piso"].sum()
techo_p = fte.loc[fte.area.isin(AREAS_PROD), "FTE_equiv_techo"].sum()
print(f"\n  FTE-equivalente cubierto con hora extra (areas con dotacion >= 8):")
print(f"    total planta : {piso:.0f} a {techo:.0f} personas   (piso = rendimiento pleno; "
      f"techo = ingresante al {RAMPA*100:.0f}% el primer trimestre)")
print(f"    solo produccion (Estampado/Ensamble/Pintura): {piso_p:.0f} a {techo_p:.0f} personas")
print(f"  Costo HE anual de esas areas: ${fte.costo_he_anual_MM.sum():.0f}MM  |  "
      f"solo produccion: ${fte.loc[fte.area.isin(AREAS_PROD),'costo_he_anual_MM'].sum():.0f}MM")
print("  CAVEAT: el techo depende del supuesto de rampa (RAMPA=0.70); N2 (meses hasta "
      "rendimiento pleno) no esta medido. El numero firme es el % de horas-plantel.")

# ---------------------------------------------------------------------------
print("\n### 3. Meses-area con pico de hora extra (deteccion generica, sin hardcodear nombres)")
g2 = g[g.area.isin(areas_ok)].copy()
base_area = g2.groupby("area").he_emp.transform("median")
g2["exceso_vs_mediana"] = g2.he_emp - base_area
g2["exceso_pct"] = g2.exceso_vs_mediana / base_area * 100
picos = g2[g2.exceso_pct >= 25].sort_values("exceso_pct", ascending=False)
if len(picos):
    print(picos.assign(mes=picos.mes_snapshot.dt.strftime("%Y-%m"))[
        ["area", "mes", "headcount", "he_emp", "exceso_pct"]].round(1).to_string(index=False))
    print("  -> revisar con el area que paso esos meses (proyecto puntual, falla mayor, ausencias en cadena).")
else:
    print("  Sin meses-area por encima del +25% de su mediana: la hora extra es pareja en todo el panel.")

# ---------------------------------------------------------------------------
out = T / "P3b_hora_extra_estructural.csv"
fte.to_csv(out, index=False, encoding="utf-8-sig")
picos.assign(mes=picos.mes_snapshot.dt.strftime("%Y-%m"))[
    ["area", "mes", "headcount", "he_emp", "exceso_pct"]].to_csv(
    T / "P3b_hora_extra_picos.csv", index=False, encoding="utf-8-sig")
print(f"\nGuardado: {out.name}, P3b_hora_extra_picos.csv")
