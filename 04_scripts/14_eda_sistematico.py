# -*- coding: utf-8 -*-
"""
MEJORA 5 — Revision sistematica de TODAS las columnas, una por una.
No busca respuestas: busca problemas que nadie sospecha.
Salida: 06_resultados/EDA/EDA_report.md
"""
import pandas as pd, numpy as np
from pathlib import Path

D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
E = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\EDA")
E.mkdir(parents=True, exist_ok=True)

# Umbrales (declarados, no escondidos en el codigo)
U_VACIO      = 0.20   # avisar si mas del 20% esta vacio
U_CONSTANTE  = 0.99   # avisar si un solo valor ocupa el 99% o mas
U_RARA       = 0.01   # etiqueta rara: aparece en menos del 1% de los casos

tablas = {
    "empleados_mensual":  pd.read_parquet(D / "panel_mensual_limpio.parquet"),
    "eventos_rrhh":       pd.read_parquet(D / "eventos_limpio.parquet"),
    "capacitaciones":     pd.read_parquet(D / "capacitaciones_limpio.parquet"),
}

def tipar(s, n):
    """Clasifica una columna en un tipo de variable."""
    if pd.api.types.is_datetime64_any_dtype(s):            return "fecha"
    if pd.api.types.is_bool_dtype(s):                      return "booleana"
    if pd.api.types.is_numeric_dtype(s):
        entera = s.dropna().mod(1).eq(0).all() if s.notna().any() else False
        return "numerica discreta" if (entera and s.nunique() <= min(20, 0.05 * n)) else "numerica continua"
    if s.nunique() > max(50, 0.5 * np.sqrt(n)):
        largo = s.dropna().astype(str).str.len().mean() if s.notna().any() else 0
        return "texto" if largo > 25 else "alta cardinalidad"
    return "categorica"

lineas = ["# Revisión sistemática de variables — TechnoStamp",
          "",
          "Revisión columna por columna de las tres tablas. No parte de ninguna pregunta de "
          "negocio: recorre todo el dataset buscando problemas que nadie sospecha.",
          "",
          f"**Umbrales usados:** vacíos > {U_VACIO:.0%} · valor dominante ≥ {U_CONSTANTE:.0%} · "
          f"etiqueta rara < {U_RARA:.0%}", ""]

todas_alertas = []

for nombre, df in tablas.items():
    n = len(df)
    tipos = {c: tipar(df[c], n) for c in df.columns}
    resumen = pd.Series(tipos).value_counts()

    print(f"\n{'='*80}\nTABLA {nombre} — {n:,} filas × {len(df.columns)} columnas")
    print("  " + " | ".join(f"{k}: {v}" for k, v in resumen.items()))

    lineas += [f"## Tabla `{nombre}`", "",
               f"{n:,} filas × {len(df.columns)} columnas", "",
               "| Tipo de variable | Columnas |", "|---|---|"]
    lineas += [f"| {k} | {v} |" for k, v in resumen.items()]
    lineas += [""]

    alertas = []
    for c in df.columns:
        s, t = df[c], tipos[c]
        vacio = s.isna().mean()
        if vacio > U_VACIO:
            alertas.append((c, t, "VACÍOS", f"{vacio:.1%} sin dato"))
        if s.notna().any():
            fr = s.value_counts(normalize=True, dropna=True)
            if len(fr) and fr.iloc[0] >= U_CONSTANTE:
                alertas.append((c, t, "CASI CONSTANTE", f"'{fr.index[0]}' ocupa el {fr.iloc[0]:.1%}"))
            if len(fr) == 1:
                alertas.append((c, t, "CONSTANTE", "un único valor — no aporta información"))
        if t == "categorica":
            fr = s.value_counts(normalize=True, dropna=True)
            raras = fr[fr < U_RARA]
            if len(raras):
                alertas.append((c, t, "ETIQUETAS RARAS", f"{len(raras)} etiquetas bajo el {U_RARA:.0%}"))
        if t in ("numerica continua", "numerica discreta") and s.notna().sum() > 10:
            sk = s.skew()
            if abs(sk) > 2:
                alertas.append((c, t, "MUY ASIMÉTRICA", f"asimetría {sk:.1f} — cola larga"))
        if t == "alta cardinalidad":
            alertas.append((c, t, "ALTA CARDINALIDAD", f"{s.nunique():,} valores distintos"))
        if t == "fecha" and s.notna().any():
            if s.max() > pd.Timestamp("2026-09-03"):
                alertas.append((c, t, "FECHA FUTURA", f"máximo {s.max().date()}"))

    if alertas:
        a = pd.DataFrame(alertas, columns=["columna", "tipo", "alerta", "detalle"])
        print(f"\n  {len(a)} alertas:")
        print(a.to_string(index=False))
        lineas += ["### Alertas", "", "| Columna | Tipo | Alerta | Detalle |", "|---|---|---|---|"]
        lineas += [f"| `{r.columna}` | {r.tipo} | **{r.alerta}** | {r.detalle} |" for r in a.itertuples()]
        lineas += [""]
        todas_alertas += [(nombre, *x) for x in alertas]
    else:
        print("\n  Sin alertas.")
        lineas += ["### Alertas", "", "Ninguna.", ""]

    # ── estadisticas por tipo ──
    num = [c for c, t in tipos.items() if t.startswith("numerica")]
    if num:
        st = df[num].describe().T[["count", "mean", "50%", "std", "min", "max"]].round(2)
        st.columns = ["n", "media", "mediana", "desvío", "mín", "máx"]
        lineas += ["### Variables numéricas", "", st.to_markdown(), ""]

    cat = [c for c, t in tipos.items() if t in ("categorica", "booleana")]
    if cat:
        filas = []
        for c in cat:
            fr = df[c].value_counts(normalize=True, dropna=True)
            filas.append({"columna": c, "categorías": df[c].nunique(),
                          "más frecuente": str(fr.index[0])[:32] if len(fr) else "—",
                          "% que ocupa": f"{fr.iloc[0]:.1%}" if len(fr) else "—",
                          "% vacío": f"{df[c].isna().mean():.1%}"})
        lineas += ["### Variables categóricas", "", pd.DataFrame(filas).to_markdown(index=False), ""]

    fec = [c for c, t in tipos.items() if t == "fecha"]
    if fec:
        filas = [{"columna": c, "desde": str(df[c].min())[:10], "hasta": str(df[c].max())[:10],
                  "% vacío": f"{df[c].isna().mean():.1%}"} for c in fec]
        lineas += ["### Fechas", "", pd.DataFrame(filas).to_markdown(index=False), ""]

# ── cierre ──
print(f"\n{'='*80}\nTOTAL: {len(todas_alertas)} alertas en las 3 tablas")
conteo = pd.Series([a[3] for a in todas_alertas]).value_counts()
print(conteo.to_string())

lineas += ["## Resumen", "",
           f"**{len(todas_alertas)} alertas** en total.", "",
           "| Tipo de alerta | Cantidad |", "|---|---|"]
lineas += [f"| {k} | {v} |" for k, v in conteo.items()]
lineas += ["", "### Cómo leer estas alertas", "",
           "Una alerta **no es un error**. Es una columna que merece una decisión explícita:",
           "",
           "- **Vacíos** — hay que decidir si el dato falta o si no aplica a ese grupo "
           "(ver `politica_vacios.csv`).",
           "- **Casi constante** — la columna casi no varía, así que aporta poco para comparar grupos.",
           "- **Etiquetas raras** — categorías con muy pocos casos; los porcentajes sobre ellas son ruido.",
           "- **Muy asimétrica** — unos pocos valores muy altos tiran del promedio; conviene mirar la mediana.",
           "- **Alta cardinalidad** — demasiados valores distintos (nombres, identificadores); "
           "no sirve para agrupar.",
           ""]

(E / "EDA_report.md").write_text("\n".join(lineas), encoding="utf-8")
print(f"\nInforme: {E / 'EDA_report.md'}")
