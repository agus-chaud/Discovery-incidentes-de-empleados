# -*- coding: utf-8 -*-
"""Visualizaciones adicionales para conectar evidencia, riesgo y decision."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "06_resultados" / "Discovery" / "datos_transformados"
T = ROOT / "06_resultados" / "Discovery" / "tablas_soporte"
V = ROOT / "06_resultados" / "Discovery" / "visualizaciones"
V.mkdir(parents=True, exist_ok=True)

AZUL, ROJO, GRIS, VERDE, NARANJA = "#1f4e79", "#c0392b", "#95a5a6", "#27ae60", "#e67e22"
plt.rcParams.update({"figure.dpi": 140, "font.size": 10, "axes.grid": True, "grid.alpha": .25,
                     "axes.spines.top": False, "axes.spines.right": False})

panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
evt = pd.read_parquet(D / "eventos_limpio.parquet")
cap = pd.read_parquet(D / "capacitaciones_limpio.parquet")

def save(fig, name):
    fig.tight_layout()
    fig.savefig(V / name, bbox_inches="tight")
    plt.close(fig)
    print("  ->", name)

def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z ** 2 / n
    center = (p + z ** 2 / (2 * n)) / den
    margin = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / den
    return max(0, center - margin), min(1, center + margin)

# G8: Rotacion mensual, original versus periodo limpio.
sal = ult[ult.salio].copy()
sal["mes_salida"] = sal.fecha_salida.values.astype("datetime64[M]")
inicio = panel.mes_snapshot.min()
corte = inicio + pd.DateOffset(months=1)
hc = panel[panel.activo].groupby("mes_snapshot").empleado_id.nunique()
tasa_original = sal.groupby("mes_salida").size().reindex(hc.index, fill_value=0) / hc * 100
arrastre = set(sal[(sal.mes_salida == inicio) & (sal.meses_observados <= 1)].empleado_id)
sal_limpio = sal[~sal.empleado_id.isin(arrastre)]
tasa_limpia = (sal_limpio.groupby("mes_salida").size().reindex(hc.index, fill_value=0) / hc * 100).where(hc.index >= corte)
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(tasa_original.index, tasa_original, "o-", color=GRIS, label="Serie original", lw=2)
ax.plot(tasa_limpia.index, tasa_limpia, "o-", color=AZUL, label="Periodo limpio", lw=2.4)
ax.axvspan(inicio, corte, color=ROJO, alpha=.10, label="Mes de arrastre excluido")
ax.set(title="La rotación es plana, no descendente\n(corregido el arrastre de enero — DEC-017)", xlabel="Mes de salida", ylabel="Rotación mensual (%)")
ax.tick_params(axis="x", rotation=45); ax.legend(frameon=False, ncol=3)
save(fig, "G8_rotacion_original_vs_limpia.png")

# G9: Rotacion por area con intervalo de confianza.
ult_limpio = ult[~ult.empleado_id.isin(arrastre)]
rot = ult_limpio.groupby("area").agg(personas=("empleado_id", "size"), salidas=("salio", "sum"))
rot = rot[rot.personas >= 15].copy(); rot["tasa"] = rot.salidas / rot.personas * 100
intervalos = [wilson(k, n) for k, n in zip(rot.salidas, rot.personas)]
rot["lo"] = [lo * 100 for lo, _ in intervalos]; rot["hi"] = [hi * 100 for _, hi in intervalos]
rot = rot.sort_values("tasa"); base = ult_limpio.salio.mean() * 100
y = np.arange(len(rot)); destaca = rot.lo > base
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.barh(y, rot.tasa, color=np.where(destaca, ROJO, GRIS))
ax.errorbar(rot.tasa, y, xerr=[rot.tasa - rot.lo, rot.hi - rot.tasa], fmt="none", ecolor="#2c3e50", capsize=4)
ax.axvline(base, color=AZUL, ls="--", label=f"Promedio limpio: {base:.1f}%")
ax.set_yticks(y, rot.index); ax.set(xlabel="Rotación (%) con IC 95%", title="Mantenimiento Eléctrico rota peor que el promedio\n(34,8% vs 16,7% — única diferencia que se sostiene)")
ax.legend(frameon=False); save(fig, "G9_rotacion_area_ic95.png")

# G10: Distribucion de horas extra por area.
pa = panel[panel.activo].copy(); orden = pa.groupby("area").horas_extra.median().sort_values().index
datos = [pa.loc[pa.area == area, "horas_extra"].dropna() for area in orden]
fig, ax = plt.subplots(figsize=(11, 5.5))
bp = ax.boxplot(datos, tick_labels=orden, vert=False, patch_artist=True, showfliers=False)
for box in bp["boxes"]: box.set(facecolor=AZUL, alpha=.65)
for median in bp["medians"]: median.set(color=ROJO, linewidth=2)
ax.set(xlabel="Horas extra por empleado-mes", title="Seis áreas superan las 11 h extra/mes; las otras cinco no llegan a 6\n(Pintura: 12,2 h · Ingeniería: 3,5 h)")
save(fig, "G10_distribucion_horas_extra_area.png")

# G11: Incidentes por turno, en tasa por exposicion (DEC-007 / DEC-021).
# Antes mostraba area y severidad en conteo bruto: violaba DEC-007 (nunca comparar
# conteos entre grupos de tamano distinto) y no probaba el hallazgo de turno noche
# que sostiene el insight ejecutivo 3. Ahora lee la tabla persistida por
# 07_verif_incidentes_p5.py (P4_incidentes_por_turno.csv).
tt = pd.read_csv(T / "P4_incidentes_por_turno.csv").sort_values("tasa_x1000")
tasa_prom = tt.incidentes.sum() / tt.emp_meses.sum() * 1000
fig, ax = plt.subplots(figsize=(9.5, 5))
colores = np.where(tt.turno_trabajo == "Noche", ROJO, GRIS)
ax.barh(tt.turno_trabajo, tt.tasa_x1000, color=colores)
for y, tasa in enumerate(tt.tasa_x1000):
    ax.text(tasa + .2, y, f"{tasa:.1f}", va="center", fontsize=9)
ax.axvline(tasa_prom, color=AZUL, ls="--", label=f"Promedio: {tasa_prom:.1f} ×1.000 empleado-mes")
ax.set(xlabel="Incidentes cada 1.000 empleado-mes", title="El turno noche tiene 5,4x la tasa de mañana o tarde\n(56% de los incidentes y 74% de los días perdidos, sobre 45 casos)")
ax.legend(frameon=False); save(fig, "G11_incidentes_por_turno.png")

# G12: Capacitacion de seguridad versus incidentes.
inc = evt[evt.tipo_evento == "incidente_seguridad"].copy()
seg = cap[cap.categoria_training == "Seguridad"].groupby("area_empleado").agg(horas=("duracion_horas", "sum"))
dotacion = ult.groupby("area").empleado_id.size().rename("empleados")
incidentes = inc.groupby("area_empleado").size().rename("incidentes")
training = pd.concat([seg, dotacion, incidentes], axis=1).fillna(0)
training["horas_por_empleado"] = training.horas / training.empleados
training["incidentes_x100"] = training.incidentes / training.empleados * 100
fig, ax = plt.subplots(figsize=(8.5, 6))
ax.scatter(training.horas_por_empleado, training.incidentes_x100, s=110, color=AZUL, alpha=.8)
for area, row in training.iterrows(): ax.annotate(area, (row.horas_por_empleado, row.incidentes_x100), xytext=(6, 5), textcoords="offset points", fontsize=8)
ax.set(xlabel="Horas de capacitación en seguridad por empleado", ylabel="Incidentes por 100 empleados", title="Más capacitación coincide con más incidentes\n(se entrena después del accidente, no antes)")
ax.text(.01, .01, "Comparacion descriptiva: no prueba causalidad.", transform=ax.transAxes, fontsize=8, color=GRIS)
save(fig, "G12_capacitacion_seguridad_vs_incidentes.png")

# G13: Riesgo de sucesion por puesto.
activos = ult[~ult.salio].copy(); criticos = activos[activos.es_posicion_critica & (activos.meses_hasta_jubilacion <= 24)]
dotacion_puesto = activos.groupby(["area", "puesto"]).empleado_id.size().rename("dotacion")
sucesion = criticos.groupby(["area", "puesto"]).agg(en_riesgo=("empleado_id", "size"), antiguedad=("antiguedad_anios", "mean")).join(dotacion_puesto).reset_index()
sucesion["pct_riesgo"] = sucesion.en_riesgo / sucesion.dotacion * 100
sucesion = sucesion.sort_values(["pct_riesgo", "en_riesgo"], ascending=False).head(15)
fig, ax = plt.subplots(figsize=(10, 6.5))
scatter = ax.scatter(sucesion.dotacion, sucesion.pct_riesgo, s=150 + sucesion.antiguedad.fillna(0) * 70, c=sucesion.en_riesgo, cmap="Reds", alpha=.75, edgecolors="#7f1d1d")
for _, row in sucesion.iterrows(): ax.annotate(f"{row['puesto']}\n({row['area']})", (row.dotacion, row.pct_riesgo), xytext=(6, 5), textcoords="offset points", fontsize=7)
ax.set(xlabel="Dotación del puesto", ylabel="Personal crítico en riesgo a 24 meses (%)", title="Supervisor de Logística: único en el puesto\n(100% en riesgo, se jubila en 6 meses)")
fig.colorbar(scatter, ax=ax, label="Personas criticas en riesgo"); save(fig, "G13_riesgo_sucesion_por_puesto.png")

# G14: Business case por escenario.
bc = pd.read_csv(T / "BC_rango_retencion.csv")
columnas = ["reducir_15pct", "reducir_25pct", "reducir_40pct"]; etiquetas = ["Reducir 15%", "Reducir 25%", "Reducir 40%"]
x = np.arange(len(columnas)); width = .23
fig, ax = plt.subplots(figsize=(10, 5.5))
for i, (_, fila) in enumerate(bc.iterrows()):
    valores = [fila[col] for col in columnas]; barras = ax.bar(x + (i - 1) * width, valores, width, label=fila.escenario.capitalize())
    ax.bar_label(barras, labels=[f"${v:,.0f}" for v in valores], padding=3, fontsize=7, rotation=90)
ax.set_xticks(x, etiquetas); ax.set(ylabel="Ahorro anual estimado", title="El ahorro va de \\$23M a \\$195M según el escenario\n(no es una cifra única — ver los supuestos)")
ax.legend(frameon=False, title="Escenario"); ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value / 1_000_000:.0f}M"))
save(fig, "G14_business_case_escenarios.png")

print("Listo. Visualizaciones de decision en:", V)

