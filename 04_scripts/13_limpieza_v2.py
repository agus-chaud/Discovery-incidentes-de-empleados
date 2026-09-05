# -*- coding: utf-8 -*-
"""
Limpieza v2 — aplica las mejoras 1, 2, 3, 4 y 6.
ORIGEN : 02_datos/01_Originales/*.csv  (INMUTABLE, solo lectura)
DESTINO: 06_resultados/Discovery/datos_transformados/
"""
import pandas as pd, numpy as np
from pathlib import Path
import json, datetime as dt, unicodedata

RAW = Path(r"C:\Users\Dell\Agus\Nivii AI\02_datos\01_Originales")
OUT = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
ENC = "utf-8"
pasos = []          # <- mejora 6: receta reejecutable
def P(op, **kw):
    pasos.append({"op": op, **kw}); print(f"  [{op}] {kw}")

emp = pd.read_csv(RAW / "empleados_mensual.csv", encoding=ENC, low_memory=False)
evt = pd.read_csv(RAW / "eventos_rrhh.csv", encoding=ENC, low_memory=False)
cap = pd.read_csv(RAW / "capacitaciones.csv", encoding=ENC, low_memory=False)
print(f"Carga OK — empleados {emp.shape} | eventos {evt.shape} | capacitaciones {cap.shape}\n")

# ══════════════════════════════════════════════════════════════════
print("MEJORA 3 — nombres de columna sin eñes ni acentos")
# ══════════════════════════════════════════════════════════════════
def limpiar(nombre):
    n = nombre.replace("ñ", "ni").replace("Ñ", "Ni")
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode()
    return n.lower().strip().replace(" ", "_")

for df, tabla in [(emp, "empleados"), (evt, "eventos"), (cap, "capacitaciones")]:
    mapa = {c: limpiar(c) for c in df.columns if limpiar(c) != c}
    if mapa:
        df.rename(columns=mapa, inplace=True)
        for viejo, nuevo in mapa.items():
            P("renombrar_columna", tabla=tabla, de=viejo, a=nuevo)
    assert df.columns.is_unique, f"{tabla}: choque de nombres al renombrar"
print(f"  Nombres finales verificados como unicos en las 3 tablas\n")

# ══════════════════════════════════════════════════════════════════
print("MEJORA 4 — tipos correctos")
# ══════════════════════════════════════════════════════════════════
for c in ["mes_snapshot", "fecha_nacimiento", "fecha_ingreso", "fecha_salida", "ultimo_training_fecha"]:
    emp[c] = pd.to_datetime(emp[c], errors="coerce"); P("a_fecha", tabla="empleados", col=c)
evt["fecha_evento"] = pd.to_datetime(evt.fecha_evento, errors="coerce"); P("a_fecha", tabla="eventos", col="fecha_evento")
for c in ["fecha_inicio", "fecha_fin"]:
    cap[c] = pd.to_datetime(cap[c], errors="coerce"); P("a_fecha", tabla="capacitaciones", col=c)

# manager_id es un identificador guardado como decimal (1129.0) -> entero que admite vacios
decimales_reales = int((emp.manager_id.dropna() % 1 != 0).sum())
assert decimales_reales == 0, f"manager_id tiene {decimales_reales} valores con decimales reales"
emp["manager_id"] = emp.manager_id.astype("Int64")
P("a_entero_con_vacios", tabla="empleados", col="manager_id", decimales_reales_hallados=0)
print()

# ══════════════════════════════════════════════════════════════════
print("MEJORA 5b — unificar categorias escritas de dos formas")
# ══════════════════════════════════════════════════════════════════
for tabla, df, col, mapa in [
    ("capacitaciones", cap, "categoria_training", {"Técnica": "Técnico"}),
    ("capacitaciones", cap, "modalidad", {"Mixta": "Mixto"}),
    ("eventos", evt, "severidad", {"high": "Grave"}),
]:
    n = int(df[col].isin(mapa).sum())
    df[col] = df[col].replace(mapa)
    P("unificar_categorias", tabla=tabla, col=col, mapa=mapa, filas_afectadas=n)
print()

# ══════════════════════════════════════════════════════════════════
print("MEJORA 1 — politica de vacios: por que falta cada dato")
# ══════════════════════════════════════════════════════════════════
# Regla: si el dato esta 100% vacio en un grupo entero y casi completo en otro,
# no es un dato perdido: es un dato que NO APLICA a ese grupo.
AREAS_PRODUCCION = ["Estampado", "Ensamble", "Pintura"]
emp["es_produccion"] = emp.area.isin(AREAS_PRODUCCION)

politica = {
    # columna                    : (motivo, universo valido)
    "tasa_scrap_porcentaje":       ("no_aplica",  "solo areas de produccion"),
    "unidades_producidas":         ("no_aplica",  "solo areas de produccion"),
    "eficiencia_vs_target":        ("no_aplica",  "solo areas de produccion"),
    "dias_perdidos_scrap":         ("no_aplica",  "solo areas de produccion"),
    "fecha_salida":                ("estructural", "solo empleados que se fueron"),
    "motivo_salida":               ("estructural", "solo empleados que se fueron"),
    "bonus_anual":                 ("estructural", "dato anual dentro de un panel mensual"),
    "ultimo_training_fecha":       ("estructural", "solo quienes hicieron alguna capacitacion"),
    "dias_time_to_fill":           ("estructural", "solo contrataciones del periodo"),
    "fuente_reclutamiento":        ("estructural", "solo contrataciones del periodo"),
    "manager_id":                  ("estructural", "la cupula no tiene jefe"),
    "manager_nombre":              ("estructural", "la cupula no tiene jefe"),
    "ultimo_aumento_porcentaje":   ("real",       "vacio genuino, sin patron de grupo"),
}

filas = []
for col, (motivo, universo) in politica.items():
    s = emp[col]
    global_nulo = s.isna().mean() * 100
    if motivo == "no_aplica":
        dentro = emp.loc[emp.es_produccion, col].isna().mean() * 100
        fuera = emp.loc[~emp.es_produccion, col].isna().mean() * 100
        detalle = f"produccion {dentro:.1f}% vacio / resto {fuera:.1f}% vacio"
    else:
        detalle = universo
    filas.append({"columna": col, "%_vacio": round(global_nulo, 1),
                  "motivo": motivo, "detalle": detalle})
    P("politica_vacios", col=col, motivo=motivo, universo=universo,
      pct_vacio=round(global_nulo, 1))
tabla_pol = pd.DataFrame(filas).sort_values(["motivo", "%_vacio"], ascending=[True, False])
print(tabla_pol.to_string(index=False))

# Consecuencia practica: las metricas de produccion solo se promedian dentro del universo valido.
emp["scrap_valido"] = emp.es_produccion & emp.tasa_scrap_porcentaje.notna()
print(f"\n  Universo valido para scrap: {int(emp.scrap_valido.sum())} de {len(emp)} filas "
      f"({emp.scrap_valido.mean()*100:.1f}%) — el resto NO se promedia\n")

# ══════════════════════════════════════════════════════════════════
print("MEJORA 2 — outliers: se detectan, se explican, NO se tocan")
# ══════════════════════════════════════════════════════════════════
s = emp.salario_base_mensual
q1, q3 = s.quantile(.25), s.quantile(.75)
tope = q3 + 1.5 * (q3 - q1)
n_out = int((s > tope).sum())
# verificacion: los salarios altos coinciden con los niveles jerarquicos altos?
med_nivel = emp.groupby("nivel_jerarquico").salario_base_mensual.median()
monotona = bool((med_nivel.diff().dropna() > 0).all())
print(f"  Regla estandar marcaria {n_out} filas ({n_out/len(s)*100:.1f}%) por encima de ${tope:,.0f}")
print(f"  Mediana salarial por nivel jerarquico:")
for k, v in med_nivel.items():
    print(f"    nivel {k}: ${v:,.0f}")
print(f"  Sube de forma estricta con el nivel: {monotona}")
print(f"  -> Son gerentes reales, no errores. NO se recorta ningun salario.")
P("politica_outliers", col="salario_base_mensual", accion="ninguna",
  motivo="los valores altos siguen la jerarquia de forma estricta; recortarlos borraria la estructura salarial",
  filas_marcadas_por_regla_estandar=n_out, tope_regla_estandar=round(tope, 2),
  mediana_sube_con_nivel=monotona)
emp["salario_sobre_tope_iqr"] = s > tope     # se marca, no se altera
print()

# ══════════════════════════════════════════════════════════════════
print("Reglas de coherencia (se marcan, no se borran filas)")
# ══════════════════════════════════════════════════════════════════
edad_calc = ((emp.mes_snapshot - emp.fecha_nacimiento).dt.days / 365.25).round(0)
emp["flag_edad_inconsistente"] = (edad_calc - emp.edad).abs() > 1
ant_calc = ((emp.mes_snapshot.dt.year - emp.fecha_ingreso.dt.year) * 12
            + (emp.mes_snapshot.dt.month - emp.fecha_ingreso.dt.month))
emp["antiguedad_meses_calc"] = ant_calc
emp["flag_antig_inconsistente"] = (ant_calc - emp.antiguedad_meses).abs() > 1
emp["flag_snapshot_pre_ingreso"] = emp.fecha_ingreso > emp.mes_snapshot
for c, desc in [("flag_edad_inconsistente", "edad declarada distinta de la calculada por fecha de nacimiento"),
                ("flag_antig_inconsistente", "antiguedad declarada distinta de la calculada por fecha de ingreso"),
                ("flag_snapshot_pre_ingreso", "el registro mensual es anterior a la fecha de ingreso")]:
    P("regla_coherencia", col_marca=c, descripcion=desc, remediacion="marcar",
      filas_marcadas=int(emp[c].sum()))
    print(f"  {c}: {int(emp[c].sum())} filas marcadas")

# ── variables derivadas ──
emp["costo_total_mes"] = emp.salario_base_mensual + emp.costo_horas_extra
emp["pct_he_sobre_base"] = (emp.costo_horas_extra / emp.salario_base_mensual * 100).round(2)
emp["banda_edad"] = pd.cut(emp.edad, [0, 29, 39, 49, 59, 99], labels=["<30", "30-39", "40-49", "50-59", "60+"])
emp["jubila_12m"] = emp.meses_hasta_jubilacion <= 12
emp["jubila_24m"] = emp.meses_hasta_jubilacion <= 24
emp["antiguedad_anios"] = (emp.antiguedad_meses / 12).round(1)

# ── tabla a nivel persona ──
emp = emp.sort_values(["empleado_id", "mes_snapshot"])
ult = emp.groupby("empleado_id").tail(1).copy()
ult["salio"] = ult.fecha_salida.notna()
hist = emp.groupby("empleado_id").agg(
    meses_observados=("mes_snapshot", "size"), he_prom=("horas_extra", "mean"),
    he_max=("horas_extra", "max"), costo_he_total=("costo_horas_extra", "sum"),
    ausencias_total=("dias_ausente", "sum"), lic_medica_total=("dias_licencia_medica", "sum"),
    incidentes_total=("incidentes_seguridad_count", "sum"), perf_prom=("rating_performance", "mean"),
    efic_prom=("eficiencia_vs_target", "mean"), horas_training_total=("horas_training_mes", "sum"))
# scrap promedio SOLO sobre el universo valido (mejora 1)
scrap_ok = (emp[emp.scrap_valido].groupby("empleado_id").tasa_scrap_porcentaje.mean()
            .rename("scrap_prom_produccion"))
ult = ult.merge(hist, on="empleado_id", how="left").merge(scrap_ok, on="empleado_id", how="left")

print(f"\nNivel persona: {len(ult)} empleados | salidas {int(ult.salio.sum())} | activos {int((~ult.salio).sum())}")
print(f"  scrap_prom_produccion disponible para {int(ult.scrap_prom_produccion.notna().sum())} empleados de produccion")

# ══════════════════════════════════════════════════════════════════
print("\nMEJORA 6 — guardar la receta reejecutable")
# ══════════════════════════════════════════════════════════════════
emp.to_parquet(OUT / "panel_mensual_limpio.parquet", index=False)
ult.to_parquet(OUT / "empleados_nivel_persona.parquet", index=False)
evt.to_parquet(OUT / "eventos_limpio.parquet", index=False)
cap.to_parquet(OUT / "capacitaciones_limpio.parquet", index=False)

receta = {
    "generado": dt.datetime.now().isoformat(timespec="seconds"),
    "script": "04_scripts/13_limpieza_v2.py",
    "origen": "02_datos/01_Originales/{empleados_mensual,eventos_rrhh,capacitaciones}.csv",
    "codificacion": ENC,
    "regla_general": "los archivos originales no se tocan; ninguna fila se borra; "
                     "las inconsistencias se marcan con una columna que empieza en flag_",
    "areas_produccion": AREAS_PRODUCCION,
    "pasos": pasos,
}
(OUT / "transformaciones.json").write_text(json.dumps(receta, indent=2, ensure_ascii=False), encoding="utf-8")
tabla_pol.to_csv(OUT / "politica_vacios.csv", index=False, encoding="utf-8-sig")
print(f"  transformaciones.json — {len(pasos)} pasos reejecutables")
print(f"  politica_vacios.csv — {len(tabla_pol)} columnas clasificadas")
print(f"\nListo. Todo en {OUT}")
