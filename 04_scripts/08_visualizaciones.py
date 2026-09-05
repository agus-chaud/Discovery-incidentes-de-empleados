# -*- coding: utf-8 -*-
"""Visualizaciones del Discovery TechnoStamp."""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
V = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\visualizaciones")

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
ax.set_title("Pirámide etaria — 562 activos (mayo 2025)\nHueco estructural en 50-59: solo 20 personas (3,6%)", fontweight="bold")
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
a2.set_ylim(15, 55); a2.set_title("Embudo de promoción: se angosta en el nivel 3", fontweight="bold")
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
a1.set_ylabel("Horas extra promedio/mes"); a1.set_ylim(9, 11)
a1.set_title("HE estructural, no un pico: 17 meses sostenidos", fontweight="bold")
a1.legend(frameon=False, fontsize=8); a1.tick_params(axis="x", rotation=45)

ar = pa.groupby("area").horas_extra.mean().sort_values()
a2.barh(ar.index, ar.values, color=[ROJO if v > 11 else (NARANJA if v > 5 else GRIS) for v in ar.values])
for i, v in enumerate(ar.values): a2.text(v + .15, i, f"{v:.1f}", va="center", fontsize=8)
a2.set_xlabel("Horas extra promedio/mes"); a2.set_title("Producción duplica a soporte", fontweight="bold")

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
a3.set_title("Pareto plano → el problema es SISTÉMICO,\nno de unos pocos abusadores", fontweight="bold")
a3.legend(frameon=False, fontsize=8)

t = pa.groupby("turno_trabajo").horas_extra.mean().sort_values()
a4.barh(t.index, t.values, color=[ROJO if v > 11.5 else (NARANJA if v > 5 else GRIS) for v in t.values])
for i, v in enumerate(t.values): a4.text(v + .15, i, f"{v:.1f}", va="center", fontsize=8)
a4.set_xlabel("Horas extra promedio/mes"); a4.set_title("Noche lidera en horas extra", fontweight="bold")
save(fig, "G4_horas_extra.png")

# ---------- G5: Seguridad ----------
fig, ((a1, a2), (a3, a4)) = plt.subplots(2, 2, figsize=(11.5, 7))
expo = pa.groupby("turno_trabajo").size()
it = inc.groupby("turno_trabajo").size()
tt = (it / expo * 1000).dropna().sort_values()
a1.barh(tt.index, tt.values, color=[ROJO if v > 8 else GRIS for v in tt.values])
for i, v in enumerate(tt.values): a1.text(v + .2, i, f"{v:.1f}", va="center", fontsize=8, fontweight="bold")
a1.set_xlabel("Incidentes cada 1.000 empleados-mes")
a1.set_title("Turno NOCHE: 5,4x el riesgo de mañana/tarde\n(hallazgo robusto en ambas fuentes)", fontweight="bold")

bins, labs = [-1, 6, 12, 24, 60, 120, 999], ["0-6m", "6-12m", "1-2a", "2-5a", "5-10a", "10a+"]
pa["ba"] = pd.cut(pa.antiguedad_meses, bins, labels=labs)
inc["ba"] = pd.cut(inc.antiguedad_meses, bins, labels=labs)
e2 = pa.groupby("ba", observed=True).size()
i2 = inc.groupby("ba", observed=True).size().reindex(e2.index).fillna(0)
r2 = (i2 / e2 * 1000)
a2.bar(range(len(r2)), r2.values, color=[GRIS if v < 5 else ROJO for v in r2.values])
a2.set_xticks(range(len(r2))); a2.set_xticklabels(r2.index)
for i, v in enumerate(r2.values): a2.text(i, v + .15, f"{v:.1f}", ha="center", fontsize=8, fontweight="bold")
a2.set_ylabel("Incidentes cada 1.000 empleados-mes"); a2.set_xlabel("Antigüedad")
a2.set_title("CONTRA-INTUITIVO: el riesgo sube con la experiencia\nCero incidentes en los primeros 12 meses", fontweight="bold")

sev = inc.groupby("severidad").agg(n=("evento_id", "size"), dias=("dias_perdidos", "sum")).reindex(["Leve", "Moderado", "Grave"])
xx = np.arange(3); w = .38
a3.bar(xx - w / 2, sev.n, w, color=GRIS, label="Cantidad de incidentes")
a3.bar(xx + w / 2, sev.dias, w, color=ROJO, label="Días perdidos")
for i, (a, b) in enumerate(zip(sev.n, sev.dias)):
    a3.text(i - w / 2, a + 1.5, int(a), ha="center", fontsize=8)
    a3.text(i + w / 2, b + 1.5, int(b), ha="center", fontsize=8, fontweight="bold")
a3.set_xticks(xx); a3.set_xticklabels(sev.index)
a3.set_title("6 incidentes GRAVES (13%) causan\n109 de 138 días perdidos (79%)", fontweight="bold")
a3.legend(frameon=False, fontsize=8)

st = inc.groupby("subtipo_evento").agg(n=("evento_id", "size"), dias=("dias_perdidos", "sum")).sort_values("dias")
a4.barh(st.index, st.dias, color=[ROJO if v > 30 else GRIS for v in st.dias])
for i, (d, n_) in enumerate(zip(st.dias, st.n)): a4.text(d + .8, i, f"{int(d)} días (n={n_})", va="center", fontsize=8)
a4.set_xlabel("Días perdidos"); a4.set_xlim(0, 62)
a4.set_title("Caídas y sobreesfuerzo = 63% de los días perdidos", fontweight="bold")
save(fig, "G5_seguridad.png")

# ---------- G6: Rotacion ----------
fig, ((a1, a2), (a3, a4)) = plt.subplots(2, 2, figsize=(11.5, 7))
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
a1.axvline(BASE, color=AZUL, ls="--", lw=1.4, label=f"Promedio {BASE:.1f}%")
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
a3.hist(sal.antiguedad_anios, bins=np.arange(0, 14, 1), color=AZUL, edgecolor="w")
a3.axvline(sal.antiguedad_anios.median(), color=ROJO, ls="--", lw=2,
           label=f"Mediana {sal.antiguedad_anios.median():.1f} años")
a3.set_xlabel("Años de antigüedad al salir"); a3.set_ylabel("Salidas")
a3.set_title("No se van los nuevos: se van a los 5 años,\ncuando ya están formados", fontweight="bold")
a3.legend(frameon=False, fontsize=8)

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

print("\nListo. Visualizaciones en:", V)
