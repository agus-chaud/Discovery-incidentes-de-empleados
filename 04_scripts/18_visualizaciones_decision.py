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

# G12: cobertura de la capacitacion de seguridad, y su relacion temporal con los
# incidentes. Antes era un scatter de horas de training vs incidentes por area,
# titulado "mas capacitacion coincide con mas incidentes (se entrena despues del
# accidente, no antes)". Dos problemas independientes: (1) la correlacion no se
# distingue de cero (r=0,394, p=0,260 sobre 10 areas); (2) el calculo agregaba
# totales de todo el periodo y nunca comparaba fechas, asi que el titulo afirmaba
# una temporalidad que el codigo no medía. El cruce temporal si se podia hacer con
# los archivos que ya existen, y da vuelta la conclusion: son 4 casos de 45.
inc = evt[evt.tipo_evento == "incidente_seguridad"].copy()
seg = cap[cap.categoria_training == "Seguridad"]

previa = posterior = ninguna = 0
for _, r in inc.iterrows():
    t_emp = seg[seg.empleado_id == r.empleado_id]
    hay_previa = bool((t_emp.fecha_fin <= r.fecha_evento).any())
    hay_post = bool((t_emp.fecha_inicio > r.fecha_evento).any())
    previa += hay_previa
    posterior += hay_post
    ninguna += not (hay_previa or hay_post)

universo = set(panel[panel.activo].empleado_id)
accidentados = set(inc.empleado_id) & universo
capacitados = set(seg.empleado_id)
pct_acc = len(accidentados & capacitados) / len(accidentados) * 100
pct_no = len(((universo - accidentados) & capacitados)) / len(universo - accidentados) * 100
pct_univ = len(universo & capacitados) / len(universo) * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5), gridspec_kw={"width_ratios": [1.25, 1]})

etiquetas = ["Sin ninguna\ncapacitación", "Con capacitación\nPREVIA al hecho", "Con capacitación\nPOSTERIOR al hecho"]
valores = [ninguna, previa, posterior]
barras = ax1.bar(etiquetas, valores, color=[ROJO, GRIS, GRIS])
ax1.bar_label(barras, labels=[f"{v}\n({v / len(inc) * 100:.0f}%)" for v in valores], padding=4, fontsize=10)
ax1.set(ylabel="Incidentes", ylim=(0, max(valores) * 1.28),
        title=f"De los {len(inc)} incidentes auditables")
ax1.tick_params(axis="x", labelsize=9)

grupos = ["Accidentados", "No accidentados"]
pcts = [pct_acc, pct_no]
b2 = ax2.bar(grupos, pcts, color=[ROJO, GRIS], width=.55)
ax2.bar_label(b2, labels=[f"{p:.1f}%" for p in pcts], padding=4, fontsize=11)
ax2.axhline(pct_univ, color=AZUL, ls="--", lw=1.5, label=f"Toda la empresa: {pct_univ:.1f}%")
ax2.set(ylabel="% con capacitación en seguridad", ylim=(0, max(pcts) * 1.6),
        title="Cobertura de la capacitación")
ax2.legend(frameon=False, fontsize=9, loc="upper left")
ax2.text(.5, -.14, "Fisher exacto bilateral: p = 0,683 — la diferencia no se distingue del azar",
         transform=ax2.transAxes, ha="center", fontsize=8.5, color=GRIS)

fig.suptitle("La capacitación en seguridad cubre al 19,3% de la gente, y no llega a quien se accidenta",
             fontsize=13, y=1.02)
save(fig, "G12_cobertura_capacitacion_seguridad.png")

# G13: tarjeta de alerta de sucesion. Antes era un scatter de hasta 15 puestos.
# El cruce del indice propio de criticidad (DEC-006) con proximidad a jubilacion
# devuelve un unico puesto: un grafico de dispersion con un punto sugiere una
# distribucion que no existe y obliga a la audiencia a buscar un patron donde hay
# un hecho puntual. Con un caso no hay patron; hay una alerta.
activos = ult[~ult.salio].copy()
if not {"score_crit", "es_critico_indice"}.issubset(activos.columns):
    raise ValueError("Faltan columnas del indice de criticidad; ejecutar 13_limpieza_v2.py antes de generar G13.")
criticos = activos[activos.es_critico_indice & (activos.meses_hasta_jubilacion <= 24)]
dotacion_puesto = activos.groupby(["area", "puesto"]).empleado_id.size().rename("dotacion")
sucesion = (criticos.groupby(["area", "puesto"])
            .agg(en_riesgo=("empleado_id", "size"))
            .join(dotacion_puesto).reset_index())
sucesion["sucesores"] = sucesion.dotacion - sucesion.en_riesgo
sucesion = sucesion.sort_values(["sucesores", "dotacion"]).head(4)

n = len(sucesion)
fig, axes = plt.subplots(n, 1, figsize=(9, 2.5 * n + .6), squeeze=False)
for ax, (_, row) in zip(axes.ravel(), sucesion.iterrows()):
    ax.axis("off")
    critico = row.sucesores == 0
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor="#fdf2f2" if critico else "#f4f6f7",
                               edgecolor=ROJO if critico else GRIS, linewidth=2.5))
    ax.text(.035, .78, f"{'⚠  ' if critico else ''}{row.puesto}", transform=ax.transAxes,
            fontsize=15, fontweight="bold", color=ROJO if critico else "#2c3e50")
    ax.text(.035, .60, f"Área: {row.area}", transform=ax.transAxes, fontsize=10.5, color="#2c3e50")
    for i, (etiqueta, valor) in enumerate([("Dotación del puesto", row.dotacion),
                                           ("En riesgo a 24 meses", row.en_riesgo),
                                           ("Sucesores potenciales", row.sucesores)]):
        x = .06 + i * .31
        ax.text(x, .30, str(int(valor)), transform=ax.transAxes, fontsize=26, fontweight="bold",
                color=ROJO if (critico and i == 2) else "#2c3e50")
        ax.text(x, .15, etiqueta, transform=ax.transAxes, fontsize=9, color=GRIS)
    if critico:
        ax.text(.97, .74, "Sin cobertura", transform=ax.transAxes, fontsize=11, color=ROJO,
                ha="right", va="center", fontweight="bold")
        ax.text(.035, .045, "Si esa persona sale, no hay nadie en el puesto y nadie preparándose para ocuparlo.",
                transform=ax.transAxes, fontsize=9.5, color=ROJO, va="bottom", style="italic")

fig.suptitle("Riesgo de sucesión: punto de falla unipersonal\n"
             "(índice propio de criticidad, score ≥ 2 — DEC-006; el flag es_posicion_critica no se usa)",
             fontsize=12.5, y=.99)
save(fig, "G13_alerta_sucesion.png")

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

