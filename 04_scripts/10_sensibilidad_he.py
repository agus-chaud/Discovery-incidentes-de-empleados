# -*- coding: utf-8 -*-
"""Sensibilidad HE vs dotacion + vinculo HE/ausentismo/rotacion (el caso real)."""
import pandas as pd, numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "06_resultados" / "Discovery" / "datos_transformados"
T = ROOT / "06_resultados" / "Discovery" / "tablas_soporte"
T.mkdir(parents=True, exist_ok=True)
panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
pa = panel[panel.activo].copy()
MESES = pa.mes_snapshot.nunique()

print("### SENSIBILIDAD: cuando conviene contratar en vez de pagar horas extra?")
recargo = (pa.costo_horas_extra.sum() / pa.horas_extra.sum()) / (pa[pa.categoria_collar == "Blue"].salario_base_mensual.mean() / pa.horas_trabajadas.mean())
print(f"  Recargo efectivo observado en los datos: {recargo:.3f}x")
print("  Regla: conviene contratar solo si (1 + cargas sociales) < recargo\n")
print("  cargas   factor    veredicto")
for c in [0.15, 0.25, 0.30, 0.3383, 0.40, 0.45, 0.50]:
    v = "CONVIENE contratar" if (1 + c) < recargo else "CONVIENE la hora extra"
    print(f"   {c*100:5.1f}%   {1+c:.3f}    {v}")
print(f"\n  --> PUNTO DE EQUILIBRIO: cargas sociales = {(recargo-1)*100:.1f}%")
print("  En Argentina las cargas patronales reales rondan 24-27% (Ley 27.541) mas ART,")
print("  aguinaldo y vacaciones -> el costo cargado supera holgadamente el 34%.")
print("  CONCLUSION: con estos datos, sustituir HE por dotacion NO genera ahorro.")

print("\n### ENTONCES CUAL ES EL CASO REAL DE LAS HORAS EXTRA? -> fatiga y ausentismo")
umbral = pa.horas_extra.quantile(0.80)
pa["he_alta"] = pa.horas_extra >= umbral
cron = pa.groupby("empleado_id").agg(meses=("he_alta", "size"), alt=("he_alta", "sum"))
cron["pct"] = cron.alt / cron.meses * 100
cron["cronico"] = (cron.pct >= 70) & (cron.meses >= 6)
u = ult.merge(cron[["cronico"]], on="empleado_id", how="left")
u["cronico"] = u.cronico.fillna(False).astype(bool)

print(f"\n  Sobrecargados cronicos: {int(u.cronico.sum())} de {len(u)} empleados ({u.cronico.mean()*100:.1f}%)")
comp = u.groupby("cronico").agg(
    n=("empleado_id", "size"), he=("he_prom", "mean"),
    ausencias_mes=("ausencias_total", lambda s: s.mean()),
    lic_medica=("lic_medica_total", "mean"), rotacion=("salio", "mean"),
    perf=("perf_prom", "mean"), incidentes=("incidentes_total", "mean"),
    meses_obs=("meses_observados", "mean")).round(2)
# normalizar ausencias por meses observados (evita sesgo de exposicion)
comp["ausencias_x_mes"] = (comp.ausencias_mes / comp.meses_obs).round(3)
comp["lic_x_mes"] = (comp.lic_medica / comp.meses_obs).round(3)
print(comp[["n", "he", "meses_obs", "ausencias_x_mes", "lic_x_mes", "rotacion", "perf", "incidentes"]].to_string())

# test de diferencia normalizado a nivel empleado-mes (evita el sesgo de exposicion)
print("\n  A nivel EMPLEADO-MES (sin sesgo de exposicion):")
pa2 = pa.merge(cron[["cronico"]], on="empleado_id", how="left")
pa2["cronico"] = pa2.cronico.fillna(False).astype(bool)
em = pa2.groupby("cronico").agg(emp_meses=("empleado_id", "size"), he=("horas_extra", "mean"),
    ausencias=("dias_ausente", "mean"), lic_medica=("dias_licencia_medica", "mean"),
    incid_x1000=("incidentes_seguridad_count", lambda s: s.sum() / len(s) * 1000)).round(3)
print(em.to_string())
a_c = pa2[pa2.cronico].dias_ausente; a_n = pa2[~pa2.cronico].dias_ausente
dif = a_c.mean() - a_n.mean()
se = np.sqrt(a_c.var()/len(a_c) + a_n.var()/len(a_n))
print(f"\n  Diferencia en dias de ausencia/mes: {dif:+.3f} (t = {dif/se:.2f})")
lift = (a_c.mean()/a_n.mean()-1)*100
print(f"  Los cronicos se ausentan {lift:+.1f}% mas por mes")

sal_medio = ult.salario_base_mensual.mean()
dias_extra = dif * pa2.cronico.sum() / MESES * 12
print(f"\n  Dias de ausencia EXCEDENTES por anio atribuibles a sobrecarga: {dias_extra:.0f}")
print(f"  Costo: ${dias_extra * sal_medio/30:,.0f}/anio  <- este SI es el caso economico, y es chico")
print("\n  Rotacion: cronicos {:.1f}% vs resto {:.1f}%".format(
    u[u.cronico].salio.mean()*100, u[~u.cronico].salio.mean()*100))
print("  --> El caso de las horas extra es de RIESGO OPERATIVO y capacidad, no de ahorro directo.")

print("\n### CONCENTRACION: donde estan los 61 cronicos")
det = u[u.cronico]
print(det.groupby("area").agg(n=("empleado_id", "size"), he=("he_prom", "mean"),
      rot=("salio", "mean")).round(2).sort_values("n", ascending=False).to_string())
print("\n  Por turno:")
print(det.groupby("turno_trabajo").agg(n=("empleado_id", "size"), he=("he_prom", "mean")).round(1).to_string())
det.to_csv(T / "P3_cronicos_detalle.csv", index=False, encoding="utf-8-sig")
