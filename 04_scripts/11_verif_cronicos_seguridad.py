# -*- coding: utf-8 -*-
"""Ultima verificacion: los sobrecargados cronicos se accidentan mas? (fuente auditable)"""
import pandas as pd, numpy as np
from pathlib import Path
D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
evt = pd.read_parquet(D / "eventos_limpio.parquet")
pa = panel[panel.activo].copy()

umbral = pa.horas_extra.quantile(0.80)
pa["he_alta"] = pa.horas_extra >= umbral
cr = pa.groupby("empleado_id").agg(m=("he_alta", "size"), a=("he_alta", "sum"))
cr["cronico"] = ((cr.a / cr.m * 100) >= 70) & (cr.m >= 6)
pa = pa.merge(cr[["cronico"]], on="empleado_id", how="left")
pa["cronico"] = pa.cronico.fillna(False).astype(bool)

inc = evt[evt.tipo_evento == "incidente_seguridad"].copy()
inc["mes"] = inc.fecha_evento.values.astype("datetime64[M]")
cro_ids = set(cr[cr.cronico].index)

print("### INCIDENTES DE SOBRECARGADOS CRONICOS — dos fuentes comparadas\n")
# fuente A: panel (columna incidentes_seguridad_count)
a = pa.groupby("cronico").agg(emp_meses=("empleado_id", "size"),
                              inc=("incidentes_seguridad_count", "sum"))
a["tasa_x1000"] = (a.inc / a.emp_meses * 1000).round(1)
print("  FUENTE A — panel (columna incidentes_seguridad_count):")
print(a.to_string())
print(f"    ratio cronico/no-cronico: {a.loc[True,'tasa_x1000']/a.loc[False,'tasa_x1000']:.2f}x")

# fuente B: eventos_rrhh (auditable)
inc["cronico"] = inc.empleado_id.isin(cro_ids)
b = pa.groupby("cronico").size().rename("emp_meses").to_frame()
b["inc"] = inc.groupby("cronico").size().reindex(b.index).fillna(0).astype(int)
b["tasa_x1000"] = (b.inc / b.emp_meses * 1000).round(1)
print("\n  FUENTE B — eventos_rrhh (auditable, con causa raiz):")
print(b.to_string())
r = b.loc[True, "tasa_x1000"] / b.loc[False, "tasa_x1000"] if b.loc[False, "tasa_x1000"] else np.nan
print(f"    ratio cronico/no-cronico: {r:.2f}x")

# test binomial simple sobre la fuente auditable
n_c, n_n = b.loc[True, "emp_meses"], b.loc[False, "emp_meses"]
i_c, i_n = b.loc[True, "inc"], b.loc[False, "inc"]
p_pool = (i_c + i_n) / (n_c + n_n)
se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_c + 1 / n_n))
z = (i_c / n_c - i_n / n_n) / se
print(f"\n  Test de proporciones (fuente auditable): z = {z:.2f}  "
      f"-> {'SIGNIFICATIVO' if abs(z) > 1.96 else 'NO significativo (p > 0.05)'}")
print(f"  n incidentes en cronicos: {i_c} sobre {n_c} empleado-mes")

print("\n### VEREDICTO")
if abs(z) > 1.96:
    print("  Las dos fuentes coinciden: la sobrecarga cronica SI eleva el riesgo de accidente.")
else:
    print("  Las fuentes DISCREPAN. El 3,7x del panel no se sostiene con la fuente auditable.")
    print("  Con n tan chico no se puede afirmar que la sobrecarga cronica cause accidentes.")
    print("  Nivel de evidencia: EXPLORATORIO. Requiere validacion antes de justificar inversion.")
