# -*- coding: utf-8 -*-
"""Business case cuantificado de las oportunidades priorizadas."""
import pandas as pd, numpy as np
from pathlib import Path
D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
T = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\tablas_soporte")

panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
evt = pd.read_parquet(D / "eventos_limpio.parquet")
pa = panel[panel.activo].copy()
act = ult[~ult.salio].copy()
MESES = pa.mes_snapshot.nunique()

print("=" * 95)
print("BASELINE ECONOMICO (17 meses observados -> anualizado)")
print("=" * 95)
nom_base = pa.salario_base_mensual.sum() / MESES * 12
costo_he = pa.costo_horas_extra.sum() / MESES * 12
hc = pa.groupby("mes_snapshot").empleado_id.nunique().mean()
print(f"  Headcount promedio                : {hc:.0f}")
print(f"  Nomina base anualizada            : ${nom_base:,.0f}")
print(f"  Costo horas extra anualizado      : ${costo_he:,.0f}  ({costo_he/nom_base*100:.1f}% de la base)")
print(f"  Costo laboral total anualizado    : ${nom_base + costo_he:,.0f}")

print("\n" + "=" * 95)
print("OPORTUNIDAD 1 — CONVERTIR HORAS EXTRA ESTRUCTURALES EN DOTACION")
print("=" * 95)
h_mes = pa.horas_extra.sum() / MESES
jornada = pa.horas_trabajadas.mean()
fte_eq = h_mes / jornada
print(f"  Horas extra totales por mes       : {h_mes:,.0f} h")
print(f"  Jornada mensual promedio          : {jornada:.0f} h")
print(f"  --> FTE EQUIVALENTES en horas extra: {fte_eq:.1f} personas")
print(f"      (la planta cubre el trabajo de {fte_eq:.0f} personas pagando recargo)")

sal_blue = pa[pa.categoria_collar == "Blue"].salario_base_mensual.mean()
costo_hora_he = pa.costo_horas_extra.sum() / pa.horas_extra.sum()
costo_hora_norm = sal_blue / jornada
print(f"\n  Costo por hora EXTRA              : ${costo_hora_he:,.0f}")
print(f"  Costo por hora NORMAL (blue)      : ${costo_hora_norm:,.0f}")
print(f"  --> Recargo efectivo              : {costo_hora_he/costo_hora_norm:.2f}x")

CARGAS = 0.45  # cargas sociales estimadas sobre salario base
print(f"\n  Supuesto: cargas sociales {CARGAS*100:.0f}% sobre nomina de nuevos ingresos")
for pct, esc in [(0.20, "MINIMO"), (0.35, "ESPERADO"), (0.50, "MAXIMO")]:
    fte_conv = fte_eq * pct
    ahorro_he = costo_he * pct
    costo_nuevos = fte_conv * sal_blue * 12 * (1 + CARGAS)
    neto = ahorro_he - costo_nuevos
    print(f"    {esc:9s}: convertir {pct*100:.0f}% ({fte_conv:4.1f} FTE) | ahorro HE ${ahorro_he:>15,.0f} | "
          f"costo nuevos ${costo_nuevos:>15,.0f} | NETO ${neto:>15,.0f}")

print("\n" + "=" * 95)
print("OPORTUNIDAD 2 — REDUCIR ROTACION VOLUNTARIA")
print("=" * 95)
sal_out = ult[ult.salio]
cont = evt[evt.tipo_evento == "contratacion"]
onb = evt[evt.tipo_evento == "onboarding"]
c_directo = cont.costo_estimado.mean() + onb.costo_estimado.mean()
ttf = cont.dias_time_to_fill.mean()
sal_medio = sal_out.salario_base_mensual.mean()
c_vacancia = ttf / 30 * sal_medio
# curva de aprendizaje: 3 meses al 50% de productividad
c_rampa = 3 * sal_medio * 0.50
c_total_salida = c_directo + c_vacancia + c_rampa
n_vol_anual = (ult.motivo_salida == "Renuncia voluntaria").sum() / MESES * 12
print(f"  Costo directo (reclutamiento+onboarding): ${c_directo:,.0f}")
print(f"  Costo vacancia ({ttf:.0f} d de time-to-fill)   : ${c_vacancia:,.0f}")
print(f"  Costo rampa (3 meses al 50%)            : ${c_rampa:,.0f}")
print(f"  --> COSTO TOTAL POR SALIDA              : ${c_total_salida:,.0f}")
print(f"\n  Renuncias voluntarias anualizadas       : {n_vol_anual:.0f}")
print(f"  COSTO ANUAL de rotacion voluntaria      : ${c_total_salida * n_vol_anual:,.0f}")
for pct, esc in [(0.15, "MINIMO"), (0.25, "ESPERADO"), (0.40, "MAXIMO")]:
    print(f"    {esc:9s}: reducir {pct*100:.0f}% -> evitar {n_vol_anual*pct:.0f} salidas | "
          f"ahorro ${c_total_salida*n_vol_anual*pct:,.0f}/anio")

print("\n  Foco: Mantenimiento Electrico (peor area)")
me = ult[ult.area == "Mantenimiento Eléctrico"]
me_vol = (me.motivo_salida == "Renuncia voluntaria").sum()
print(f"    Dotacion {len(me)} | salidas {int(me.salio.sum())} ({me.salio.mean()*100:.1f}%) | voluntarias {me_vol}")
print(f"    Costo anual solo de esta area: ${c_total_salida * me_vol / MESES * 12:,.0f}")

print("\n" + "=" * 95)
print("OPORTUNIDAD 3 — SEGURIDAD EN TURNO NOCHE")
print("=" * 95)
inc = evt[evt.tipo_evento == "incidente_seguridad"].copy()
inc["mes"] = inc.fecha_evento.values.astype("datetime64[M]")
inc["k"] = inc.empleado_id.astype(str) + "|" + inc.mes.astype(str)
panel["k"] = panel.empleado_id.astype(str) + "|" + panel.mes_snapshot.astype(str)
inc = inc.merge(panel[["k", "turno_trabajo"]], on="k", how="left")
noche = inc[inc.turno_trabajo == "Noche"]
dias_noche = noche.dias_perdidos.sum()
costo_dia = sal_medio / 30
print(f"  Incidentes en Noche: {len(noche)} de {len(inc)} ({len(noche)/len(inc)*100:.0f}%)")
print(f"  Dias perdidos en Noche: {dias_noche} de {inc.dias_perdidos.sum()} ({dias_noche/inc.dias_perdidos.sum()*100:.0f}%)")
print(f"  Costo directo registrado (Noche): ${noche.costo_estimado.sum():,.0f} en {MESES} meses")
c_dias = dias_noche / MESES * 12 * costo_dia
c_directo_n = noche.costo_estimado.sum() / MESES * 12
print(f"\n  Costo anualizado dias perdidos   : ${c_dias:,.0f}")
print(f"  Costo anualizado directo         : ${c_directo_n:,.0f}")
print(f"  --> COSTO ANUAL VISIBLE de Noche : ${c_dias + c_directo_n:,.0f}")
print("\n  ATENCION: el costo financiero directo es BAJO frente a la nomina.")
print("  El caso NO es de ahorro, es de EXPOSICION: 6 incidentes graves en 17 meses,")
print(f"  {inc[inc.severidad=='Grave'].dias_perdidos.sum():.0f} dias perdidos, y un 55% de incidentes sin causa raiz registrada.")
n_noche = pa[pa.turno_trabajo == "Noche"].empleado_id.nunique()
print(f"  Poblacion expuesta: {n_noche} personas rotan por turno noche.")
tasa_noche = len(noche) / (pa.turno_trabajo == "Noche").sum() * 1000
tasa_dia = len(inc[inc.turno_trabajo.isin(["Mañana", "Tarde"])]) / pa.turno_trabajo.isin(["Mañana", "Tarde"]).sum() * 1000
print(f"  Si Noche igualara la tasa diurna ({tasa_dia:.1f} vs {tasa_noche:.1f} x1000):")
eq = (tasa_noche - tasa_dia) / 1000 * (pa.turno_trabajo == "Noche").sum() / MESES * 12
print(f"    se evitarian {eq:.0f} incidentes por anio ({eq/ (len(inc)/MESES*12) * 100:.0f}% del total)")

print("\n" + "=" * 95)
print("RESUMEN — VALOR ANUAL EN JUEGO")
print("=" * 95)
res = pd.DataFrame([
    {"Oportunidad": "Horas extra -> dotacion", "Minimo": costo_he*0.20 - fte_eq*0.20*sal_blue*12*1.45,
     "Esperado": costo_he*0.35 - fte_eq*0.35*sal_blue*12*1.45, "Maximo": costo_he*0.50 - fte_eq*0.50*sal_blue*12*1.45,
     "Evidencia": "Impacto estimado"},
    {"Oportunidad": "Rotacion voluntaria", "Minimo": c_total_salida*n_vol_anual*0.15,
     "Esperado": c_total_salida*n_vol_anual*0.25, "Maximo": c_total_salida*n_vol_anual*0.40,
     "Evidencia": "Impacto estimado"},
    {"Oportunidad": "Seguridad turno noche", "Minimo": (c_dias+c_directo_n)*0.30,
     "Esperado": (c_dias+c_directo_n)*0.55, "Maximo": (c_dias+c_directo_n)*0.80,
     "Evidencia": "Exploratorio (n=45)"},
])
res["Minimo"] = res.Minimo.round(0); res["Esperado"] = res.Esperado.round(0); res["Maximo"] = res.Maximo.round(0)
print(res.to_string(index=False))
print(f"\n  TOTAL esperado anual: ${res.Esperado.sum():,.0f}")
print(f"  Rango: ${res.Minimo.sum():,.0f}  a  ${res.Maximo.sum():,.0f}")
res.to_csv(T / "BC_resumen_oportunidades.csv", index=False, encoding="utf-8-sig")
