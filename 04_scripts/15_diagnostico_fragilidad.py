# -*- coding: utf-8 -*-
"""Donde esta fragil el Discovery: el numero que sostiene el business case."""
import pandas as pd, numpy as np
from pathlib import Path
D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
evt = pd.read_parquet(D / "eventos_limpio.parquet")
pd.set_option("display.width", 200)

print("=" * 88)
print("A — DE QUE ESTA HECHO EL COSTO POR SALIDA ($5,88M)")
print("=" * 88)
cont = evt[evt.tipo_evento == "contratacion"]
onb = evt[evt.tipo_evento == "onboarding"]
sal_medio = ult[ult.salio].salario_base_mensual.mean()
ttf = cont.dias_time_to_fill.mean()
comp = {
    "Reclutamiento (dato real del cliente)": cont.costo_estimado.mean(),
    "Onboarding (dato real del cliente)":    onb.costo_estimado.mean(),
    "Vacancia (SUPUESTO NUESTRO)":           ttf / 30 * sal_medio,
    "Rampa 3 meses al 50% (SUPUESTO NUESTRO)": 3 * sal_medio * 0.50,
}
tot = sum(comp.values())
for k, v in comp.items():
    print(f"  {k:42s} ${v:>13,.0f}   {v/tot*100:5.1f}%")
print(f"  {'TOTAL':42s} ${tot:>13,.0f}")
supuesto = comp["Vacancia (SUPUESTO NUESTRO)"] + comp["Rampa 3 meses al 50% (SUPUESTO NUESTRO)"]
print(f"\n  >> {supuesto/tot*100:.0f}% del costo por salida son supuestos nuestros, no datos del cliente.")
print(f"  >> El business case de $92M descansa entero sobre eso.")

print("\n  Sensibilidad — que pasa si los supuestos son mas conservadores:")
n_vol = (ult.motivo_salida == "Renuncia voluntaria").sum() / 17 * 12
esc = [
    ("Solo datos reales (sin vacancia ni rampa)", 0.0, 0.0),
    ("Vacancia al 50%, rampa 2 meses al 30%",     0.50, 2 * 0.30),
    ("Nuestro escenario actual",                  1.00, 3 * 0.50),
    ("Vacancia completa, rampa 6 meses al 50%",   1.00, 6 * 0.50),
]
for nombre, f_vac, meses_eq in esc:
    c = comp["Reclutamiento (dato real del cliente)"] + comp["Onboarding (dato real del cliente)"]
    c += comp["Vacancia (SUPUESTO NUESTRO)"] * f_vac + sal_medio * meses_eq
    print(f"    {nombre:44s} ${c:>12,.0f}/salida -> ahorro 25% = ${c*n_vol*0.25:>13,.0f}/anio")

print("\n" + "=" * 88)
print("B — LAS 483 FILAS RARAS: HAY REINGRESOS QUE INFLAN LA ROTACION?")
print("=" * 88)
print(f"  Filas con antiguedad declarada distinta de la calculada: {int(panel.flag_antig_inconsistente.sum())}")
emp_raros = panel[panel.flag_antig_inconsistente].empleado_id.nunique()
print(f"  Empleados afectados: {emp_raros}")
# un reingreso se ve como: la fecha de ingreso CAMBIA para el mismo empleado
cambios = panel.groupby("empleado_id").fecha_ingreso.nunique()
print(f"  Empleados con MAS DE UNA fecha de ingreso: {int((cambios > 1).sum())}")
# o como: la antiguedad BAJA de un mes al siguiente
panel_o = panel.sort_values(["empleado_id", "mes_snapshot"])
salto = panel_o.groupby("empleado_id").antiguedad_meses.diff()
retro = panel_o[salto < 0]
print(f"  Casos donde la antiguedad BAJA de un mes al siguiente: {len(retro)} "
      f"({retro.empleado_id.nunique()} empleados)")
if len(retro):
    print("\n  Ejemplos:")
    print(retro[["empleado_id", "mes_snapshot", "antiguedad_meses", "fecha_ingreso", "area"]].head(6).to_string(index=False))
# empleados que aparecen, desaparecen y vuelven
pres = panel.groupby("empleado_id").mes_snapshot.agg(["min", "max", "size"])
meses_totales = panel.mes_snapshot.nunique()
span = ((pres["max"].dt.year - pres["min"].dt.year) * 12 + (pres["max"].dt.month - pres["min"].dt.month) + 1)
huecos = pres[span > pres["size"]]
print(f"\n  Empleados con HUECOS en su historia (aparecen, faltan, vuelven): {len(huecos)}")
if len(huecos):
    print(huecos.head(5).to_string())

print("\n" + "=" * 88)
print("C — MANTENIMIENTO ELECTRICO: 34,8% ES REALMENTE DISTINTO DEL 19%?")
print("=" * 88)
base = ult.salio.mean()
print(f"  Rotacion global: {base*100:.1f}% ({int(ult.salio.sum())} de {len(ult)})")
filas = []
for area, sub in ult.groupby("area"):
    n, k = len(sub), int(sub.salio.sum())
    if n < 15:
        continue
    p = k / n
    # intervalo de confianza 95% (Wilson) — robusto con n chico
    z = 1.96
    den = 1 + z**2 / n
    centro = (p + z**2 / (2 * n)) / den
    margen = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    lo, hi = max(0, centro - margen), min(1, centro + margen)
    # test contra la tasa global
    se = np.sqrt(base * (1 - base) / n)
    zt = (p - base) / se
    filas.append({"area": area, "n": n, "salidas": k, "rotacion_%": round(p * 100, 1),
                  "IC95_bajo_%": round(lo * 100, 1), "IC95_alto_%": round(hi * 100, 1),
                  "z_vs_global": round(zt, 2),
                  "distinto?": "SI" if abs(zt) > 1.96 else "no"})
r = pd.DataFrame(filas).sort_values("rotacion_%", ascending=False)
print(r.to_string(index=False))
print(f"\n  >> Solo las areas marcadas SI se distinguen del promedio con los datos disponibles.")

print("\n" + "=" * 88)
print("D — LA ROTACION SE ESTA ACELERANDO?")
print("=" * 88)
sal = ult[ult.salio].copy()
sal["mes_salida"] = sal.fecha_salida.values.astype("datetime64[M]")
por_mes = sal.groupby("mes_salida").size().rename("salidas")
hc = panel[panel.activo].groupby("mes_snapshot").empleado_id.nunique().rename("activos")
t = pd.concat([por_mes, hc], axis=1).dropna()
t["tasa_mensual_%"] = (t.salidas / t.activos * 100).round(2)
print(t.to_string())
x = np.arange(len(t))
pend = np.polyfit(x, t["tasa_mensual_%"].values, 1)[0]
print(f"\n  Tendencia: {pend*12:+.2f} puntos porcentuales por anio")
print(f"  Primeros 8 meses: {t['tasa_mensual_%'].head(8).mean():.2f}%/mes | "
      f"ultimos 8: {t['tasa_mensual_%'].tail(8).mean():.2f}%/mes")
