# -*- coding: utf-8 -*-
"""P3 Horas extra | P4 Seguridad | P5 Rotacion"""
import pandas as pd, numpy as np
from pathlib import Path
D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
T = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\tablas_soporte")
pd.set_option("display.width", 230)
pd.set_option("display.max_columns", 60)

panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
evt = pd.read_parquet(D / "eventos_limpio.parquet")
act = ult[~ult.salio].copy()
pa = panel[panel.activo].copy()

print("=" * 100)
print("P3 - HORAS EXTRA: CONCENTRACION Y COSTO")
print("=" * 100)
tot_he = pa.costo_horas_extra.sum()
tot_base = pa.salario_base_mensual.sum()
print(f"\nCosto TOTAL horas extra (17 meses): ${tot_he:,.0f} | sobre nomina base: {tot_he/tot_base*100:.1f}%")
print(f"Costo HE anualizado (12m): ${tot_he/17*12:,.0f}")

print("\n--- Pareto: concentracion del costo de HE por empleado ---")
he_emp = pa.groupby("empleado_id").costo_horas_extra.sum().sort_values(ascending=False)
cum = he_emp.cumsum() / he_emp.sum()
for p in [0.05, 0.10, 0.20, 0.30]:
    k = int(len(he_emp) * p)
    print(f"  Top {p*100:>4.0f}% empleados ({k:3d} pers.) concentran {cum.iloc[k-1]*100:4.1f}% del costo de HE")

print("\n--- HE por AREA (promedio mensual por empleado) ---")
ar = pa.groupby("area").agg(
    emp=("empleado_id", "nunique"),
    he_prom_mes=("horas_extra", "mean"),
    he_p90=("horas_extra", lambda s: s.quantile(0.9)),
    pct_he_nomina=("pct_he_sobre_base", "mean"),
    costo_he=("costo_horas_extra", "sum"),
).round(2)
ar["costo_he_anual"] = (ar.costo_he / 17 * 12).round(0)
print(ar.sort_values("he_prom_mes", ascending=False).to_string())
ar.to_csv(T / "P3_horas_extra_por_area.csv", encoding="utf-8-sig")

print("\n--- HE por TURNO ---")
print(pa.groupby("turno_trabajo").agg(
    emp=("empleado_id", "nunique"),
    he_prom=("horas_extra", "mean"),
    pct_nomina=("pct_he_sobre_base", "mean"),
    ausencias=("dias_ausente", "mean"),
).round(2).sort_values("he_prom", ascending=False).to_string())

print("\n--- Es estructural o pico puntual? HE promedio por mes ---")
ev = pa.groupby("mes_snapshot").agg(
    he_prom=("horas_extra", "mean"),
    activos=("empleado_id", "nunique"),
    costo=("costo_horas_extra", "sum"),
).round(2)
print(ev.to_string())

print("\n--- SOBRECARGA CRONICA: empleados con HE alta sostenida ---")
umbral = pa.horas_extra.quantile(0.80)
pa["he_alta"] = pa.horas_extra >= umbral
cron = pa.groupby("empleado_id").agg(meses=("he_alta", "size"), meses_he_alta=("he_alta", "sum"))
cron["pct_meses_sobrecargado"] = (cron.meses_he_alta / cron.meses * 100).round(0)
cr = cron[(cron.pct_meses_sobrecargado >= 70) & (cron.meses >= 6)]
print(f"  Umbral HE alta (p80) = {umbral:.1f} h/mes")
print(f"  Empleados sobrecargados CRONICOS (>=70% de sus meses sobre p80): {len(cr)}")
det = act.merge(cr, on="empleado_id", how="inner")
if len(det):
    print(det.groupby(["area", "turno_trabajo"]).agg(
        n=("empleado_id", "size"),
        he=("he_prom", "mean"),
        ausencias=("ausencias_total", "mean"),
        incid=("incidentes_total", "sum"),
    ).round(1).sort_values("n", ascending=False).to_string())
    det.to_csv(T / "P3_sobrecargados_cronicos.csv", index=False, encoding="utf-8-sig")

print("\n" + "=" * 100)
print("P4 - SEGURIDAD: QUE PREDICE LOS ACCIDENTES")
print("=" * 100)
inc = evt[evt.tipo_evento == "incidente_seguridad"].copy()
print(f"\nIncidentes registrados en eventos: {len(inc)} | periodo {inc.fecha_evento.min().date()} a {inc.fecha_evento.max().date()}")
print(f"Dias perdidos totales: {inc.dias_perdidos.sum():.0f} | Costo estimado: ${inc.costo_estimado.sum():,.0f}")
print("\n  Severidad:", dict(inc.severidad.value_counts()))
print("  Por area:", dict(inc.area_empleado.value_counts()))
print("  Por turno:", dict(inc.turno_evento.value_counts()))
print("  Parte del cuerpo:", dict(inc.parte_cuerpo_afectada.value_counts()))
print("  Subtipo:", dict(inc.subtipo_evento.value_counts()))

print("\n--- TASA de incidentes por area (normalizada por dotacion-mes) ---")
expo = pa.groupby("area").empleado_id.size().rename("empleado_meses")
ic = pa.groupby("area").incidentes_seguridad_count.sum().rename("incidentes")
tasa = pd.concat([expo, ic], axis=1)
tasa["tasa_x1000_emp_mes"] = (tasa.incidentes / tasa.empleado_meses * 1000).round(1)
tasa["he_prom"] = pa.groupby("area").horas_extra.mean().round(1)
print(tasa.sort_values("tasa_x1000_emp_mes", ascending=False).to_string())
tasa.to_csv(T / "P4_tasa_incidentes_por_area.csv", encoding="utf-8-sig")

print("\n--- TASA por TURNO ---")
tt = pa.groupby("turno_trabajo").agg(
    emp_meses=("empleado_id", "size"),
    incid=("incidentes_seguridad_count", "sum"),
    he=("horas_extra", "mean"),
)
tt["tasa_x1000"] = (tt.incid / tt.emp_meses * 1000).round(1)
print(tt.round(1).sort_values("tasa_x1000", ascending=False).to_string())

print("\n--- Perfil accidentado vs no accidentado (nivel persona) ---")
ult["tuvo_incidente"] = ult.incidentes_total > 0
comp = ult.groupby("tuvo_incidente").agg(
    n=("empleado_id", "size"), edad=("edad", "mean"),
    antig_anios=("antiguedad_anios", "mean"), he_prom=("he_prom", "mean"),
    training_h=("horas_training_total", "mean"), perf=("perf_prom", "mean"),
    ausencias=("ausencias_total", "mean"),
    # solo produccion: el desperdicio no existe fuera de Estampado/Ensamble/Pintura (DEC-010)
    scrap_solo_produccion=("scrap_prom_produccion", "mean"),
    n_con_scrap=("scrap_prom_produccion", lambda s: int(s.notna().sum())),
).round(2)
print(comp.to_string())

print("\n--- Incidentes por decil de HORAS EXTRA (hipotesis de Martina, testeada) ---")
pa["dec_he"] = pd.qcut(pa.horas_extra, 10, labels=False, duplicates="drop")
dh = pa.groupby("dec_he").agg(
    emp_meses=("empleado_id", "size"), he_prom=("horas_extra", "mean"),
    incid=("incidentes_seguridad_count", "sum"), ausencias=("dias_ausente", "mean"),
)
dh["tasa_x1000"] = (dh.incid / dh.emp_meses * 1000).round(1)
print(dh.round(2).to_string())

print("\n--- Incidentes por ANTIGUEDAD (curva de experiencia) ---")
pa["banda_antig"] = pd.cut(pa.antiguedad_meses, [-1, 6, 12, 24, 60, 120, 999],
                           labels=["0-6m", "6-12m", "1-2a", "2-5a", "5-10a", "10a+"])
ba = pa.groupby("banda_antig", observed=True).agg(
    emp_meses=("empleado_id", "size"), incid=("incidentes_seguridad_count", "sum"),
    he=("horas_extra", "mean"), train=("horas_training_mes", "mean"),
)
ba["tasa_x1000"] = (ba.incid / ba.emp_meses * 1000).round(1)
print(ba.round(2).to_string())
ba.to_csv(T / "P4_incidentes_por_antiguedad.csv", encoding="utf-8-sig")

print("\n" + "=" * 100)
print("P5 - ROTACION: QUIEN SE VA, POR QUE Y CUANTO CUESTA")
print("=" * 100)
sal = ult[ult.salio].copy()
hc_prom = pa.groupby("mes_snapshot").empleado_id.nunique().mean()
print(f"\nSalidas en el periodo: {len(sal)} sobre {len(ult)} empleados observados")
print(f"Headcount promedio: {hc_prom:.0f} | Rotacion anualizada: {len(sal)/17*12/hc_prom*100:.1f}% anual")
print("\n  Motivo:", dict(sal.motivo_salida.value_counts()))

print("\n--- Rotacion por AREA ---")
ra = ult.groupby("area").agg(total=("empleado_id", "size"), salidas=("salio", "sum"))
ra["pct_rotacion"] = (ra.salidas / ra.total * 100).round(1)
print(ra.sort_values("pct_rotacion", ascending=False).to_string())
ra.to_csv(T / "P5_rotacion_por_area.csv", encoding="utf-8-sig")

print("\n--- Cuando se van? Antiguedad al momento de la salida ---")
print(sal.antiguedad_anios.describe().round(1).to_string())
print("\n  Distribucion:", dict(pd.cut(sal.antiguedad_anios, [-1, 1, 2, 5, 10, 99],
      labels=["<1a", "1-2a", "2-5a", "5-10a", "10a+"]).value_counts().sort_index()))

print("\n--- Perfil: los que se van vs los que se quedan ---")
pf = ult.groupby("salio").agg(
    n=("empleado_id", "size"), edad=("edad", "mean"), antig=("antiguedad_anios", "mean"),
    salario=("salario_base_mensual", "mean"), perf=("perf_prom", "mean"), he=("he_prom", "mean"),
    ausencias=("ausencias_total", "mean"), training=("horas_training_total", "mean"),
    top_perf=("es_top_performer", "mean"), meses_sin_aumento=("meses_desde_ultimo_aumento", "mean"),
).round(2)
print(pf.to_string())

print("\n--- ALERTA: se van los BUENOS? ---")
ult["perf_band"] = pd.cut(ult.perf_prom, [0, 2.5, 3.5, 4.5, 5.1],
                          labels=["Bajo (<2.5)", "Medio (2.5-3.5)", "Alto (3.5-4.5)", "Top (4.5+)"])
pb = ult.groupby("perf_band", observed=True).agg(n=("empleado_id", "size"), salidas=("salio", "sum"))
pb["pct_rotacion"] = (pb.salidas / pb.n * 100).round(1)
print(pb.to_string())
print(f"\n  Rotacion TOP PERFORMERS: {ult[ult.es_top_performer].salio.mean()*100:.1f}% | resto: {ult[~ult.es_top_performer].salio.mean()*100:.1f}%")

print("\n--- COSTO de la rotacion ---")
cont = evt[evt.tipo_evento == "contratacion"]
print(f"  Contrataciones: {len(cont)} | costo medio registrado: ${cont.costo_estimado.mean():,.0f}")
print(f"  Costo total contratacion+onboarding: ${evt[evt.tipo_evento.isin(['contratacion','onboarding'])].costo_estimado.sum():,.0f}")
print(f"  Time to fill promedio: {cont.dias_time_to_fill.mean():.0f} dias | p90: {cont.dias_time_to_fill.quantile(0.9):.0f} dias")
