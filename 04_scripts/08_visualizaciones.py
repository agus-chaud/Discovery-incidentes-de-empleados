# -*- coding: utf-8 -*-
"""Visualizaciones del Discovery TechnoStamp."""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "06_resultados" / "Discovery" / "datos_transformados"
V = ROOT / "06_resultados" / "Discovery" / "visualizaciones"
V.mkdir(parents=True, exist_ok=True)

AZUL, ROJO, GRIS, VERDE, NARANJA = "#1f4e79", "#c0392b", "#95a5a6", "#27ae60", "#e67e22"
plt.rcParams.update({"figure.dpi": 130, "font.size": 9, "axes.grid": True,
                     "grid.alpha": .25, "axes.spines.top": False, "axes.spines.right": False})

panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
evt = pd.read_parquet(D / "eventos_limpio.parquet")
cap = pd.read_parquet(D / "capacitaciones_limpio.parquet")
pa = panel[panel.activo].copy()
act = ult[~ult.salio].copy()
inc = evt[evt.tipo_evento == "incidente_seguridad"].copy()
inc["mes"] = inc.fecha_evento.values.astype("datetime64[M]")
inc["k"] = inc.empleado_id.astype(str) + "|" + inc.mes.astype(str)
panel["k"] = panel.empleado_id.astype(str) + "|" + panel.mes_snapshot.astype(str)
inc = inc.merge(panel[["k", "turno_trabajo", "antiguedad_meses"]], on="k", how="left")

def save(fig, name):
    fig.tight_layout(); fig.savefig(V / name, bbox_inches="tight"); plt.close(fig)
    print("  ->", name)

# ---------- G1: Piramide etaria ----------
fig, ax = plt.subplots(figsize=(7, 3.6))
pir = act.groupby(["banda_edad", "genero"], observed=True).size().unstack(fill_value=0)
y = np.arange(len(pir))
ax.barh(y, -pir.get("M", 0), color=AZUL, label="Masculino")
ax.barh(y, pir.get("F", 0), color=NARANJA, label="Femenino")
ax.set_yticks(y); ax.set_yticklabels(pir.index)
ax.set_xticks([-250, -150, -50, 0, 50, 150]); ax.set_xticklabels([250, 150, 50, 0, 50, 150])
for i, (m, f) in enumerate(zip(pir.get("M", 0), pir.get("F", 0))):
    ax.text(-m - 8, i, str(m), va="center", ha="right", fontsize=8)
    ax.text(f + 8, i, str(f), va="center", fontsize=8)
ax.axvline(0, color="k", lw=.8)
ax.set_title("Dotación activa por edad y género (mayo 2025)", fontweight="bold")
ax.legend(loc="lower right", frameon=False)
save(fig, "G1_piramide_etaria.png")

# ---------- G2: Genero por area + embudo jerarquico ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
g = pd.crosstab(act.area, act.genero)
g["pct_F"] = (g.get("F", 0) / g.sum(1) * 100).round(1)
g = g.sort_values("pct_F")
cols = [ROJO if v < 33 else (NARANJA if v < 40 else VERDE) for v in g.pct_F]
a1.barh(g.index, g.pct_F, color=cols)
a1.axvline(37.0, color=AZUL, ls="--", lw=1.4, label="Promedio empresa 37,0%")
for i, v in enumerate(g.pct_F): a1.text(v + .6, i, f"{v:.0f}%", va="center", fontsize=8)
a1.set_xlabel("% mujeres"); a1.set_title("Representación femenina por área", fontweight="bold")
a1.legend(frameon=False, fontsize=8); a1.set_xlim(0, 55)

n = pd.crosstab(act.nivel_jerarquico, act.genero)
n["pct_F"] = (n.get("F", 0) / n.sum(1) * 100).round(1)
a2.plot(n.index, n.pct_F, "o-", color=ROJO, lw=2.2, ms=9)
for x, v, tot in zip(n.index, n.pct_F, n.get("F", 0) + n.get("M", 0)):
    a2.annotate(f"{v:.0f}%\n(n={tot})", (x, v), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=8)
a2.axhline(37.0, color=GRIS, ls="--", label="Dotación total 37,0%")
a2.set_xticks(n.index); a2.set_xlabel("Nivel jerárquico"); a2.set_ylabel("% mujeres")
a2.set_ylim(15, 55); a2.set_title("Representación femenina por nivel jerárquico", fontweight="bold")
a2.legend(frameon=False, fontsize=8)
save(fig, "G2_genero_area_y_nivel.png")

# ---------- G3: Brecha salarial ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8))
lv, gaps, ns = [], [], []
for l, sub in act.groupby("nivel_jerarquico"):
    f, m = sub[sub.genero == "F"], sub[sub.genero == "M"]
    if len(f) >= 5 and len(m) >= 5:
        lv.append(f"Nivel {l}"); gaps.append((1 - f.salario_base_mensual.mean() / m.salario_base_mensual.mean()) * 100)
        ns.append(f"nF={len(f)} nM={len(m)}")
a1.barh(lv, gaps, color=[VERDE if abs(x) < 2 else NARANJA for x in gaps])
a1.axvline(0, color="k", lw=1)
a1.axvspan(-2, 2, color=VERDE, alpha=.10)
for i, (v, t) in enumerate(zip(gaps, ns)):
    a1.text(v + (.15 if v >= 0 else -.15), i, f"{v:+.1f}%  ({t})", va="center",
            ha="left" if v >= 0 else "right", fontsize=8)
a1.set_xlim(-3, 3); a1.set_xlabel("Brecha salarial F vs M (%)  —  positivo = M cobra más")
a1.set_title("Brecha por nivel: dentro de ±2% (banda verde)", fontweight="bold")

labels = ["Brecha\ncruda", "Ajustada por nivel,\náreas, antigüedad,\nedad y performance"]
vals = [0.9, 0.02]
a2.bar(labels, vals, color=[GRIS, VERDE], width=.55)
for i, v in enumerate(vals): a2.text(i, v + .06, f"{v:.2f}%", ha="center", fontweight="bold")
a2.axhline(0, color="k", lw=1); a2.set_ylim(0, 1.5); a2.set_ylabel("Brecha (%)")
a2.set_title("Regresión OLS: efecto género no significativo\n(t = -0,03 · R² = 0,865 · n = 562)", fontweight="bold")
save(fig, "G3_brecha_salarial.png")

# ---------- G4: Horas extra ----------
fig, ((a1, a2), (a3, a4)) = plt.subplots(2, 2, figsize=(11.5, 7))
ev = pa.groupby("mes_snapshot").horas_extra.mean()
a1.plot(ev.index, ev.values, "o-", color=ROJO, lw=2, ms=4)
z = np.polyfit(range(len(ev)), ev.values, 1)
a1.plot(ev.index, np.poly1d(z)(range(len(ev))), "--", color=AZUL, lw=1.6,
        label=f"Tendencia: +{z[0]*12:.2f} h/año")
a1.set_ylabel("Horas extra promedio/mes"); a1.set_ylim(0, 12)
a1.set_title("HE estructural, no un pico: 17 meses sostenidos", fontweight="bold")
a1.legend(frameon=False, fontsize=8); a1.tick_params(axis="x", rotation=45)

ar = pa.groupby("area").horas_extra.mean().sort_values()
a2.barh(ar.index, ar.values, color=[ROJO if v > 11 else (NARANJA if v > 5 else GRIS) for v in ar.values])
for i, v in enumerate(ar.values): a2.text(v + .15, i, f"{v:.1f}", va="center", fontsize=8)
a2.set_xlabel("Horas extra promedio/mes"); a2.set_title("Horas extra promedio", fontweight="bold")

he_emp = pa.groupby("empleado_id").costo_horas_extra.sum().sort_values(ascending=False)
cum = (he_emp.cumsum() / he_emp.sum() * 100).values
x = np.arange(1, len(cum) + 1) / len(cum) * 100
a3.plot(x, cum, color=AZUL, lw=2.2)
a3.plot([0, 100], [0, 100], "--", color=GRIS, lw=1.2, label="Distribución uniforme")
a3.fill_between(x, cum, x, color=AZUL, alpha=.12)
a3.scatter([20], [cum[int(len(cum) * .2)]], color=ROJO, zorder=5, s=45)
a3.annotate(f"Top 20% = {cum[int(len(cum)*.2)]:.0f}% del costo\n(si fuera concentrado sería >60%)",
            (20, cum[int(len(cum) * .2)]), textcoords="offset points", xytext=(12, -32), fontsize=8, color=ROJO)
a3.set_xlabel("% de empleados (ordenados por costo HE)"); a3.set_ylabel("% del costo acumulado")
a3.set_title("El problema de HE es SISTÉMICO", fontweight="bold")
a3.legend(frameon=False, fontsize=8)

t = pa.groupby("turno_trabajo").horas_extra.mean().sort_values()
a4.barh(t.index, t.values, color=[ROJO if v > 11.5 else (NARANJA if v > 5 else GRIS) for v in t.values])
for i, v in enumerate(t.values): a4.text(v + .15, i, f"{v:.1f}", va="center", fontsize=8)
a4.set_xlabel("Horas extra promedio/mes"); a4.set_title("Noche lidera en horas extra", fontweight="bold")
save(fig, "G4_horas_extra.png")

# ---------- G5: Seguridad ----------
fig, ((a1, a2), (a3, a4), (a5, a6)) = plt.subplots(3, 2, figsize=(11.5, 11))

def _poisson_ci(count, exposure, scale=1000, z=1.96):
    """Approximate Poisson rate CI; exposure is employee-months."""
    rate = count / exposure * scale
    margin = z * np.sqrt(count) / exposure * scale if count else 0
    return max(0, rate - margin), rate + margin

expo = pa.groupby("turno_trabajo").size()
it = inc.groupby("turno_trabajo").size()
tt = (it / expo * 1000).dropna().sort_values()
a1.barh(tt.index, tt.values, color=[ROJO if v > 8 else GRIS for v in tt.values])
for i, (turno, v) in enumerate(tt.items()):
    n = int(it.get(turno, 0)); lo, hi = _poisson_ci(n, int(expo[turno]))
    a1.errorbar(v, i, xerr=[[v - lo], [hi - v]], fmt="none", ecolor="#2c3e50", capsize=3)
    a1.text(hi + .2, i, f"{v:.1f} (n={n})", va="center", fontsize=8, fontweight="bold")
a1.set_xlabel("Incidentes cada 1.000 empleados-mes")
a1.set_title("Tasa observada de incidentes por turno\n(barras: tasa; lineas: IC aproximado)", fontweight="bold")

bins, labs = [-1, 6, 12, 24, 60, 120, 999], ["0-6m", "6-12m", "1-2a", "2-5a", "5-10a", "10a+"]
pa["ba"] = pd.cut(pa.antiguedad_meses, bins, labels=labs)
inc["ba"] = pd.cut(inc.antiguedad_meses, bins, labels=labs)
e2 = pa.groupby("ba", observed=True).size()
i2 = inc.groupby("ba", observed=True).size().reindex(e2.index).fillna(0)
r2 = (i2 / e2 * 1000)
a2.bar(range(len(r2)), r2.values, color=[GRIS if v < 5 else ROJO for v in r2.values])
a2.set_xticks(range(len(r2))); a2.set_xticklabels(r2.index)
for i, (banda, v) in enumerate(r2.items()):
    n = int(i2.get(banda, 0)); lo, hi = _poisson_ci(n, int(e2.iloc[i]))
    a2.errorbar(i, v, yerr=[[v - lo], [hi - v]], fmt="none", ecolor="#2c3e50", capsize=3)
    a2.text(i, hi + .15, f"{v:.1f} (n={n})", ha="center", fontsize=8, fontweight="bold")
a2.set_ylabel("Incidentes cada 1.000 empleados-mes"); a2.set_xlabel("Antiguedad")
a2.set_title("Tasa observada por antiguedad\n(cero incidentes auditables en los primeros 12 meses)", fontweight="bold")

sev = inc.groupby("severidad").agg(n=("evento_id", "size"), dias=("dias_perdidos", "sum")).reindex(["Leve", "Moderado", "Grave"])
a3.bar(sev.index, sev.n, color=GRIS)
for i, v in enumerate(sev.n): a3.text(i, v + 1, f"{int(v)}", ha="center", fontsize=9, fontweight="bold")
a3.set_ylabel("Cantidad de incidentes")
a3.set_title("Frecuencia de incidentes por severidad", fontweight="bold")

a4.bar(sev.index, sev.dias, color=ROJO)
for i, v in enumerate(sev.dias): a4.text(i, v + 3, f"{int(v)}", ha="center", fontsize=9, fontweight="bold")
a4.set_ylabel("Dias perdidos")
a4.set_title("Impacto por severidad: dias perdidos", fontweight="bold")

st = inc.groupby("subtipo_evento").agg(n=("evento_id", "size"), dias=("dias_perdidos", "sum")).sort_values("dias")
a5.barh(st.index, st.dias, color=[ROJO if v > 30 else GRIS for v in st.dias])
for i, (d, n_) in enumerate(zip(st.dias, st.n)): a5.text(d + .8, i, f"{int(d)} dias (n={n_})", va="center", fontsize=8)
a5.set_xlabel("Dias perdidos"); a5.set_xlim(0, 62)
a5.set_title("Dias perdidos por subtipo (n = incidentes)", fontweight="bold")

a6.axis("off")
a6.text(.02, .85, "Lectura", fontsize=11, fontweight="bold")
a6.text(.02, .67, "La frecuencia y el impacto no son lo mismo.\nLos incidentes graves son pocos, pero concentran\nla mayor parte de los dias perdidos.", fontsize=10, va="top")
a6.text(.02, .37, "Fuente: eventos_rrhh (45 incidentes auditables).\nLas tasas son descriptivas; no prueban causalidad.", fontsize=9, va="top", color="#555555")
save(fig, "G5_seguridad.png")

# ---------- G6: Rotacion ----------
fig, (a1, a2, a4) = plt.subplots(1, 3, figsize=(15, 4.8))
# periodo limpio: excluye las 19 salidas de arrastre de enero 2024 (DEC-017)
_s = ult[ult.salio].copy()
_s["mes_salida"] = _s.fecha_salida.values.astype("datetime64[M]")
_arr = set(_s[_s.mes_salida == panel.mes_snapshot.min()].empleado_id)
ultc = ult[~ult.empleado_id.isin(_arr)]
BASE = ultc.salio.mean() * 100

def _wilson(k, n, z=1.96):
    p = k / n; den = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / den
    m = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    return max(0, c - m) * 100, min(1, c + m) * 100

ra = ultc.groupby("area").agg(total=("empleado_id", "size"), sal=("salio", "sum"))
ra = ra[ra.total >= 15].copy()
ra["pct"] = ra.sal / ra.total * 100
ic = [_wilson(k, n) for k, n in zip(ra.sal, ra.total)]
ra["lo"], ra["hi"] = [i[0] for i in ic], [i[1] for i in ic]
ra["destaca"] = ra.lo > BASE          # solo si el rango entero supera al promedio
ra = ra.sort_values("pct")
y = np.arange(len(ra))
a1.barh(y, ra.pct, color=[ROJO if d else GRIS for d in ra.destaca])
a1.errorbar(ra.pct, y, xerr=[ra.pct - ra.lo, ra.hi - ra.pct], fmt="none",
            ecolor="#2c3e50", elinewidth=1.3, capsize=3.5)
a1.axvline(BASE, color=AZUL, ls="--", lw=1.4, label=f"Periodo limpio {BASE:.1f}%")
a1.set_yticks(y); a1.set_yticklabels(ra.index)
for i, (v, hi_, n_) in enumerate(zip(ra.pct, ra.hi, ra.total)):
    a1.text(hi_ + 1, i, f"{v:.0f}% (n={n_})", va="center", fontsize=7.5)
a1.set_xlabel("% rotación — la barra fina es el margen de error"); a1.set_xlim(0, 62)
a1.set_title("Solo Mantenimiento Eléctrico se distingue.\nEl resto se solapa con el promedio", fontweight="bold")
a1.legend(frameon=False, fontsize=8, loc="lower right")

mv = ultc[ultc.salio].motivo_salida.value_counts()
w, _ = a2.pie(mv.values, colors=[ROJO, NARANJA, GRIS, "#bdc3c7", "#d5dbdb"], startangle=90,
              wedgeprops={"edgecolor": "w", "linewidth": 1.5})
a2.legend(w, [f"{i} — {v} ({v/mv.sum()*100:.0f}%)" for i, v in mv.items()],
          loc="center left", bbox_to_anchor=(.98, .5), frameon=False, fontsize=8)
a2.set_title("67% son renuncias VOLUNTARIAS\n= la porción sobre la que se puede actuar", fontweight="bold")

sal = ultc[ultc.salio]
# No alcanza con contar salidas: si un tramo tiene mas personas, tendra
# naturalmente mas salidas aunque el riesgo individual sea igual. La barra
# muestra la tasa de salida dentro de cada tramo (salidas / personas).
bins_ant = [-1, 1, 2, 5, 8, 10, 999]
labs_ant = ["<1 ano", "1-2 anos", "2-5 anos", "5-8 anos", "8-10 anos", "10+ anos"]
ultc["tramo_antiguedad"] = pd.cut(ultc.antiguedad_anios, bins_ant, labels=labs_ant)
ant = ultc.groupby("tramo_antiguedad", observed=True).agg(
    personas=("empleado_id", "size"), salidas=("salio", "sum")
)
ant["pct"] = ant.salidas / ant.personas * 100
fig_ant, ant_ax = plt.subplots(figsize=(8.8, 4.8))
x_ant = np.arange(len(ant))
ant_ax.bar(x_ant, ant.pct, color=[ROJO if v == ant.pct.max() else AZUL for v in ant.pct], width=.62)
for i, (v, k, n) in enumerate(zip(ant.pct, ant.salidas, ant.personas)):
    ant_ax.text(i, v + 1.2, f"{v:.0f}%\n({int(k)}/{int(n)})",
            ha="center", va="bottom", fontsize=7.5)
ant_ax.axhline(BASE, color=GRIS, ls="--", lw=1.2, label=f"Promedio periodo {BASE:.1f}%")
ant_ax.text(.02, .97, f"Mediana de salidas: {sal.antiguedad_anios.median():.1f} anos",
         transform=ant_ax.transAxes, va="top", fontsize=8, color=ROJO)
ant_ax.set_xticks(x_ant); ant_ax.set_xticklabels(ant.index, rotation=25)
ant_ax.set_xlabel("Antiguedad al salir"); ant_ax.set_ylabel("Tasa de salida en el tramo (%)")
ant_ax.set_title("1-2 tiene la tasa puntual mas alta\n(pero con n=14; barras normalizadas por dotacion)", fontweight="bold")
ant_ax.legend(frameon=False, fontsize=7.5, loc="upper right")
save(fig_ant, "G6_antiguedad_rotacion.png")

grupos = [("Top performers", ultc[ultc.es_top_performer]), ("Resto", ultc[~ultc.es_top_performer])]
vals = [g.salio.mean() * 100 for _, g in grupos]
ics = [_wilson(int(g.salio.sum()), len(g)) for _, g in grupos]
xs = np.arange(2)
a4.bar(xs, vals, color=[NARANJA, GRIS], width=.45)
a4.errorbar(xs, vals, yerr=[[v - i[0] for v, i in zip(vals, ics)],
                            [i[1] - v for v, i in zip(vals, ics)]],
            fmt="none", ecolor="#2c3e50", elinewidth=1.5, capsize=6)
a4.axhspan(max(ics[0][0], ics[1][0]), min(ics[0][1], ics[1][1]), color=GRIS, alpha=.18)
for i, (v, n_) in enumerate(zip(vals, [len(g) for _, g in grupos])):
    a4.text(i, ics[i][1] + 1.2, f"{v:.1f}%\n(n={n_})", ha="center", fontsize=8, fontweight="bold")
a4.set_xticks(xs); a4.set_xticklabels([g[0] for g in grupos])
a4.set_ylabel("% rotación"); a4.set_ylim(0, 44)
a4.set_title("NO se sostiene: los márgenes de error se solapan\n(zona gris) — la diferencia puede ser azar", fontweight="bold")
save(fig, "G6_rotacion.png")

# ---------- G7: Brecha de trazabilidad de incidentes ----------
fig, ax = plt.subplots(figsize=(7.5, 3.6))
cats = ["Incidentes en\nnómina (panel)", "Con registro detallado\nen eventos_RRHH", "SIN investigación\nde causa raíz"]
vals = [100, 45, 55]
ax.bar(cats, vals, color=[AZUL, VERDE, ROJO], width=.55)
for i, v in enumerate(vals): ax.text(i, v + 1.8, str(v), ha="center", fontweight="bold", fontsize=11)
ax.set_ylabel("Incidentes registrados (17 meses)"); ax.set_ylim(0, 118)
ax.set_title("BRECHA DE TRAZABILIDAD: 55% de los incidentes no tienen\ncausa, parte del cuerpo ni acción correctiva registrada", fontweight="bold")
save(fig, "G7_brecha_trazabilidad.png")

# ---------- G8: la hora extra no se mueve ----------
AREAS_PROD = ["Estampado", "Ensamble", "Pintura"]
mprod = pa[pa.area.isin(AREAS_PROD)]
he_prod = mprod.groupby("mes_snapshot").horas_extra.mean()
u_prod = mprod.groupby("mes_snapshot").unidades_producidas.sum()
idx_prod = u_prod / u_prod.iloc[0] * 100
he_me = pa[pa.area == "Mantenimiento Eléctrico"].groupby("mes_snapshot").horas_extra.mean()

fig, ax = plt.subplots(figsize=(9.6, 4.4))
ax.plot(he_prod.index, he_prod.values, "o-", color=ROJO, lw=2.4, ms=4,
        label="Hora extra / persona — producción")
ax.plot(he_me.index, he_me.values, "-", color=GRIS, lw=1.4,
        label="Hora extra / persona — Mant. Eléctrico")
ax.set_ylabel("Horas extra por persona / mes"); ax.set_ylim(0, 21)
ax.tick_params(axis="x", rotation=45)

ax2 = ax.twinx(); ax2.grid(False)
ax2.plot(idx_prod.index, idx_prod.values, "--", color=AZUL, lw=1.8,
         label="Producción de planta (índice, ene-24 = 100)")
ax2.set_ylabel("Producción de planta (índice)"); ax2.set_ylim(80, 108)

pk = he_me.idxmax()
ax.annotate("Mant. Eléctrico:\npico de 3 meses\n(feb–abr 2025)", (pk, he_me.max()),
            textcoords="offset points", xytext=(-78, -4), fontsize=7.5, color="#555555",
            arrowprops=dict(arrowstyle="->", color="#999999", lw=1))
ax.text(.015, .06, "Calidad es la única área con hora extra creciente (4,0 → 6,3 h)",
        transform=ax.transAxes, fontsize=7.5, color="#555555")

lns = ax.get_lines() + ax2.get_lines()
ax.legend(lns, [l.get_label() for l in lns], frameon=False, fontsize=7.5, loc="lower right")
ax.set_title("Las horas extras no suben ni bajan con la producción", fontweight="bold")
save(fig, "G8_hora_extra_no_se_mueve.png")

# ---------- G9: cuanta gente es esa hora extra ----------
MESES_HE = pa.mes_snapshot.nunique()
gm = (pa.groupby(["area", "mes_snapshot"])
        .agg(hc=("empleado_id", "nunique"), he_tot=("horas_extra", "sum"),
             std_tot=("horas_trabajadas", "sum"), cohe=("costo_horas_extra", "sum"))
        .reset_index())
_rows = []
for area, s in gm.groupby("area"):
    if s.hc.mean() < 8:
        continue
    piso = s.he_tot.mean() / (s.std_tot / s.hc).mean()   # FTE a rendimiento pleno
    _rows.append((area, piso, piso / 0.70, s.cohe.sum() / MESES_HE * 12 / 1e6))
fte = pd.DataFrame(_rows, columns=["area", "piso", "techo", "costo_MM"]).sort_values("costo_MM")
prod_mask = fte.area.isin(AREAS_PROD).values

fig, ax = plt.subplots(figsize=(9.6, 4.6))
y = np.arange(len(fte))
cols = [ROJO if p else GRIS for p in prod_mask]
ax.barh(y, fte.piso, color=cols, label="a rendimiento pleno")
ax.barh(y, fte.techo - fte.piso, left=fte.piso, color=cols, alpha=.35,
        label="margen por curva de aprendizaje del ingresante")
for i, (pi, te, c) in enumerate(zip(fte.piso, fte.techo, fte.costo_MM)):
    ax.text(te + .3, i, f"{pi:.0f}–{te:.0f}  ·  ${c:.0f} MM/año", va="center", fontsize=7.5)
ax.set_yticks(y); ax.set_yticklabels(fte.area)
ax.set_xlabel("Personas-equivalente cubiertas con hora extra (por mes)")
ax.set_xlim(0, fte.techo.max() * 1.4)
p_lo, p_hi = fte.loc[prod_mask, "piso"].sum(), fte.loc[prod_mask, "techo"].sum()
p_cost = fte.loc[prod_mask, "costo_MM"].sum()
ax.text(.98, .05, f"Producción (Estampado + Ensamble + Pintura):\n{p_lo:.0f}–{p_hi:.0f} operarios  ·  ${p_cost:.0f} MM/año",
        transform=ax.transAxes, ha="right", fontsize=8.5, fontweight="bold", color=ROJO)
ax.legend(frameon=False, fontsize=7.5, loc="lower right", bbox_to_anchor=(1, .16))
ax.set_title("Las horas extras equivalen a entre 24 y 34 operarios de producción faltantes", fontweight="bold")
save(fig, "G9_hora_extra_en_personas.png")

# ---------- G15: Q1 - el costo por pieza sube porque bajan las piezas por hora ----------
_q = panel[(panel.activo) & (panel.area.isin(AREAS_PROD))]
_qp = _q[_q.unidades_producidas.notna() & _q.tasa_scrap_porcentaje.notna()].copy()
_qp["buenas"] = _qp.unidades_producidas * (1 - _qp.tasa_scrap_porcentaje / 100)
_ga = _q.groupby(["area", "mes_snapshot"]).agg(costo=("costo_total_mes", "sum"),
                                               hs=("horas_trabajadas", "sum")).reset_index()
_gp = _qp.groupby(["area", "mes_snapshot"]).agg(unid=("unidades_producidas", "sum"),
                                                buenas=("buenas", "sum")).reset_index()
q1 = _ga.merge(_gp, on=["area", "mes_snapshot"]).sort_values(["area", "mes_snapshot"])
q1["cpp"] = q1.costo / q1.buenas
q1["pph"] = q1.unid / q1.hs
_m = sorted(q1.mes_snapshot.unique())

fig, ax = plt.subplots(figsize=(9.6, 4.4))
for area, sub in q1.groupby("area"):
    ax.plot(sub.mes_snapshot, sub.cpp, "o-", lw=2, ms=3, label=area)
ax.set_ylabel("Costo laboral por pieza buena ($)")
_d0 = q1[q1.mes_snapshot == _m[0]].cpp.mean(); _d1 = q1[q1.mes_snapshot == _m[-1]].cpp.mean()
ax.annotate(f"+{_d1/_d0-1:.0%} de punta a punta", (_m[-1], _d1),
            textcoords="offset points", xytext=(-130, 6), fontsize=9, fontweight="bold", color=ROJO)
ax.tick_params(axis="x", rotation=45)
ax2 = ax.twinx(); ax2.grid(False)
_pph = q1.groupby("mes_snapshot").pph.mean()
ax2.plot(_pph.index, _pph.values, "--", color=GRIS, lw=1.8, label="Piezas por persona-hora (prom.)")
ax2.set_ylabel("Piezas por persona-hora")
_lns = ax.get_lines() + ax2.get_lines()
ax.legend(_lns, [l.get_label() for l in _lns], frameon=False, fontsize=7.5, loc="upper left")
ax.set_title(f"El costo por pieza subió ~{_d1/_d0-1:.0%}: se hacen menos piezas por hora trabajada", fontweight="bold")
save(fig, "G15_costo_pieza_sube.png")

# ---------- G16: Q1 - la rotacion no encarece la pieza (era la tendencia del tiempo) ----------
_s = ult[ult.salio].copy(); _s["ms"] = _s.fecha_salida.values.astype("datetime64[M]")
_arr = set(_s[_s.ms == panel.mes_snapshot.min()].empleado_id)
_sal = _s[~_s.empleado_id.isin(_arr)].groupby(["area", "ms"]).size().rename("sal")
_hc = _q.groupby(["area", "mes_snapshot"]).empleado_id.nunique().rename("hc")
q1 = (q1.merge(_sal, left_on=["area", "mes_snapshot"], right_on=["area", "ms"], how="left")
        .merge(_hc, on=["area", "mes_snapshot"]))
q1["sal"] = q1.sal.fillna(0); q1["rot"] = q1.sal / q1.hc * 100
q1["midx"] = q1.groupby("area").cumcount()
_res = pd.Series(index=q1.index, dtype=float)
for _a, _ix in q1.groupby("area").groups.items():
    _sub = q1.loc[_ix]; _b1, _b0 = np.polyfit(_sub.midx, _sub.cpp, 1)
    _res.loc[_ix] = _sub.cpp - (_b0 + _b1 * _sub.midx)
q1["cpp_res"] = _res
_qhi, _qlo = q1.rot.quantile(.75), q1.rot.quantile(.25)
_hi, _lo = q1[q1.rot >= _qhi], q1[q1.rot <= _qlo]
_crudo = (_hi.cpp.mean() / _lo.cpp.mean() - 1) * 100
_detr = (_hi.cpp_res.mean() - _lo.cpp_res.mean()) / _lo.cpp.mean() * 100

fig, ax = plt.subplots(figsize=(7.4, 4))
_b = ax.bar(["Comparación cruda\n(meses de rotación alta vs baja)", "Descontada la\ntendencia del tiempo"],
            [_crudo, _detr], color=[ROJO, GRIS], width=.5)
for _bar, _v in zip(_b, [_crudo, _detr]):
    ax.text(_bar.get_x() + _bar.get_width() / 2, _v + .12, f"{_v:+.1f}%", ha="center", fontweight="bold")
ax.axhline(0, color="k", lw=.8); ax.set_ylim(-1, _crudo + 2)
ax.set_ylabel("Sobrecosto por pieza en meses de rotación alta")
ax.set_title('El "+5 % por rotación" era la tendencia del tiempo, no la rotación', fontweight="bold")
save(fig, "G16_rotacion_no_encarece.png")

print("\nListo. Visualizaciones en:", V)
