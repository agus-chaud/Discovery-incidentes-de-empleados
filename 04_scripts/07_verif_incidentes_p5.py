# -*- coding: utf-8 -*-
"""Verificacion cruzada de incidentes (2 fuentes) + cierre de P5 rotacion."""
import pandas as pd, numpy as np
from pathlib import Path
D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
T = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\tablas_soporte")
pd.set_option("display.width", 230)

panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
evt = pd.read_parquet(D / "eventos_limpio.parquet")
cap = pd.read_parquet(D / "capacitaciones_limpio.parquet")
pa = panel[panel.activo].copy()

print("### DISCREPANCIA ENTRE FUENTES DE INCIDENTES")
inc = evt[evt.tipo_evento == "incidente_seguridad"].copy()
inc["mes"] = inc.fecha_evento.values.astype("datetime64[M]")
a = inc.groupby("mes").size().rename("eventos_rrhh")
b = panel.groupby("mes_snapshot").incidentes_seguridad_count.sum().rename("panel_count")
cmp = pd.concat([a, b], axis=1).fillna(0).astype(int)
cmp["dif"] = cmp.panel_count - cmp.eventos_rrhh
print(cmp.to_string())
print(f"\n  TOTAL eventos_rrhh: {len(inc)} | TOTAL panel (suma columna): {int(panel.incidentes_seguridad_count.sum())}")
print(f"  Empleados-mes con count>1: {int((panel.incidentes_seguridad_count > 1).sum())} | max valor: {panel.incidentes_seguridad_count.max()}")
# cruce a nivel empleado-mes
inc["k"] = inc.empleado_id.astype(str) + "|" + inc.mes.astype(str)
panel["k"] = panel.empleado_id.astype(str) + "|" + panel.mes_snapshot.astype(str)
con_evento = set(inc.k)
con_count = set(panel.loc[panel.incidentes_seguridad_count > 0, "k"])
print(f"  Empleado-mes con evento registrado: {len(con_evento)}")
print(f"  Empleado-mes con count>0 en panel : {len(con_count)}")
print(f"  Coinciden ambas fuentes           : {len(con_evento & con_count)}")
print(f"  Solo en eventos_rrhh              : {len(con_evento - con_count)}")
print(f"  Solo en panel                     : {len(con_count - con_evento)}")

print("\n### RECALCULO DE SEGURIDAD USANDO SOLO eventos_rrhh (fuente auditable)")
inc2 = inc.merge(panel[["k", "turno_trabajo", "antiguedad_meses", "horas_extra", "area"]], on="k", how="left")
expo_t = pa.groupby("turno_trabajo").size().rename("emp_meses")
i_t = inc2.groupby("turno_trabajo").size().rename("incidentes")
dias_t = inc2.groupby("turno_trabajo").dias_perdidos.sum().rename("dias_perdidos")
tt = pd.concat([expo_t, i_t, dias_t], axis=1).fillna(0)
tt["tasa_x1000"] = (tt.incidentes / tt.emp_meses * 1000).round(1)
tt = tt.sort_values("tasa_x1000", ascending=False)
print("\n  Por TURNO (turno del empleado en ese mes):")
print(tt.to_string())
tt.to_csv(T / "P4_incidentes_por_turno.csv", encoding="utf-8-sig")  # hallazgo mas robusto del proyecto: ahora tiene tabla de soporte (DEC-021)

bins = [-1, 6, 12, 24, 60, 120, 999]
labs = ["0-6m", "6-12m", "1-2a", "2-5a", "5-10a", "10a+"]
pa["ba"] = pd.cut(pa.antiguedad_meses, bins, labels=labs)
inc2["ba"] = pd.cut(inc2.antiguedad_meses, bins, labels=labs)
expo_a = pa.groupby("ba", observed=True).size().rename("emp_meses")
i_a = inc2.groupby("ba", observed=True).size().rename("incidentes")
ba = pd.concat([expo_a, i_a], axis=1).fillna(0)
ba["tasa_x1000"] = (ba.incidentes / ba.emp_meses * 1000).round(1)
ba["train_h_mes"] = pa.groupby("ba", observed=True).horas_training_mes.mean().round(2)
print("\n  Por ANTIGUEDAD:")
print(ba.to_string())
ba.to_csv(T / "P4_incidentes_antiguedad_fuente_eventos.csv", encoding="utf-8-sig")

print("\n  Por DECIL de horas extra:")
pa["dec"] = pd.qcut(pa.horas_extra, 10, labels=False, duplicates="drop")
inc2["dec"] = pd.cut(inc2.horas_extra, pd.qcut(pa.horas_extra, 10, retbins=True, duplicates="drop")[1],
                     labels=False, include_lowest=True)
ed = pa.groupby("dec").size().rename("emp_meses")
idd = inc2.groupby("dec").size().rename("incidentes")
dd = pd.concat([ed, idd], axis=1).fillna(0)
dd["he_prom"] = pa.groupby("dec").horas_extra.mean().round(1)
dd["tasa_x1000"] = (dd.incidentes / dd.emp_meses * 1000).round(1)
print(dd.to_string())

print("\n  Antiguedad de los accidentados (meses):")
print(inc2.antiguedad_meses.describe().round(1).to_string())
print(f"\n  Incidentes en los primeros 6 meses: {int((inc2.antiguedad_meses <= 6).sum())} de {len(inc2)} ({(inc2.antiguedad_meses<=6).mean()*100:.0f}%)")
print(f"  Incidentes en turno Noche         : {int((inc2.turno_trabajo=='Noche').sum())} de {len(inc2)} ({(inc2.turno_trabajo=='Noche').mean()*100:.0f}%)")

print("\n### GRAVEDAD: donde estan los dias perdidos y el costo")
g = inc.groupby("severidad").agg(n=("evento_id", "size"), dias=("dias_perdidos", "sum"),
                                 costo=("costo_estimado", "sum"), dias_prom=("dias_perdidos", "mean")).round(1)
print(g.to_string())
print("\n  Por subtipo:")
print(inc.groupby("subtipo_evento").agg(n=("evento_id", "size"), dias=("dias_perdidos", "sum"),
      costo=("costo_estimado", "sum")).sort_values("dias", ascending=False).to_string())

print("\n" + "=" * 100)
print("P5 (cierre) - PERFIL DE SALIDA Y COSTO")
print("=" * 100)
sal = ult[ult.salio].copy()
print("\n--- Perfil: se van vs se quedan ---")
pf = ult.groupby("salio").agg(
    n=("empleado_id", "size"), edad=("edad", "mean"), antig=("antiguedad_anios", "mean"),
    salario=("salario_base_mensual", "mean"), perf=("perf_prom", "mean"), he=("he_prom", "mean"),
    ausencias=("ausencias_total", "mean"), training=("horas_training_total", "mean"),
    top_perf=("es_top_performer", "mean"), meses_sin_aumento=("meses_desde_ultimo_aumento", "mean"),
).round(2)
print(pf.to_string())

print("\n--- Se van los BUENOS? ---")
ult["pb"] = pd.cut(ult.perf_prom, [0, 2.5, 3.5, 4.5, 5.1], labels=["Bajo", "Medio", "Alto", "Top"])
pbt = ult.groupby("pb", observed=True).agg(n=("empleado_id", "size"), salidas=("salio", "sum"))
pbt["pct_rotacion"] = (pbt.salidas / pbt.n * 100).round(1)
print(pbt.to_string())
print(f"\n  Rotacion TOP PERFORMERS: {ult[ult.es_top_performer].salio.mean()*100:.1f}% (n={int(ult.es_top_performer.sum())})")
print(f"  Rotacion resto         : {ult[~ult.es_top_performer].salio.mean()*100:.1f}% (n={int((~ult.es_top_performer).sum())})")

print("\n--- Renuncias VOLUNTARIAS: perfil especifico (lo controlable) ---")
vol = ult[ult.motivo_salida == "Renuncia voluntaria"]
print(f"  n={len(vol)} | antig media={vol.antiguedad_anios.mean():.1f}a | perf={vol.perf_prom.mean():.2f} | "
      f"HE={vol.he_prom.mean():.1f}h | meses sin aumento={vol.meses_desde_ultimo_aumento.mean():.1f} | top_perf={vol.es_top_performer.mean()*100:.0f}%")
qd = ult[~ult.salio]
print(f"  vs se quedan: antig={qd.antiguedad_anios.mean():.1f}a | perf={qd.perf_prom.mean():.2f} | "
      f"HE={qd.he_prom.mean():.1f}h | meses sin aumento={qd.meses_desde_ultimo_aumento.mean():.1f} | top_perf={qd.es_top_performer.mean()*100:.0f}%")
print("\n  Renuncias voluntarias por area:")
rv = ult.groupby("area").agg(total=("empleado_id", "size"))
rv["renuncias"] = ult[ult.motivo_salida == "Renuncia voluntaria"].groupby("area").size()
rv = rv.fillna(0)
rv["pct"] = (rv.renuncias / rv.total * 100).round(1)
print(rv.sort_values("pct", ascending=False).to_string())

print("\n--- COSTO de la rotacion ---")
cont = evt[evt.tipo_evento == "contratacion"]
onb = evt[evt.tipo_evento == "onboarding"]
c_rep = cont.costo_estimado.mean() + onb.costo_estimado.mean()
print(f"  Contrataciones: {len(cont)} | costo medio contratacion ${cont.costo_estimado.mean():,.0f} + onboarding ${onb.costo_estimado.mean():,.0f}")
print(f"  Costo directo de reemplazo por persona: ${c_rep:,.0f}")
print(f"  Time to fill: media {cont.dias_time_to_fill.mean():.0f} d | mediana {cont.dias_time_to_fill.median():.0f} d | p90 {cont.dias_time_to_fill.quantile(0.9):.0f} d")
sal_prom = ult[ult.salio].salario_base_mensual.mean()
print(f"  Salario medio del que sale: ${sal_prom:,.0f}/mes")
print(f"  Costo vacancia (time-to-fill x salario/30): ${cont.dias_time_to_fill.mean()/30*sal_prom:,.0f}")
print(f"  COSTO TOTAL estimado por salida: ${c_rep + cont.dias_time_to_fill.mean()/30*sal_prom:,.0f}")
print(f"  Salidas anualizadas: {len(sal)/17*12:.0f}/anio  ->  COSTO ANUAL ROTACION: ${(c_rep + cont.dias_time_to_fill.mean()/30*sal_prom)*len(sal)/17*12:,.0f}")

print("\n### ROI DE CAPACITACION (bonus)")
print("  Categorias:", dict(cap.categoria_training.value_counts()))
print(f"  Costo total training periodo: ${cap.costo_training.sum():,.0f} | anualizado ${cap.costo_training.sum()/17*12:,.0f}")
print(f"  Tasa de NO completado: {(~cap.completado).mean()*100:.1f}% ({int((~cap.completado).sum())} de {len(cap)})")
print("\n  Efectividad por modalidad:")
print(cap.groupby("modalidad").agg(n=("training_id", "size"), rating=("rating_efectividad", "mean"),
      nota=("calificacion_examen", "mean"), completado=("completado", "mean"),
      costo_h=("costo_training", "mean")).round(2).to_string())
print("\n  Cobertura de training en SEGURIDAD por area (horas por empleado):")
seg = cap[cap.categoria_training == "Seguridad"].groupby("area_empleado").agg(
    n_trainings=("training_id", "size"), horas=("duracion_horas", "sum"))
dot = ult.groupby("area").empleado_id.size().rename("empleados")
sg = pd.concat([seg, dot], axis=1).fillna(0)
sg["horas_por_empleado"] = (sg.horas / sg.empleados).round(1)
inc_area = inc.groupby("area_empleado").size().rename("incidentes")
sg = sg.join(inc_area).fillna(0)
sg["tasa_inc_x100emp"] = (sg.incidentes / sg.empleados * 100).round(1)
print(sg.sort_values("tasa_inc_x100emp", ascending=False).to_string())
sg.to_csv(T / "P6_training_seguridad_vs_incidentes.csv", encoding="utf-8-sig")
