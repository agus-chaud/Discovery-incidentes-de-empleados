# -*- coding: utf-8 -*-
"""MEJORA 3 — la rotacion en el tiempo, y que hacer con enero 2024."""
import pandas as pd, numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "06_resultados" / "Discovery" / "datos_transformados"
T = ROOT / "06_resultados" / "Discovery" / "tablas_soporte"
T.mkdir(parents=True, exist_ok=True)
panel = pd.read_parquet(D / "panel_mensual_limpio.parquet")
ult = pd.read_parquet(D / "empleados_nivel_persona.parquet")
pd.set_option("display.width", 200)

sal = ult[ult.salio].copy()
sal["mes_salida"] = sal.fecha_salida.values.astype("datetime64[M]")
INICIO = panel.mes_snapshot.min()

print("=" * 88)
print("DIAGNOSTICO — que pasa en enero 2024")
print("=" * 88)
ene = sal[sal.mes_salida == INICIO]
print(f"  Salidas en {INICIO.date()}: {len(ene)}  (un mes normal tiene ~6)")
print(f"  Antiguedad media al salir: {ene.antiguedad_anios.mean():.1f} anios")
print(f"  Motivos: {dict(ene.motivo_salida.value_counts())}")
print("\n  Cuantos meses aparece cada uno en el panel antes de irse:")
print(f"    {dict(ene.meses_observados.value_counts().sort_index())}")
print("\n  Comparado con el resto de las salidas:")
resto = sal[sal.mes_salida > INICIO]
print(f"    enero 2024: {ene.meses_observados.mean():.1f} meses observados en promedio")
print(f"    resto     : {resto.meses_observados.mean():.1f} meses observados en promedio")

# La prueba: si alguien "sale" en enero 2024 y solo aparece 1 mes, es que ya estaba
# de salida cuando arranco el archivo -> no es una salida DEL periodo, es arrastre.
arrastre = ene[ene.meses_observados <= 1]
print(f"\n  >> Salidas de enero-2024 que aparecen 1 solo mes: {len(arrastre)} de {len(ene)}")
print("     Son personas que ya estaban saliendo cuando empieza el archivo.")
print("     No son rotacion generada en el periodo: son arrastre del corte.")

print("\n" + "=" * 88)
print("RECALCULO — periodo limpio (desde febrero 2024)")
print("=" * 88)
CORTE = INICIO + pd.DateOffset(months=1)
hc = panel[panel.activo].groupby("mes_snapshot").empleado_id.nunique()

def tasa_acumulada(desde):
    # Definicion OFICIAL (DEC-019): salidas / personas expuestas en el universo del periodo.
    # Es la misma formula que ya usan las 10 areas de P5_rotacion_por_area_con_IC.csv,
    # los IC95 de Wilson y el grafico G9 — se unifica el titular contra esa base.
    if desde == INICIO:
        return len(sal), len(ult)
    s = sal[sal.mes_salida >= desde]
    s = s[~s.empleado_id.isin(arrastre)]
    universo = len(ult) - len(arrastre)
    return len(s), universo

def tasa_anualizada(desde):
    # Definicion informativa (NO usar como titular): anualizada sobre dotacion activa promedio.
    s = sal[sal.mes_salida >= desde]
    meses = int(panel[panel.mes_snapshot >= desde].mes_snapshot.nunique())
    h = hc[hc.index >= desde].mean()
    return len(s), meses, h, len(s) / meses * 12 / h * 100

for etiqueta, desde in [("Todo el periodo (con enero 2024)", INICIO),
                        ("Periodo limpio (desde feb 2024)", CORTE)]:
    n, u = tasa_acumulada(desde)
    print(f"  {etiqueta:36s} {n:3d} salidas / {u:3d} personas expuestas -> {n/u*100:5.1f}% acumulado")

n_all, u_all = tasa_acumulada(INICIO)
n_cl, u_cl = tasa_acumulada(CORTE)
t_all, t_cl = n_all / u_all * 100, n_cl / u_cl * 100
print(f"\n  >> La tasa acumulada con el arrastre incluido: {t_all:.1f}%.")
print(f"  >> Tasa corregida (definicion oficial, DEC-019): {t_cl:.1f}% acumulado del periodo  (diferencia: {t_all-t_cl:+.1f} puntos)")

_, m_cl, h_cl, t_cl_anual = tasa_anualizada(CORTE)
print(f"  Informativa, NO usar como titular (anualizada sobre dotacion activa): {t_cl_anual:.1f}% anual")

print("\n" + "=" * 88)
print("EVOLUCION MENSUAL (periodo limpio)")
print("=" * 88)
ev = (sal[sal.mes_salida >= CORTE].groupby("mes_salida").size()
      .reindex(hc[hc.index >= CORTE].index, fill_value=0).rename("salidas").to_frame())
ev["activos"] = hc[hc.index >= CORTE]
ev["tasa_%"] = (ev.salidas / ev.activos * 100).round(2)
ev["media_movil_3m"] = ev["tasa_%"].rolling(3, min_periods=1).mean().round(2)
print(ev.to_string())
x = np.arange(len(ev))
pend = np.polyfit(x, ev["tasa_%"].values, 1)[0]
h1, h2 = ev["tasa_%"].iloc[:len(ev)//2].mean(), ev["tasa_%"].iloc[len(ev)//2:].mean()
print(f"\n  Tendencia: {pend*12:+.2f} puntos porcentuales por anio")
print(f"  Primera mitad: {h1:.2f}%/mes | Segunda mitad: {h2:.2f}%/mes | cambio {(h2/h1-1)*100:+.0f}%")
# es una tendencia real o ruido? test simple sobre la pendiente
res = ev["tasa_%"].values - np.poly1d(np.polyfit(x, ev["tasa_%"].values, 1))(x)
se_p = np.sqrt((res @ res / (len(x) - 2)) / ((x - x.mean()) ** 2).sum())
print(f"  La pendiente se distingue de cero? t = {pend/se_p:.2f} -> "
      f"{'SI' if abs(pend/se_p) > 2 else 'NO — es ruido, no tendencia'}")
ev.to_csv(T / "P5_rotacion_evolucion_mensual.csv", encoding="utf-8-sig")

print("\n" + "=" * 88)
print("IMPACTO EN EL BUSINESS CASE")
print("=" * 88)
vol_all = (ult.motivo_salida == "Renuncia voluntaria").sum()
vol_cl = (sal[(sal.mes_salida >= CORTE)].motivo_salida == "Renuncia voluntaria").sum()
print(f"  Renuncias voluntarias — todo el periodo: {vol_all} | periodo limpio: {vol_cl}")
print(f"  Anualizadas — antes: {vol_all/17*12:.0f}/anio | ahora: {vol_cl/m_cl*12:.0f}/anio")
print(f"  >> La base del ahorro baja {(1 - (vol_cl/m_cl)/(vol_all/17))*100:.0f}%")
