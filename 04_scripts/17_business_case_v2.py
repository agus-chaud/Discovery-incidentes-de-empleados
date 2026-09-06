# -*- coding: utf-8 -*-
"""
MEJORA 1 — business case como rango, con el dato duro separado del supuesto.
MEJORA 2 — margen de error en toda comparacion entre areas.
"""
import pandas as pd, numpy as np
from pathlib import Path
import json, math
D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
T = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\tablas_soporte")
panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
evt = pd.read_parquet(D / "eventos_limpio.parquet")
pd.set_option("display.width", 210)

INICIO = panel.mes_snapshot.min()
CORTE = INICIO + pd.DateOffset(months=1)          # periodo limpio (mejora 3)
sal = ult[ult.salio].copy()
sal["mes_salida"] = sal.fecha_salida.values.astype("datetime64[M]")
sal_limpio = sal[sal.mes_salida >= CORTE]
MESES = int(panel[panel.mes_snapshot >= CORTE].mes_snapshot.nunique())
n_vol = int((sal_limpio.motivo_salida == "Renuncia voluntaria").sum()) / MESES * 12

print("=" * 92)
print("MEJORA 1 — COSTO POR SALIDA: DATO DURO vs SUPUESTO")
print("=" * 92)
cont = evt[evt.tipo_evento == "contratacion"]
onb = evt[evt.tipo_evento == "onboarding"]
sal_medio = sal_limpio.salario_base_mensual.mean()
ttf = cont.dias_time_to_fill.mean()

DURO = cont.costo_estimado.mean() + onb.costo_estimado.mean()
print(f"\n  DATO DURO (registrado por el cliente)")
print(f"    Reclutamiento              ${cont.costo_estimado.mean():>12,.0f}")
print(f"    Onboarding                 ${onb.costo_estimado.mean():>12,.0f}")
print(f"    Subtotal verificable       ${DURO:>12,.0f}")
print(f"\n  SUPUESTOS (nuestros — el cliente no los mide)")
print(f"    Salario medio del que sale ${sal_medio:>12,.0f}/mes   <- dato duro")
print(f"    Dias para cubrir el puesto  {ttf:>12.0f} dias  <- dato duro")
print(f"    Fraccion del sueldo que se pierde durante la vacancia  <- SUPUESTO")
print(f"    Meses de rampa y a que rendimiento                     <- SUPUESTO")

# Tres escenarios explicitos. Cada uno declara sus dos supuestos.
ESCENARIOS = {
    "conservador": {"f_vacancia": 0.50, "meses_rampa": 2, "rendimiento_rampa": 0.70,
                    "razon": "el equipo absorbe parte del trabajo; el ingresante rinde 70% desde el mes 1"},
    "central":     {"f_vacancia": 1.00, "meses_rampa": 3, "rendimiento_rampa": 0.50,
                    "razon": "el puesto queda descubierto; el ingresante rinde 50% durante 3 meses"},
    "agresivo":    {"f_vacancia": 1.00, "meses_rampa": 6, "rendimiento_rampa": 0.50,
                    "razon": "puesto descubierto y rampa larga, tipica de perfiles tecnicos"},
}
print(f"\n  COSTO POR SALIDA SEGUN ESCENARIO")
costos = {}
for k, p in ESCENARIOS.items():
    vac = ttf / 30 * sal_medio * p["f_vacancia"]
    rampa = p["meses_rampa"] * sal_medio * (1 - p["rendimiento_rampa"])
    c = DURO + vac + rampa
    costos[k] = c
    print(f"    {k:12s} ${c:>12,.0f}   (duro ${DURO:,.0f} + vacancia ${vac:,.0f} + rampa ${rampa:,.0f})")
    print(f"                 {p['razon']}")

print("\n" + "=" * 92)
print("BUSINESS CASE COMO RANGO — retencion (oportunidad A)")
print("=" * 92)
print(f"  Renuncias voluntarias anualizadas (periodo limpio): {n_vol:.0f}/anio")
print(f"\n  {'':14s}{'reducir 15%':>18s}{'reducir 25%':>18s}{'reducir 40%':>18s}")
tabla = []
for k, c in costos.items():
    fila = {"escenario": k, "costo_salida": round(c)}
    linea = f"  {k:12s}"
    for red in [0.15, 0.25, 0.40]:
        v = c * n_vol * red
        fila[f"reducir_{int(red*100)}pct"] = round(v)
        linea += f"${v:>17,.0f}"
    tabla.append(fila)
    print(linea)
bc = pd.DataFrame(tabla)
bc.to_csv(T / "BC_rango_retencion.csv", index=False, encoding="utf-8-sig")

piso = costos["conservador"] * n_vol * 0.15
techo = costos["agresivo"] * n_vol * 0.40
centro = costos["central"] * n_vol * 0.25
print(f"\n  RANGO COMPLETO: ${piso:,.0f}  a  ${techo:,.0f} por anio")
print(f"  Punto central : ${centro:,.0f} por anio")
print(f"  Amplitud: {techo/piso:.1f}x  -> el rango se reporta, no se esconde detras de un promedio")
print(f"\n  PISO VERIFICABLE (solo dato duro, reduccion 15%): ${DURO*n_vol*0.15:,.0f}/anio")
print("  Ese numero no depende de ningun supuesto nuestro.")

print("\n  QUE PEDIRLE AL CLIENTE para cerrar el rango:")
print("    1. Produccion promedio de un operario formado (unidades/mes por puesto)")
print("    2. Cuantos meses tarda un ingresante en alcanzar ese nivel")
print("    -> con esos dos datos, el 97% que hoy es supuesto pasa a ser medicion")

print("\n" + "=" * 92)
print("MEJORA 2 — MARGEN DE ERROR EN LAS COMPARACIONES POR AREA")
print("=" * 92)
# universo limpio: excluye las 19 salidas de arrastre
ult2 = ult.copy()
ids_arrastre = set(sal[sal.mes_salida == INICIO].empleado_id)
ult2 = ult2[~ult2.empleado_id.isin(ids_arrastre)]
base = ult2.salio.mean()
print(f"  Rotacion global (periodo limpio): {base*100:.1f}% "
      f"({int(ult2.salio.sum())} de {len(ult2)})\n")

def wilson(k, n, z=1.96):
    """Intervalo de confianza 95% para una proporcion. Robusto con n chico."""
    p = k / n
    den = 1 + z**2 / n
    centro = (p + z**2 / (2 * n)) / den
    margen = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    return max(0, centro - margen), min(1, centro + margen)

filas = []
for area, sub in ult2.groupby("area"):
    n, k = len(sub), int(sub.salio.sum())
    if n < 15:
        continue
    p = k / n
    lo, hi = wilson(k, n)
    z = (p - base) / np.sqrt(base * (1 - base) / n)
    p_valor = math.erfc(abs(z) / math.sqrt(2))  # p bilateral, sin corregir
    filas.append({"area": area, "personas": n, "salidas": k,
                  "rotacion_%": round(p * 100, 1),
                  "IC95_%": f"{lo*100:.1f} – {hi*100:.1f}",
                  "z": round(z, 2),
                  "p_valor": round(p_valor, 5),
                  "veredicto": "PEOR que el promedio" if z > 1.96 else
                               ("MEJOR que el promedio" if z < -1.96 else "sin diferencia")})
r = pd.DataFrame(filas).sort_values("rotacion_%", ascending=False)

# DEC-019b — correccion de Bonferroni: testeamos r.shape[0] areas contra el
# promedio de la empresa, asi que el umbral de significancia individual baja
# de 0.05 a 0.05/n_areas para mantener el 5% de falsa alarma GLOBAL.
n_areas = len(r)
alpha_bonferroni = 0.05 / n_areas
r["sig_bonferroni"] = np.where(r.p_valor < alpha_bonferroni, "Se sostiene", "No sobrevive")
r.loc[r.veredicto == "sin diferencia", "sig_bonferroni"] = "no aplica"  # "n/a" colisiona con los NA por defecto de pandas al releer el CSV

print(r.to_string(index=False))
r.to_csv(T / "P5_rotacion_por_area_con_IC.csv", index=False, encoding="utf-8-sig")
distintas = r[r.veredicto != "sin diferencia"]
print(f"\n  >> Areas que se distinguen del promedio (sin corregir): {len(distintas)} de {len(r)}")
for _, x in distintas.iterrows():
    print(f"     {x.area}: {x['rotacion_%']}% (rango real {x['IC95_%']}%) — {x.veredicto}, "
          f"p={x.p_valor:.5f} vs umbral Bonferroni {alpha_bonferroni:.4f} -> {x.sig_bonferroni}")
print("  >> El resto NO se puede afirmar que rote distinto del promedio.")
print(f"  >> Umbral Bonferroni ({n_areas} areas testeadas, alpha global 5%): "
      f"alpha individual = {alpha_bonferroni:.4f}")

print("\n  Lo mismo para TOP PERFORMERS:")
for etiqueta, sub in [("Top performers", ult2[ult2.es_top_performer]),
                      ("Resto", ult2[~ult2.es_top_performer])]:
    n, k = len(sub), int(sub.salio.sum())
    lo, hi = wilson(k, n)
    print(f"    {etiqueta:16s} n={n:3d}  {k/n*100:5.1f}%  (rango real {lo*100:.1f} – {hi*100:.1f}%)")
a, b = ult2[ult2.es_top_performer], ult2[~ult2.es_top_performer]
pa, pb = a.salio.mean(), b.salio.mean()
pp = (a.salio.sum() + b.salio.sum()) / (len(a) + len(b))
zt = (pa - pb) / np.sqrt(pp * (1 - pp) * (1 / len(a) + 1 / len(b)))
print(f"    Diferencia: z = {zt:.2f} -> "
      f"{'SI se distingue' if abs(zt) > 1.96 else 'NO se distingue — con estos datos puede ser azar'}")

resumen = {
    "periodo_limpio_desde": str(CORTE.date()),
    "renuncias_voluntarias_anuales": round(n_vol),
    "costo_salida": {k: round(v) for k, v in costos.items()},
    "supuestos": ESCENARIOS,
    "ahorro_anual": {"piso": round(piso), "central": round(centro), "techo": round(techo),
                     "piso_solo_dato_duro": round(DURO * n_vol * 0.15)},
    "areas_que_se_distinguen": distintas.area.tolist(),
}
(T / "BC_supuestos.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nGuardado: BC_rango_retencion.csv, P5_rotacion_por_area_con_IC.csv, BC_supuestos.json")
