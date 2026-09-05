# -*- coding: utf-8 -*-
"""
Limpieza trazable TechnoStamp.
ORIGEN : 02_datos/01_Originales/*.csv  (INMUTABLE, solo lectura)
DESTINO: 06_resultados/Discovery/datos_transformados/*.parquet
PROPOSITO: base reproducible para el Discovery de RRHH.
"""
import pandas as pd, numpy as np
from pathlib import Path
import json, datetime as dt

RAW = Path(r"C:\Users\Dell\Agus\Nivii AI\02_datos\01_Originales")
OUT = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
ENC = "utf-8"          # VERIFICADO por hexdump: bytes c3 a9 = UTF-8. latin-1 producia mojibake.
log = []

def L(msg):
    log.append(msg); print(msg)

emp = pd.read_csv(RAW/"empleados_mensual.csv", encoding=ENC, low_memory=False)
evt = pd.read_csv(RAW/"eventos_rrhh.csv",      encoding=ENC, low_memory=False)
cap = pd.read_csv(RAW/"capacitaciones.csv",    encoding=ENC, low_memory=False)
L(f"[carga] encoding={ENC} | emp={emp.shape} evt={evt.shape} cap={cap.shape}")

# ---------- fechas ----------
for c in ["mes_snapshot","fecha_nacimiento","fecha_ingreso","fecha_salida","ultimo_training_fecha"]:
    emp[c] = pd.to_datetime(emp[c], errors="coerce")
evt["fecha_evento"] = pd.to_datetime(evt.fecha_evento, errors="coerce")
for c in ["fecha_inicio","fecha_fin"]:
    cap[c] = pd.to_datetime(cap[c], errors="coerce")

# ---------- normalizacion de categorias sucias ----------
cap["categoria_training"] = cap.categoria_training.replace({"Técnica":"Técnico"})
cap["modalidad"]          = cap.modalidad.replace({"Mixta":"Mixto"})
evt["severidad"]          = evt.severidad.replace({"high":"Grave"})   # 3 casos en ingles
L("[norm] capacitaciones: 'Técnica'->'Técnico' (21) | modalidad 'Mixta'->'Mixto' (19) | severidad 'high'->'Grave' (3)")

# ---------- flags de calidad (NO se borran filas: se marcan) ----------
edad_calc = ((emp.mes_snapshot - emp.fecha_nacimiento).dt.days/365.25).round(0)
emp["flag_edad_inconsistente"] = (edad_calc - emp.edad).abs() > 1
ant_calc = ((emp.mes_snapshot.dt.year - emp.fecha_ingreso.dt.year)*12
            + (emp.mes_snapshot.dt.month - emp.fecha_ingreso.dt.month))
emp["antiguedad_meses_calc"]        = ant_calc
emp["flag_antig_inconsistente"]     = (ant_calc - emp.antiguedad_meses).abs() > 1
emp["flag_snapshot_pre_ingreso"]    = emp.fecha_ingreso > emp.mes_snapshot
L(f"[flags] edad inconsistente={int(emp.flag_edad_inconsistente.sum())} | "
  f"antiguedad inconsistente={int(emp.flag_antig_inconsistente.sum())} | "
  f"snapshot previo al ingreso={int(emp.flag_snapshot_pre_ingreso.sum())}")

# ---------- variables derivadas explicables ----------
emp["costo_total_mes"]   = emp.salario_base_mensual + emp.costo_horas_extra
emp["pct_he_sobre_base"] = (emp.costo_horas_extra / emp.salario_base_mensual * 100).round(2)
emp["he_ratio_horas"]    = (emp.horas_extra / emp.horas_trabajadas * 100).round(2)
emp["banda_edad"]        = pd.cut(emp.edad, [0,29,39,49,59,99],
                                  labels=["<30","30-39","40-49","50-59","60+"])
emp["jubila_12m"]        = emp.meses_hasta_jubilacion <= 12
emp["jubila_24m"]        = emp.meses_hasta_jubilacion <= 24
emp["antiguedad_anios"]  = (emp.antiguedad_meses/12).round(1)

# ---------- tabla NIVEL EMPLEADO (ultimo snapshot de cada uno) ----------
emp = emp.sort_values(["empleado_id","mes_snapshot"])
ult = emp.groupby("empleado_id").tail(1).copy()
ult["salio"] = ult.fecha_salida.notna()
# metricas promedio del historial de cada empleado
hist = emp.groupby("empleado_id").agg(
    meses_observados      = ("mes_snapshot","size"),
    he_prom               = ("horas_extra","mean"),
    he_max                = ("horas_extra","max"),
    costo_he_total        = ("costo_horas_extra","sum"),
    ausencias_total       = ("dias_ausente","sum"),
    lic_medica_total      = ("dias_licencia_medica","sum"),
    incidentes_total      = ("incidentes_seguridad_count","sum"),
    perf_prom             = ("rating_performance","mean"),
    scrap_prom            = ("tasa_scrap_porcentaje","mean"),
    efic_prom             = ("eficiencia_vs_target","mean"),
    horas_training_total  = ("horas_training_mes","sum"),
)
ult = ult.merge(hist, on="empleado_id", how="left")
L(f"[nivel empleado] {len(ult)} empleados | salidas registradas={int(ult.salio.sum())} | activos al final={int((~ult.salio).sum())}")

# ---------- persistir ----------
emp.to_parquet(OUT/"panel_mensual_limpio.parquet", index=False)
ult.to_parquet(OUT/"empleados_nivel_persona.parquet", index=False)
evt.to_parquet(OUT/"eventos_limpio.parquet", index=False)
cap.to_parquet(OUT/"capacitaciones_limpio.parquet", index=False)

linaje = {
    "generado": dt.datetime.now().isoformat(timespec="seconds"),
    "script": "04_scripts/03_limpieza.py",
    "origen": "02_datos/01_Originales/{empleados_mensual,eventos_rrhh,capacitaciones}.csv",
    "encoding": ENC,
    "transformaciones": log,
    "regla": "raw inmutable; ninguna fila eliminada; inconsistencias marcadas con flag_*",
}
(OUT/"_linaje.json").write_text(json.dumps(linaje, indent=2, ensure_ascii=False), encoding="utf-8")
L(f"[ok] persistido en {OUT}")
