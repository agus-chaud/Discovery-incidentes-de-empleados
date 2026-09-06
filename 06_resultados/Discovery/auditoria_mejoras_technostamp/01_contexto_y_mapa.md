# 01 · Contexto y mapa del proyecto

**Auditoría integral TechnoStamp — subentregable 1 de 6**
**Fecha:** 5 de septiembre de 2026 · **Alcance:** solo diagnóstico y recomendación; no se modificó código, notebook, datos ni visualizaciones.

---

## 1. Contexto recuperado

Fuentes leídas antes de auditar:

| Fuente | Qué aportó |
|---|---|
| Engram `#1043` — *Handoff TechnoStamp para nueva sesión* | Estado técnico: el notebook orquesta scripts por `subprocess`; `18_visualizaciones_decision.py` genera G8–G14; se usan `13_limpieza_v2` y `17_business_case_v2` en lugar de `03` y `09`. Commits `157413c`, `acd6a39`, `b050d62`, `71de2eb`. |
| Engram `#1044` — *Session summary* | El notebook no debe duplicar la lógica de los scripts; los PNG se renderizan inline porque los scripts usan backend `Agg`. |
| `decisions.md` | 17 decisiones vigentes (DEC-001 … DEC-018, sin DEC-002) y 3 decisiones pendientes de validación con el cliente. |
| `ESTUDIO_conceptos_technostamp.md` | 9 secciones conceptuales + mapa concepto → pregunta de entrevista. |
| `06_resultados/Discovery/conclusiones_ejecutivas_technostamp.md` | 4 insights ejecutivos + nota financiera. Es el entregable de comunicación. |
| `03_notebooks/Technostamp_Completo.ipynb` | 37 celdas, 16 etapas ejecutables. |
| `06_resultados/Discovery/Discovery_report.md` | Informe técnico completo, 13 secciones. |

---

## 2. Mapa del flujo real: datos → scripts → notebook → resultados → documentación

```
02_datos/01_Originales/           (RAW inmutable, DEC-001)
  ├─ empleados_mensual.csv        panel 9.733 filas · 694 personas · 17 meses
  ├─ eventos_rrhh.csv             fuente auditable de incidentes (DEC-004)
  └─ capacitaciones.csv
        │
        ▼   01_perfilado.py · 02_calidad.py          (diagnóstico, no escriben datos)
        ▼   13_limpieza_v2.py                        (ÚNICA etapa que escribe datos)
        │
06_resultados/Discovery/datos_transformados/
  ├─ panel_mensual_limpio.parquet           (empleado-mes)
  ├─ empleados_nivel_persona.parquet        (1 fila = 1 persona, DEC-005)
  ├─ eventos_limpio.parquet
  ├─ capacitaciones_limpio.parquet
  ├─ transformaciones.json   (receta de 31 pasos, DEC-014)
  ├─ politica_vacios.csv     (DEC-010)
  └─ _linaje.json
        │
        ▼  ANÁLISIS (leen parquet; escriben CSV de soporte y stdout)
        │   04_p1_p2 · 05_verif_critica · 06_p3_p4_p5 · 07_verif_incidentes_p5
        │   10_sensibilidad_he · 11_verif_cronicos_seguridad · 12_diagnostico_gaps
        │   14_eda_sistematico · 15_diagnostico_fragilidad · 16_rotacion_temporal
        │   17_business_case_v2
        ▼
06_resultados/Discovery/tablas_soporte/     17 CSV + BC_supuestos.json
06_resultados/EDA/EDA_report.md             54 alertas automáticas (DEC-013)
        │
        ▼  VISUALIZACIÓN
        │   08_visualizaciones.py            → G1–G7   (exploratorios)
        │   18_visualizaciones_decision.py   → G8–G14  (de decisión)
        ▼
06_resultados/Discovery/visualizaciones/    14 PNG
        │
        ▼  COMUNICACIÓN
  Discovery_report.md                       informe técnico (13 secciones)
  conclusiones_ejecutivas_technostamp.md    4 insights para Martina / CEO / Directorio
  decisions.md                              por qué de cada decisión
  ESTUDIO_conceptos_technostamp.md          aprendizaje conceptual
```

**Orquestador:** `03_notebooks/Technostamp_Completo.ipynb` corre cada script como proceso independiente (`subprocess` + `runpy`), muestra `stdout`/`stderr` y renderiza los PNG inline. No duplica lógica — eso está bien resuelto y hay que preservarlo.

---

## 3. Inventario de artefactos

| Carpeta | Estado | Observación |
|---|---|---|
| `01_Documentos/` | **vacía** | Andamiaje de plantilla sin usar |
| `02_datos/01_Originales/` | 3 CSV | Correcto, inmutable |
| `02_datos/02_Validacion/`, `03_Entrenamiento/`, `04_Caches/` | **vacías** | Andamiaje de un proyecto de modelado que este proyecto decidió no ser (ESTUDIO §1) |
| `03_notebooks/` | 1 notebook | 37 celdas |
| `04_scripts/` | 18 scripts, 3.339 líneas | 2 versiones obsoletas siguen en disco (ver §5) |
| `05_modelos/`, `07_despliegue/`, `99_otros/` | **vacías** | Andamiaje sin usar |
| `06_resultados/Discovery/` | informe + 14 PNG + 17 CSV + 4 parquet | Núcleo del entregable |
| `06_resultados/EDA/` | `EDA_report.md` | 54 alertas |
| Raíz del repo | 3 CSV duplicados + PDF del brief + ZIP | Copias sueltas de los originales |

---

## 4. Hallazgo principal de este subentregable

**El notebook no corre de punta a punta.** La celda 24 (`12_diagnostico_gaps.py`) terminó en `CalledProcessError` en la última ejecución guardada:

```
File "04_scripts/12_diagnostico_gaps.py", line 23, in <module>
    chk = ult.groupby("tuvo_inc").agg(...)
  ...pandas/core/apply.py, normalize_dictlike_arg
```

El notebook se presenta como *"ejecutá las celdas de arriba hacia abajo"*, y `ejecutar_etapa` hace `raise` ante cualquier código de salida distinto de cero. Un lector que siga esa instrucción se detiene en la etapa 11 de 16 y **nunca llega al EDA sistemático, al diagnóstico de fragilidad, a la rotación temporal corregida, al business case vigente ni a los gráficos de decisión G8–G14** — es decir, no llega a nada de lo que sostiene el informe ejecutivo.

Es un problema de credibilidad antes que de código: el artefacto que el proyecto ofrece como prueba de reproducibilidad hoy no reproduce.

*Nota de alcance:* `12_diagnostico_gaps.py` es un script de autodiagnóstico; queda pendiente verificar en el subentregable 03 si alguna cifra publicada depende de él.

---

## 5. Hallazgos secundarios de estructura

1. **Corrupción de caracteres en los dos documentos escritos más recientemente.** `decisions.md` (DEC-018) tiene 34 tokens con acentos reemplazados por `?` literal (`?rea`, `Decisi?n`, `El?ctrico`); `ESTUDIO_conceptos_technostamp.md` (§9) tiene 48 (`Log?stica`, `n?mina`, `n?mero`). Los bytes son UTF-8 válido y no hay ningún carácter de reemplazo: **no es un problema de visualización, el texto se escribió ya degradado y la información se perdió**. Es visible para cualquiera que abra el archivo, y contradice el estándar de calidad que el propio proyecto se fijó en DEC-002/DEC-012 sobre encoding.
2. **Dos versiones vivas del mismo paso.** `03_limpieza.py` y `09_business_case.py` siguen en disco, pero fueron reemplazados por `13_limpieza_v2.py` y `17_business_case_v2.py`. Nada en el nombre del archivo lo indica: hay que leer el notebook o `decisions.md` para saber cuál manda.
3. **La numeración de scripts no refleja el orden de ejecución.** El orden real es `01 → 02 → 13 → 04 → 05 → 06 → 07 → 08 → 10 → 11 → 12 → 14 → 15 → 16 → 17 → 18`. El prefijo numérico promete una secuencia que no existe.
4. **`Discovery_report.md` §13 (Reproducibilidad) está desactualizado.** Declara "Scripts del pipeline `01_perfilado.py … 14_eda_sistematico.py`", "Visualizaciones (G1–G7)" y "Tablas de soporte (12 CSV)". En disco hay 18 scripts, 14 PNG y 17 CSV. La sección que existe para dar trazabilidad es la que peor describe el estado real.
5. **Paths absolutos en 17 de 18 scripts.** Todos menos `18_visualizaciones_decision.py` tienen `C:\Users\Dell\Agus\Nivii AI` escrito a mano. `18` ya resuelve la raíz con `Path(__file__).resolve().parents[1]`: **el patrón correcto ya existe dentro del propio proyecto, solo no se propagó.** En cualquier otra máquina el pipeline no arranca.
6. **Texto del notebook inconsistente con su propio contenido.** La celda de cierre dice "Se ejecutaron las 15 etapas vigentes" y la lista `ETAPAS_EJECUTADAS` tiene 16.
7. **Siete carpetas vacías** (`01_Documentos`, `02_datos/02_Validacion`, `02_datos/03_Entrenamiento`, `02_datos/04_Caches`, `05_modelos`, `07_despliegue`, `99_otros`) y **tres CSV duplicados en la raíz del repo**. Para un lector nuevo sugieren trabajo faltante o dos fuentes de datos posibles.

---

## 6. Lo que ya está sólido y hay que preservar

- **Separación notebook / scripts.** El notebook aporta narrativa y secuencia; la lógica vive en `04_scripts/`. No hay duplicación. Es la mejor decisión de arquitectura del proyecto.
- **RAW inmutable + linaje + receta de 31 pasos** (DEC-001, DEC-014). Permite reprocesar los próximos meses sin reconstruir a mano lo que hizo otro.
- **`decisions.md` con alternativa descartada y bug evitado.** Artefacto poco común y muy defendible: DEC-004, DEC-009, DEC-015, DEC-016 y DEC-017 documentan conclusiones corregidas contra la intuición.
- **Tabla nivel-persona separada del panel** (DEC-005): evita pseudorreplicación y sesgo por permanencia.
- **Secciones "Qué NO se puede afirmar" y "Afirmaciones retiradas"** del `Discovery_report.md`. Es justamente lo que da credibilidad ante un directorio.

---

## 7. Riesgos abiertos que este subentregable no resuelve

| Riesgo | Dónde se trata |
|---|---|
| ¿El universo correcto es 450 o 562 activos? | Decisión de negocio pendiente con el cliente (ya registrada en `decisions.md`) |
| ¿El fallo de `12_diagnostico_gaps.py` afecta alguna cifra publicada? | Subentregable 03 |
| ¿Los números del informe ejecutivo coinciden con las tablas de soporte? | Subentregable 02 |

---

## Próximo subentregable

`02_datos_y_rigor.md` — universo, denominadores, período, incertidumbre y consistencia entre las cifras publicadas y las tablas de soporte.
