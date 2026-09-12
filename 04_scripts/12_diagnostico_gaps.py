# -*- coding: utf-8 -*-
"""Diagnostico de brechas del Discovery contra los contratos ds-04 y ds-05."""
import pandas as pd, numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "06_resultados" / "Discovery" / "datos_transformados"
panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
pd.set_option("display.width", 200)

print("=" * 90)
print("GAP 1 — FALTANTES NO ALEATORIOS: mis comparaciones de scrap son validas?")
print("=" * 90)
print("\n  % nulos de tasa_scrap_porcentaje por categoria de collar:")
print(panel.groupby("categoria_collar").tasa_scrap_porcentaje.apply(
    lambda s: pd.Series({"n": len(s), "pct_nulo": round(s.isna().mean() * 100, 1)})).unstack().to_string())
print("\n  % nulos por area:")
t = panel.groupby("area").tasa_scrap_porcentaje.apply(
    lambda s: pd.Series({"n": len(s), "pct_nulo": round(s.isna().mean() * 100, 1)})).unstack()
print(t.sort_values("pct_nulo", ascending=False).to_string())

print("\n  >> En el informe compare scrap accidentados (3,23) vs no accidentados (2,35).")
ult["tuvo_inc"] = ult.incidentes_total > 0
chk = ult.groupby("tuvo_inc").agg(
    n=("empleado_id", "size"),
    n_con_scrap=("scrap_prom_produccion", lambda s: s.notna().sum()),
    pct_perdido=("scrap_prom_produccion", lambda s: round(s.isna().mean() * 100, 1)),
    scrap=("scrap_prom_produccion", "mean")).round(2)
print(chk.to_string())
print("  >> La media se calculo sobre subconjuntos distintos. Es comparable?")
b = ult.groupby(["tuvo_inc", "categoria_collar"]).scrap_prom_produccion.apply(lambda s: s.notna().mean() * 100).round(1)
print("\n  Cobertura de scrap por grupo y collar (%):")
print(b.to_string())

print("\n" + "=" * 90)
print("GAP 2 — OUTLIERS: el salario tiene cola larga que puede distorsionar el OLS")
print("=" * 90)
act = ult[~ult.salio]
s = act.salario_base_mensual
q1, q3 = s.quantile(.25), s.quantile(.75)
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
out = s[(s < lo) | (s > hi)]
print(f"  n={len(s)} | p25=${q1:,.0f} p50=${s.median():,.0f} p75=${q3:,.0f}")
print(f"  Limite IQR superior: ${hi:,.0f} | maximo observado: ${s.max():,.0f} ({s.max()/s.median():.1f}x la mediana)")
print(f"  Outliers por IQR: {len(out)} ({len(out)/len(s)*100:.1f}%)")
print("\n  Quienes son (top 8):")
print(act.nlargest(8, "salario_base_mensual")[
    ["area", "puesto", "nivel_jerarquico", "genero", "salario_base_mensual"]].to_string(index=False))
print("\n  >> Son ejecutivos reales o errores de carga? Reviso coherencia con nivel:")
print(act.groupby("nivel_jerarquico").salario_base_mensual.agg(["size", "min", "median", "max"]).round(0).to_string())

print("\n" + "=" * 90)
print("GAP 3 — NOMBRES DE COLUMNA fuera de snake_case ASCII")
print("=" * 90)
import unicodedata
malas = [c for c in panel.columns
         if c != unicodedata.normalize("NFKD", c).encode("ascii", "ignore").decode()
         or c != c.lower() or " " in c]
print(f"  Columnas problematicas: {len(malas)} -> {malas}")

print("\n" + "=" * 90)
print("GAP 4 — TIPOS sospechosos")
print("=" * 90)
print(f"  manager_id dtype={panel.manager_id.dtype} | ejemplo={panel.manager_id.dropna().iloc[0]}")
print(f"    -> es un ID guardado como float. Valores no enteros: {int((panel.manager_id.dropna() % 1 != 0).sum())}")
print(f"  empleado_id dtype={panel.empleado_id.dtype} (correcto: entero)")
obj = [c for c in panel.columns if panel[c].dtype == "object"]
print(f"\n  Columnas object ({len(obj)}): {obj}")

print("\n" + "=" * 90)
print("GAP 5 — ALERTAS AUTOMATICAS que un pase EDA sistematico habria levantado")
print("=" * 90)
al = []
for c in panel.columns:
    s2 = panel[c]
    m = s2.isna().mean()
    if m > 0.20:
        al.append((c, "FALTANTES", f"{m*100:.1f}% nulo"))
    if s2.notna().any():
        top = s2.value_counts(normalize=True, dropna=True)
        if len(top) and top.iloc[0] >= 0.99:
            al.append((c, "CASI CONSTANTE", f"valor dominante {top.iloc[0]*100:.1f}%"))
    if s2.dtype == "object" and s2.nunique() > max(50, 0.5 * np.sqrt(len(s2))):
        al.append((c, "ALTA CARDINALIDAD", f"{s2.nunique()} valores únicos"))
print(pd.DataFrame(al, columns=["columna", "alerta", "detalle"]).to_string(index=False))
