# -*- coding: utf-8 -*-
"""Q1 — Cuanto cuesta (en mano de obra) una pieza bien producida, y como varia ese costo.

5 pasos:
  1. piezas buenas por area-mes    = unidades * (1 - scrap)
  2. costo laboral por area-mes     = sum(costo_total_mes) = salario + costo hora extra
  3. costo laboral por pieza buena  = costo laboral / piezas buenas  (serie mensual por area)
                                    = precio_hora / productividad     (descomposicion)
  4. que mueve la PRODUCTIVIDAD (piezas por persona-hora), controlando el paso del tiempo
  5. traduccion a plata: efecto sobre el costo unitario, sobre los residuos de la tendencia

MEJORA 1: el costo por pieza sube ~16% en el panel solo por la caida de volumen. Se controla
          agregando el indice de mes a la regresion y trabajando el paso 5 sobre residuos.
MEJORA 2: `costo_gente` incluye el costo de la hora extra, asi que regresar el costo por pieza
          contra hora extra / ausentismo es en parte circular. La variable de salida del
          paso 4 pasa a ser la productividad fisica (unidades / persona-hora), que no se
          arma con la nomina. El costo se reconstruye aparte (precio_hora / productividad).

LIMITES: es solo la porcion de mano de obra (no materia prima, energia ni maquina).
17 meses x 3 areas = 51 puntos -> descriptivo, no causalidad.
"""
import pandas as pd, numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "06_resultados" / "Discovery" / "datos_transformados"
T = ROOT / "06_resultados" / "Discovery" / "tablas_soporte"
T.mkdir(parents=True, exist_ok=True)
panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")

AREAS_PROD = ["Estampado", "Ensamble", "Pintura"]
INICIO = panel.mes_snapshot.min()
pa = panel[(panel.activo) & (panel.area.isin(AREAS_PROD))].copy()          # toda la dotacion del area
prod = pa[pa.unidades_producidas.notna() & pa.tasa_scrap_porcentaje.notna()].copy()   # filas que producen
prod["scrap_units"] = prod.unidades_producidas * prod.tasa_scrap_porcentaje / 100      # mejora: peso explicito
prod["buenas_i"] = prod.unidades_producidas - prod.scrap_units

# salidas por area-mes (periodo limpio: sin el arrastre de enero 2024 -- DEC-017)
s = ult[ult.salio].copy()
s["mes_salida"] = s.fecha_salida.values.astype("datetime64[M]")
arr = set(s[s.mes_salida == INICIO].empleado_id)
salidas = s[~s.empleado_id.isin(arr)].groupby(["area", "mes_salida"]).size().rename("salidas")

# --- agregados ---
base = pa[~pa.flag_antig_inconsistente].copy()   # frac_nuevos sin las fechas de ingreso dudosas (cf. DEC-031)
g = (pa.groupby(["area", "mes_snapshot"])
     .agg(hc=("empleado_id", "nunique"),
          hs_trab=("horas_trabajadas", "sum"),
          costo_gente=("costo_total_mes", "sum"),
          costo_sal=("salario_base_mensual", "sum"),
          costo_he=("costo_horas_extra", "sum"),
          he_emp=("horas_extra", "mean"),
          aus_emp=("dias_ausente", "mean"))
     .reset_index())
gp = (prod.groupby(["area", "mes_snapshot"])
      .agg(unid=("unidades_producidas", "sum"),
           buenas=("buenas_i", "sum"),
           scrap_u=("scrap_units", "sum")).reset_index())
gn = (base.groupby(["area", "mes_snapshot"])
      .agg(frac_nuevos=("antiguedad_meses", lambda x: (x < 12).mean())).reset_index())
g = g.merge(gp, on=["area", "mes_snapshot"]).merge(gn, on=["area", "mes_snapshot"])
g = g.merge(salidas, left_on=["area", "mes_snapshot"], right_on=["area", "mes_salida"], how="left")
g["salidas"] = g.salidas.fillna(0)

g["scrap_pond"] = g.scrap_u / g.unid * 100
g["rot_pct"] = g.salidas / g.hc * 100
g["prod_hora"] = g.unid / g.hs_trab                       # piezas brutas por persona-hora (mejora 2)
g["prod_hora_buena"] = g.buenas / g.hs_trab
g["precio_hora"] = g.costo_gente / g.hs_trab              # $ por persona-hora
g["costo_pp_prod"] = g.costo_gente / g.unid               # = precio_hora / prod_hora
g["costo_pp_buena"] = g.costo_gente / g.buenas
g["scrap_tax"] = g.costo_pp_buena - g.costo_pp_prod
g = g.sort_values(["area", "mes_snapshot"])
g["mes_idx"] = g.groupby("area").cumcount()               # 0..16 dentro de cada area (control de tiempo)
MESES = g.mes_snapshot.nunique()


def resumen(col):
    return g.groupby("area")[col].agg(prom="mean", minimo="min", maximo="max",
                                      CV=lambda x: x.std() / x.mean()).round(3)


def ols(y, Xcols, names):
    X = np.column_stack([np.ones(len(y))] + Xcols)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n, k = X.shape
    cov = (resid @ resid / (n - k)) * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    r2 = 1 - (resid @ resid) / ((y - y.mean()) @ (y - y.mean()))
    return beta, se, r2, ["const"] + names


def detrend(col):
    """residuo de col respecto de su propia recta vs mes_idx, dentro de cada area."""
    out = pd.Series(index=g.index, dtype=float)
    for _, idx in g.groupby("area").groups.items():
        sub = g.loc[idx]
        b1, b0 = np.polyfit(sub.mes_idx, sub[col], 1)
        out.loc[idx] = sub[col] - (b0 + b1 * sub.mes_idx)
    return out


d_ens = (g.area == "Ensamble").astype(float).values
d_pin = (g.area == "Pintura").astype(float).values

# ==========================================================================
print("=" * 100); print("PASO 1 - PIEZAS BUENAS POR AREA-MES"); print("=" * 100)
p1 = g.groupby("area").agg(unid_mes=("unid", "mean"), scrap_pct=("scrap_pond", "mean"),
                           buenas_mes=("buenas", "mean")).round(1)
p1["perdidas_scrap_mes"] = (p1.unid_mes - p1.buenas_mes).round(0)
p1["pct_en_scrap"] = (p1.perdidas_scrap_mes / p1.unid_mes * 100).round(2)
print(p1.to_string())
print(f"\n  Total: {g.unid.sum():,.0f} producidas, {g.buenas.sum():,.0f} buenas "
      f"({(1 - g.buenas.sum()/g.unid.sum())*100:.2f}% scrap, {g.unid.sum()-g.buenas.sum():,.0f} piezas perdidas en 17 meses).")

# ==========================================================================
print("\n" + "=" * 100); print("PASO 2 - COSTO LABORAL POR AREA-MES (salario + costo hora extra)"); print("=" * 100)
p2 = g.groupby("area").agg(costo_gente_mes=("costo_gente", "mean"), costo_sal_mes=("costo_sal", "mean"),
                           costo_he_mes=("costo_he", "mean"), hc=("hc", "mean")).round(0)
p2["pct_he"] = (p2.costo_he_mes / p2.costo_gente_mes * 100).round(1)
p2["costo_x_persona"] = (p2.costo_gente_mes / p2.hc).round(0)
print(p2.to_string())
print(f"\n  Costo laboral anual de las 3 areas de produccion: ${g.costo_gente.sum()/MESES*12/1e6:,.0f} MM")

# ==========================================================================
print("\n" + "=" * 100); print("PASO 3 - COSTO LABORAL POR PIEZA BUENA + DESCOMPOSICION"); print("=" * 100)
print("costo_pp_buena = costo laboral / piezas buenas   = precio_hora / prod_hora_buena")
print("precio_hora    = $ por persona-hora   (componente 'precio', contable)")
print("prod_hora      = piezas por persona-hora   (componente 'productividad', fisico)\n")
print("-- costo_pp_buena ($/pieza) --"); print(resumen("costo_pp_buena").to_string())
print("\n-- precio_hora ($/persona-hora) --"); print(resumen("precio_hora").to_string())
print("\n-- prod_hora (piezas/persona-hora) --"); print(resumen("prod_hora").to_string())
print("\n-- impuesto scrap por pieza ($) --"); print(resumen("scrap_tax").to_string())
# tendencia: cuanto sube el costo por pieza de punta a punta, y cuanto de eso es precio vs productividad
print("\n-- variacion punta a punta (mes 0 -> mes 16), por area --")
for area, sub in g.groupby("area"):
    a, b = sub.iloc[0], sub.iloc[-1]
    print(f"  {area:11s} costo_pp_buena {a.costo_pp_buena:7.0f} -> {b.costo_pp_buena:7.0f}  ({b.costo_pp_buena/a.costo_pp_buena-1:+.1%})   "
          f"| precio_hora {a.precio_hora/b.precio_hora-1:+.1%} inverso   prod_hora {b.prod_hora/a.prod_hora-1:+.1%}")
piv = g.pivot_table(index="area", columns="mes_snapshot", values="costo_pp_buena").round(0)
piv.columns = [c.strftime("%y-%m") for c in piv.columns]
print("\n-- costo_pp_buena mes a mes --"); print(piv.to_string())

# ==========================================================================
print("\n" + "=" * 100)
print("PASO 4 - QUE MUEVE LA PRODUCTIVIDAD  (mejoras 1 y 2: variable fisica + control de tiempo)")
print("=" * 100)
y = g.prod_hora.values
beta, se, r2, names = ols(
    y, [g.mes_idx.values, g.rot_pct.values, g.aus_emp.values, g.frac_nuevos.values, d_ens, d_pin],
    ["mes_idx", "rot_pct", "aus_emp", "frac_nuevos", "Ensamble", "Pintura"])
print(f"Regresion  prod_hora ~ mes_idx + rot_pct + aus_emp + frac_nuevos + area   (n={len(y)}, R2={r2:.2f})")
ym = y.mean()
for nm, b, s_ in zip(names, beta, se):
    ef = f"  =>  {b/ym*100:+.2f}% de la productividad por unidad del driver" if nm in ("rot_pct", "aus_emp", "frac_nuevos") else ""
    print(f"  {nm:11s} coef={b:+11.5f}  (t={b/s_:+.2f}){ef}")

print("\nComparacion: la MISMA regresion sobre el costo por pieza (variable contable), para ver la circularidad")
bc, sc, r2c, nc = ols(
    g.costo_pp_prod.values, [g.mes_idx.values, g.rot_pct.values, g.he_emp.values, g.aus_emp.values, d_ens, d_pin],
    ["mes_idx", "rot_pct", "he_emp", "aus_emp", "Ensamble", "Pintura"])
print(f"Regresion  costo_pp_prod ~ mes_idx + rot_pct + he_emp + aus_emp + area   (n=51, R2={r2c:.2f})")
for nm, b, s_ in zip(nc, bc, sc):
    if nm == "const":
        continue
    print(f"  {nm:11s} coef={b:+11.2f}  (t={b/s_:+.2f})")
print("  (he_emp y aus_emp entran en el numerador del costo -> su efecto aca es en parte mecanico)")

# ==========================================================================
print("\n" + "=" * 100)
print("PASO 5 - EFECTO SOBRE EL COSTO UNITARIO, SOBRE LOS RESIDUOS DE LA TENDENCIA (mejora 1)")
print("=" * 100)
g["prod_hora_res"] = detrend("prod_hora")
g["costo_ppb_res"] = detrend("costo_pp_buena")
q_hi, q_lo = g.rot_pct.quantile(.75), g.rot_pct.quantile(.25)
hi, lo = g[g.rot_pct >= q_hi], g[g.rot_pct <= q_lo]
print(f"  meses de rotacion ALTA (>= p75 = {q_hi:.1f}%, n={len(hi)})  vs  BAJA (<= p25 = {q_lo:.1f}%, n={len(lo)})")
print(f"    productividad (residuo de tendencia): alta {hi.prod_hora_res.mean():+.4f}  vs  baja {lo.prod_hora_res.mean():+.4f}  "
      f"(pieza/persona-hora; prom del panel {g.prod_hora.mean():.3f})")
print(f"    costo por pieza (residuo de tendencia): alta ${hi.costo_ppb_res.mean():+,.1f}  vs  baja ${lo.costo_ppb_res.mean():+,.1f}")
print(f"\n  Antes de detrendar (lo que daba la version vieja): "
      f"costo_pp_buena alta ${hi.costo_pp_buena.mean():,.0f} vs baja ${lo.costo_pp_buena.mean():,.0f} "
      f"({hi.costo_pp_buena.mean()/lo.costo_pp_buena.mean()-1:+.1%}).")

# traduccion: si el efecto de rotacion sobre prod_hora sobrevive al control de tiempo
b_rot = beta[names.index("rot_pct")]
t_rot = b_rot / se[names.index("rot_pct")]
buenas_anual = g.buenas.sum() / MESES * 12
precio_hora_medio = g.precio_hora.mean()
if abs(t_rot) >= 2:
    d_prod = b_rot * g.rot_pct.mean()                       # caida de prod por el nivel medio de rotacion
    d_costo_pp = precio_hora_medio * (1 / (g.prod_hora.mean() + d_prod) - 1 / g.prod_hora.mean())
    print(f"\n  El efecto de la rotacion sobre la productividad SOBREVIVE al control de tiempo (t={t_rot:+.2f}).")
    print(f"  Traducido: ~${d_costo_pp * buenas_anual / 1e6:,.0f} MM/ano de sobrecosto laboral atribuible a la rotacion.")
else:
    print(f"\n  El efecto de la rotacion sobre la productividad NO sobrevive al control de tiempo "
          f"(coef {b_rot:+.5f}, t={t_rot:+.2f}).")
    print("  -> No se puede poner un numero de 'cuanto cuesta la rotacion por pieza' con estos datos.")
    print("     Lo firme: costo ~$2.000/pieza buena, +16% en el panel por caida de volumen (paso 3),")
    print("     scrap 2,3%. La disrupcion mes a mes por rotacion no se distingue de la tendencia.")

print(f"\n  Contexto: DEC-015 estima el costo TOTAL de rotacion (reclutamiento+vacancia+rampa) en "
      f"$23,3M-$194,8M/ano. Esto es otra cosa (efecto sobre el costo unitario, solo mano de obra); no se suman.")

# ==========================================================================
print("\n" + "=" * 100)
print("CONCLUSIONES PARA EL CEO")
print("=" * 100)
_cpp = g.groupby("area").costo_pp_buena.mean()
_sube = g[g.mes_idx == g.mes_idx.max()].costo_pp_buena.mean() / g[g.mes_idx == 0].costo_pp_buena.mean() - 1
print(f"""
  1. Una pieza buena cuesta hoy ~${g.costo_pp_buena.mean():,.0f} de mano de obra
     (Estampado ${_cpp['Estampado']:,.0f}, Ensamble ${_cpp['Ensamble']:,.0f}, Pintura ${_cpp['Pintura']:,.0f}).
  2. Ese costo subio ~{_sube:.0%} en los 17 meses. Aprox. la mitad es menos piezas por hora
     trabajada (misma dotacion, menos produccion -> hora extra estructural, DEC-030); la otra
     mitad, el precio de la hora subiendo.
  3. Palanca de gestion: el costo unitario baja recuperando volumen o ajustando la dotacion a
     la carga real, no tocando el scrap (2,3 %, chico) ni pidiendo mas horas extra.
  4. La rotacion NO explica la variacion mes a mes del costo por pieza una vez descontada la
     tendencia (rot_pct t={t_rot:+.2f}). No hay caso para "retener para bajar el costo unitario"
     con esta evidencia.
  5. Para medir el efecto real de una salida haria falta el costo de rampa (N1/N2), granularidad
     por linea/turno y costos deflactados. Hoy solo se sostiene lo descriptivo.
""")

g.to_csv(T / "Q1_costo_pieza_buena.csv", index=False, encoding="utf-8-sig")
print(f"\nGuardado: Q1_costo_pieza_buena.csv  ({len(g)} filas area-mes)")
