# -*- coding: utf-8 -*-
"""Calidad de datos: encoding, granularidad, consistencia interna, outliers."""
import pandas as pd, numpy as np
from pathlib import Path
RAW = Path(r"C:\Users\Dell\Agus\Nivii AI\02_datos\01_Originales")

# --- 1. Encoding test ---
print("### 1. ENCODING")
for enc in ["utf-8", "latin-1", "cp1252"]:
    try:
        t = pd.read_csv(RAW/"empleados_mensual.csv", encoding=enc, nrows=5, low_memory=False)
        print(f"  {enc:10s} OK -> puesto ejemplo: {t['puesto'].iloc[0]!r}")
    except Exception as e:
        print(f"  {enc:10s} FALLA: {type(e).__name__}")

emp = pd.read_csv(RAW/"empleados_mensual.csv", encoding="utf-8", low_memory=False)
evt = pd.read_csv(RAW/"eventos_rrhh.csv", encoding="utf-8", low_memory=False)
cap = pd.read_csv(RAW/"capacitaciones.csv", encoding="utf-8", low_memory=False)

print("\n### 2. GRANULARIDAD empleados_mensual")
print("  filas:", len(emp), "| empleados unicos:", emp.empleado_id.nunique(), "| meses:", emp.mes_snapshot.nunique())
dup = emp.duplicated(["empleado_id","mes_snapshot"]).sum()
print("  duplicados (empleado_id, mes_snapshot):", dup)
print("  rango meses:", emp.mes_snapshot.min(), "->", emp.mes_snapshot.max())
print("\n  headcount ACTIVO por mes:")
hc = emp.groupby("mes_snapshot").agg(filas=("empleado_id","size"), activos=("activo","sum"))
print(hc.to_string())

print("\n### 3. CONSISTENCIA INTERNA")
e = emp.copy()
e["mes_dt"] = pd.to_datetime(e.mes_snapshot)
e["fnac"] = pd.to_datetime(e.fecha_nacimiento, errors="coerce")
e["fing"] = pd.to_datetime(e.fecha_ingreso, errors="coerce")
e["fsal"] = pd.to_datetime(e.fecha_salida, errors="coerce")
edad_calc = ((e.mes_dt - e.fnac).dt.days/365.25).round(0)
print("  edad declarada vs calculada -> dif abs >1 anio:", int((abs(edad_calc - e.edad) > 1).sum()))
ant_calc = ((e.mes_dt.dt.year - e.fing.dt.year)*12 + (e.mes_dt.dt.month - e.fing.dt.month))
print("  antiguedad declarada vs calculada -> dif abs >1 mes:", int((abs(ant_calc - e.antiguedad_meses) > 1).sum()))
print("  activo=True PERO con fecha_salida pasada:", int(((e.activo) & (e.fsal.notna()) & (e.fsal < e.mes_dt)).sum()))
print("  activo=False SIN fecha_salida:", int(((~e.activo) & (e.fsal.isna())).sum()))
print("  ingreso posterior al snapshot:", int((e.fing > e.mes_dt).sum()))
print("  edad fuera de [16,75]:", int((~e.edad.between(16,75)).sum()), "| min/max:", e.edad.min(), e.edad.max())

print("\n### 4. CATEGORICAS CLAVE")
for c in ["genero","area","categoria_collar","turno_trabajo","motivo_salida","nivel_jerarquico"]:
    vc = emp[c].value_counts(dropna=False)
    print(f"  {c}: {dict(vc.head(12))}")

print("\n### 5. OUTLIERS / RANGOS NUMERICOS")
for c in ["salario_base_mensual","horas_extra","horas_trabajadas","edad","meses_hasta_jubilacion",
          "tasa_scrap_porcentaje","eficiencia_vs_target","rating_performance","dias_ausente"]:
    s = emp[c].dropna()
    print(f"  {c:28s} min={s.min():>12.2f} p50={s.median():>12.2f} p99={s.quantile(.99):>12.2f} max={s.max():>12.2f} neg={int((s<0).sum())}")

print("\n### 6. EVENTOS")
print("  tipo_evento:", dict(evt.tipo_evento.value_counts()))
print("  severidad:", dict(evt.severidad.value_counts(dropna=False)))
print("  rango fechas:", evt.fecha_evento.min(), "->", evt.fecha_evento.max())
print("  empleado_id de eventos NO presentes en empleados:", len(set(evt.empleado_id) - set(emp.empleado_id)))
print("  subtipos accidente:", dict(evt[evt.tipo_evento.str.contains('accid', case=False, na=False)].subtipo_evento.value_counts()))

print("\n### 7. CAPACITACIONES")
print("  categoria_training:", dict(cap.categoria_training.value_counts()))
print("  modalidad:", dict(cap.modalidad.value_counts()))
print("  completado:", dict(cap.completado.value_counts()))
print("  empleado_id de capacitaciones NO presentes en empleados:", len(set(cap.empleado_id) - set(emp.empleado_id)))
print("  rango fechas:", cap.fecha_inicio.min(), "->", cap.fecha_inicio.max())
print("  fecha_fin < fecha_inicio:", int((pd.to_datetime(cap.fecha_fin) < pd.to_datetime(cap.fecha_inicio)).sum()))
print("  calificacion_examen rango:", cap.calificacion_examen.min(), cap.calificacion_examen.max())
