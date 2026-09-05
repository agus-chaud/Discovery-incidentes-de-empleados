# -*- coding: utf-8 -*-
"""Verificacion: coherencia de es_posicion_critica y meses_hasta_jubilacion."""
import pandas as pd, numpy as np
from pathlib import Path
D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
pd.set_option("display.width",200)
panel = pd.read_parquet(D/"panel_mensual_limpio.parquet")
ult   = pd.read_parquet(D/"empleados_nivel_persona.parquet")
act   = ult[~ult.salio].copy()

print("### es_posicion_critica")
print("  filas panel con critica=True:", int(panel.es_posicion_critica.sum()))
print("  empleados que ALGUNA VEZ fueron criticos:", panel.groupby('empleado_id').es_posicion_critica.max().sum())
print("  empleados criticos en su ULTIMO snapshot:", int(ult.es_posicion_critica.sum()))
print("  varia dentro del mismo empleado?:", int((panel.groupby('empleado_id').es_posicion_critica.nunique()>1).sum()), "empleados")
print("\n  Quienes son los criticos (activos):")
print(act[act.es_posicion_critica][["empleado_id","area","puesto","nivel_jerarquico","edad","antiguedad_anios","span_of_control","meses_hasta_jubilacion"]].to_string(index=False))

print("\n### meses_hasta_jubilacion vs edad — coherencia")
print(act.groupby('banda_edad', observed=True).agg(n=('empleado_id','size'),
      mhj_min=('meses_hasta_jubilacion','min'), mhj_p50=('meses_hasta_jubilacion','median'),
      mhj_max=('meses_hasta_jubilacion','max')).to_string())
print("\n  Edad implicita de jubilacion = edad + meses/12:")
act['edad_jub'] = (act.edad + act.meses_hasta_jubilacion/12).round(0)
print("  ", dict(act.edad_jub.value_counts().head(8)))
print("  por genero:", act.groupby('genero').edad_jub.median().to_dict())

print("\n### PIRAMIDE ETARIA de activos")
print(act.banda_edad.value_counts().sort_index().to_string())
print("\n  Empleados 55+:", int((act.edad>=55).sum()), " | 60+:", int((act.edad>=60).sum()))
print("  Se jubilan en <=36m (recalculado con edad_jub):", int((act.meses_hasta_jubilacion<=36).sum()))

print("\n### CRITICIDAD ALTERNATIVA basada en datos (el flag oficial cubre solo 5 personas)")
# senal 1: puestos con dotacion chica  senal 2: gente que manda  senal 3: know-how (antiguedad alta)
dot = act.groupby('puesto').empleado_id.size().rename('dotacion_puesto')
a = act.merge(dot, on='puesto')
a['escaso']     = a.dotacion_puesto <= 3
a['manda']      = (a.span_of_control >= 3) | (a.nivel_jerarquico >= 3)
a['knowhow']    = a.antiguedad_anios >= 10
a['top']        = a.es_top_performer
a['score_crit'] = a[['escaso','manda','knowhow','top']].sum(1)
print("  distribucion score de criticidad (0-4):", dict(a.score_crit.value_counts().sort_index()))
alto = a[a.score_crit>=2]
print(f"\n  Empleados con score>=2 (criticidad real estimada): {len(alto)} ({len(alto)/len(a)*100:.1f}% de la dotacion)")
print(f"  De esos, edad 55+: {int((alto.edad>=55).sum())} | 58+: {int((alto.edad>=58).sum())} | 60+: {int((alto.edad>=60).sum())}")
print("\n  Top areas con criticidad estimada alta y edad 55+:")
print(alto[alto.edad>=55].groupby(['area','puesto']).agg(n=('empleado_id','size'),
      edad=('edad','mean'), antig=('antiguedad_anios','mean'), dot=('dotacion_puesto','first')).sort_values('n',ascending=False).round(1).to_string())
