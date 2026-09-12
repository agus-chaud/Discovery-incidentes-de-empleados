# -*- coding: utf-8 -*-
"""Perfilado inicial de las 3 tablas de TechnoStamp. Raw inmutable: solo lectura."""
import pandas as pd
import numpy as np
from pathlib import Path

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 100)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_datos" / "01_Originales"

def load(name):
    return pd.read_csv(RAW / name, low_memory=False)

emp = load("empleados_mensual.csv")
evt = load("eventos_rrhh.csv")
cap = load("capacitaciones.csv")

for nombre, df in [("empleados_mensual", emp), ("eventos_rrhh", evt), ("capacitaciones", cap)]:
    print("=" * 90)
    print(f"TABLA: {nombre}   shape={df.shape}")
    print("-" * 90)
    info = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "n_nulos": df.isna().sum(),
        "pct_nulos": (df.isna().mean() * 100).round(1),
        "n_unicos": df.nunique(dropna=True),
        "ejemplo": [df[c].dropna().iloc[0] if df[c].notna().any() else None for c in df.columns],
    })
    print(info.to_string())
