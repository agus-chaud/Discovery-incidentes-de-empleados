# Registro de Decisiones Técnicas

Por qué se tomó cada decisión,  el código ya explica qué se hizo.
Formato corto: decisión → por qué (con la cifra clave) → regla a futuro.

**El razonamiento completo, con todas las cifras, alternativas descartadas y código
afectado, está en [`decisions_detalle.md`](decisions_detalle.md)** — mismos IDs, mismo
orden. Las decisiones superadas no se borran de ninguno de los dos archivos.

---

## Índice

| ID      | Área | Decisión |
|----     |------|----------|
| DEC-001 | setup | Raw del cliente inmutable en `01_Originales/` |
| DEC-002 | calidad-datos | cambio de encoding `latin-1`→`utf-8`|
| DEC-003 | calidad-datos | Inconsistencias con flags, nunca borrar filas |
| DEC-004 | calidad-datos | `eventos_rrhh` como única fuente de incidentes |
| DEC-005 | feature-engineering | Tabla de una fila por persona para preguntas de persona |
| DEC-006 | feature-engineering | Índice de criticidad propio, no `es_posicion_critica` |
| DEC-007 | eda | Tasas por empleado-mes, no conteos *(grupo rigor estadístico)* |
| DEC-008 | eda | Brecha salarial por OLS multivariado, no diferencia de medias |
| DEC-009 | evaluación | Horas extra→dotación: descartado, reportado en negativo |
| DEC-010 | calidad-datos | Clasificar por qué falta un dato antes de promediar |
| DEC-011 | calidad-datos | Sueldos extremos: detectados, no recortados |
| DEC-012 | calidad-datos | Columnas sin eñes, IDs siempre enteros |
| DEC-013 | eda | Barrido sistemático de las 95 columnas, no solo las necesarias |
| DEC-014 | transversal   | Limpieza como receta (`transformaciones.json`), no relato |
| DEC-015 | evaluación    | Ahorro de retención como rango, no cifra única |
| DEC-016 | eda           | Margen de error obligatorio en toda comparación *(grupo rigor estadístico)* |
| DEC-017 | calidad-datos | Excluir enero 2024 del cálculo de rotación (arrastre) |
| DEC-018 | comunicación | Hallazgos ejecutivos como riesgos focalizados, no plan de 90 días |
| DEC-019 | comunicación | Rotación oficial = 16,7% (acumulada), no 15,0% (anualizada) |
| DEC-020 | eda          | Bonferroni sobre las 10 áreas testeadas *(grupo rigor estadístico)* |
| DEC-021 | comunicación | G11 rehecho: por turno y tasa, no área y conteo |
| DEC-022 | comunicación | Límites de seguridad nocturna declarados en la propia slide |
| DEC-023 | calidad-datos | Retirar `meses_desde_ultimo_aumento` de todo análisis de rotación |
| DEC-024 | comunicación | G12 rehecho sobre cruce temporal, no correlación por área |
| DEC-025 | comunicación | Sucesión sobre jubilación a 12 meses, sin rótulo "posiciones críticas" |
| DEC-026 | eda          | Retirar el gradiente de riesgo por antigüedad (no se distingue) |
| DEC-027 | transversal | Ningún insight justifica pasar a Automation |
| DEC-028 | trazabilidad | Notebook celda 33: actualizar a los nombres de gráfico vigentes |
| DEC-029 | trazabilidad | Notebook celda 13: anotar que reproduce hallazgos ya retirados |
| DEC-030 | evaluación | Hora extra = déficit de dotación estructural (~7%), no volatilidad de demanda; condiciona DEC-009 |
| DEC-031 | calidad-datos | `es_top_performer` es el rating de un mes, no un rasgo; comparar por métrica de carrera |
| DEC-032 | evaluación | Costo por pieza: descriptivo sí; efecto de la rotación no identificable (control de tiempo + productividad) |

---

## Pendientes reales

| Decisión | Área |
|---|---|
| Confirmar con el cliente si la dotación informada (450) excluye contratistas o una planta — los datos muestran 562 activos / 694 totales | calidad-datos |
| Definir si el índice de criticidad propio (DEC-006) se adopta formalmente como reemplazo de `es_posicion_critica` en el sistema origen | feature-engineering |
| Renumerar `G8`/`G9`: `08_visualizaciones.py` (G1–G9, G15–G16) y `18_visualizaciones_decision.py` (G8–G14) usan G8 y G9 con nombres de archivo distintos pero el mismo número — no rompe, pero "G9" es ambiguo en prosa | trazabilidad |

---

## Rigor estadístico en comparaciones (DEC-007, DEC-016, DEC-020)

Regla compartida: nunca comparar grupos sin normalizar por exposición, sin margen de
error, y sin corregir cuando se testean varios grupos a la vez.

- **DEC-007 — Tasas por empleado-mes, no conteos absolutos.** Ensamble parecía 4x peor que Calidad en conteo (14 vs 3); normalizado por exposición, la brecha real es 26%. **Regla:** nunca comparar conteos de eventos entre grupos de tamaño distinto.
- **DEC-016 — Margen de error en toda comparación entre grupos.** Retiró "Estampado rota mal" (su IC contiene al promedio) y "los top performers rotan un 35% más" (intervalos solapados). **Regla:** solo marcar un grupo como distinto cuando su intervalo completo queda fuera del promedio.
- **DEC-020 — Corrección de Bonferroni sobre las diez áreas testeadas.** Mantenimiento Eléctrico sobrevive con margen (p=0,00105 contra umbral 0,005) — el único hallazgo por área que se sostiene. **Regla:** al testear más de dos grupos contra un mismo promedio, correr la corrección es tan barato como declarar que falta.

---

## Decisiones

**DEC-001 — Raw inmutable en `01_Originales/`.** Copiar los CSV del cliente a solo lectura; toda transformación se persiste aparte con `transformaciones.json` (receta y procedencia). **Por qué:** al corregir el encoding de `latin-1` a `utf-8`, sobrescribir el original hubiera hecho el error irreversible. **Regla:** nunca escribir sobre un archivo del cliente, ni para "arreglarlo".

**DEC-003 — Marcar inconsistencias con flags, no borrar filas.** 605 filas (6,2%) con antigüedad, fecha o edad inconsistente se conservan con flags booleanos. **Por qué:** no están distribuidas al azar — se concentran en reingresos y cambios de contrato, justo el perfil relevante para rotación; borrarlas sesga la tasa hacia abajo. **Regla:** nunca borrar filas por inconsistencia interna en un Discovery; marcar y reportar el conteo.

**DEC-004 — `eventos_rrhh` como única fuente de incidentes.** Todo análisis de seguridad usa esta tabla (45 casos), no `incidentes_seguridad_count` del panel (100 casos). **Por qué:** con la fuente del panel, los ingresantes parecían tener 10x más riesgo y los sobrecargados 3,71x — con la fuente auditable, ambos hallazgos se invierten (0 accidentes en el primer año; 0,47x). **Regla:** entre dos fuentes que miden lo mismo y difieren, elegir la auditable, no la de mayor volumen.

**DEC-005 — Tabla nivel-persona = último snapshot + agregados de historial.** Preguntas sobre personas (rotación, brecha salarial) se responden sobre una tabla de una fila por persona, no sobre el panel de 9.733 filas. **Por qué:** el panel pondera implícitamente por permanencia — sesga en contra de quien se va. **Regla:** en un panel longitudinal, construir la tabla de entidad antes de responder preguntas de entidad.

**DEC-006 — Índice de criticidad propio, no `es_posicion_critica`.** El flag del sistema marca 10 de 694 personas (1,4%) y no cambia en 17 meses; se construyó un índice propio (dotación baja + jerarquía + antigüedad + top performer) que identifica 47 empleados (8,4%). **Por qué:** con el flag original, la pregunta de sucesión del cliente tendría una respuesta cierta pero inútil. **Regla:** antes de usar un flag de negocio como insumo, verificar su cobertura y variación temporal.

**DEC-008 — Brecha salarial por OLS multivariado.** Se estima con regresión (n=562, R²=0,865), no diferencia de medias. **Por qué:** la media simple confunde género con composición (área, nivel jerárquico); ajustada da 0,02% no significativo, donde la cruda daba 0,9%. **Regla:** nunca reportar una brecha salarial como diferencia de medias; controlar por nivel, área y antigüedad como mínimo.

**DEC-009 — Horas extra→dotación: descartado, reportado en negativo.** Sustituir horas extra por contrataciones da flujo neto negativo en los tres escenarios. **Por qué:** el recargo de la hora extra (1,343x) es menor al costo cargado de un ingresante (>1,40x); el punto de equilibrio (cargas del 34,3%) no se cumple en Argentina. **Regla:** nunca convertir un costo grande en "oportunidad de ahorro" sin calcular el costo de la alternativa.

**DEC-010 — Clasificar por qué falta un dato antes de promediar.** El desperdicio de producción se promedia solo dentro de las áreas donde existe (60,9% de las filas). **Por qué:** no es un dato perdido, es un dato que no aplica a áreas administrativas — promediarlo mezcla dos poblaciones en un solo número. **Regla:** si un grupo está casi todo vacío y otro casi todo lleno, sacar ese grupo del universo, no promediarlo.

**DEC-011 — Sueldos extremos: detectados, no recortados.** 1.388 registros marcados como atípicos por rango intercuartílico, ninguno recortado. **Por qué:** siguen el organigrama exactamente — sube con cada nivel jerárquico, sin excepción; es estructura real, no error. **Regla:** antes de recortar un outlier, verificar si sigue un orden conocido (jerarquía, antigüedad, categoría).

**DEC-012 — Columnas sin eñes, IDs siempre enteros.** **Por qué:** la eñe rompe al mover datos entre sistemas; un ID con decimales (`1129.0`) falla al cruzar contra una tabla que lo espera entero, sin dar ningún error. **Regla:** normalizar nombres de columna al cargar los datos; identificadores siempre enteros.

**DEC-013 — Barrido sistemático de las 95 columnas.** No solo las que hacen falta para cada pregunta — 54 alertas automáticas levantadas. **Por qué:** encontró que solo 15 de 45 incidentes tienen acción correctiva, y las 15 dicen la misma frase; nadie lo había buscado a propósito. **Regla:** antes de responder la primera pregunta de negocio, pasar por todas las columnas con alertas automáticas.

**DEC-014 — Limpieza como receta, no como relato.** `transformaciones.json`: 31 pasos con valores ya calculados, no instrucciones en prosa. **Por qué:** una receta se reaplica exactamente a datos nuevos; una descripción en prosa hay que reconstruirla a mano. **Regla:** guardar cada paso de limpieza con su valor calculado, nunca con la instrucción que lo calcula.

**DEC-015 — Ahorro de retención como rango, no cifra única.** $23,3M–$194,8M/año, no $92M. **Por qué:** el 97% del costo por salida es supuesto propio (vacancia + rampa); solo $200.000 es dato medido. **Regla:** si los supuestos pesan más que los datos, publicar el rango con los supuestos a la vista, más el piso que se sostiene solo con datos duros.

**DEC-017 — Excluir enero 2024 del cálculo de rotación.** Las 19 salidas de enero son arrastre del corte del archivo — las 19 aparecen un solo mes en el panel. **Por qué:** con enero adentro, la rotación parecía estar bajando; sin él, es plana. **Regla:** revisar siempre el primer y el último mes de un panel por separado antes de calcular tasas.

**DEC-018 — Hallazgos ejecutivos como riesgos focalizados.** No como plan de 90 días, secuencia de métricas de RR.HH. ni pedido de aprobación genérico. **Por qué:** la audiencia necesita saber qué decisión merece atención, no reconstruir el análisis desde la planilla. **Regla:** presentar a C-level como conclusión + impacto + evidencia + acción; nunca un gráfico como conclusión.

**DEC-019 — Rotación oficial = 16,7% (acumulada del período).** No 15,0% (anualizada sobre dotación activa). **Por qué:** la acumulada ya sostenía las diez áreas, los IC95 y el 34,8% de Mantenimiento Eléctrico; usar la otra inflaba la brecha de 2,08x a 2,32x. **Regla:** cuando una tasa admite más de una fórmula, adoptar la que ya sostiene el resto del análisis.

**DEC-021 — G11 rehecho: por turno y tasa, no área y conteo.** **Por qué:** el gráfico citado para el hallazgo de turno noche mostraba área, no turno, y en conteo bruto — violaba DEC-007. **Regla:** si un gráfico se cita como evidencia, verificar que grafique la variable de la que habla el título.

**DEC-022 — Límites de seguridad nocturna, declarados en la propia slide.** El turno del incidente es el asignado, no el del hecho (coincide en 45 de 45 casos); la concentración de gravedad en la noche no se distingue del azar (Fisher p=0,205). **Por qué:** son generalizaciones que un directorio desarma con una pregunta. **Regla:** antes de convertir un hallazgo en slide, verificar qué mide exactamente cada campo que lo sostiene.

**DEC-023 — Retirar `meses_desde_ultimo_aumento` de todo análisis de rotación.** El patrón (1,0 mes en renuncias vs 4,5 en activos) se repite igual en los 5 motivos de salida, incluida jubilación — es artefacto de registro. **Por qué:** nadie se jubila por un aumento reciente; el campo se trunca al registrar cualquier baja. **Regla:** cuando una variable separa demasiado bien, preguntar primero cuándo se escribe ese dato.

**DEC-024 — G12 rehecho sobre cruce temporal y cobertura.** El título "se entrena después del accidente" describía 4 casos de 45; el cruce real muestra que el 80% nunca tuvo capacitación. **Por qué:** el código nunca había comparado fechas. **Regla:** antes de escribir "antes" o "después" en un titular, verificar que exista una comparación de fechas en el código.

**DEC-025 — Sucesión sobre jubilación a 12 meses, sin el rótulo "posiciones críticas".** 4 personas, 3 puestos, verificados; el rótulo importaba el flag ya descartado por DEC-006. **Por qué:** la tabla estaba bien, solo el rótulo estaba mal — y una corrección previa había descartado la tabla entera por error. **Regla:** al corregir, separar el rótulo del cálculo.

**DEC-026 — Retirar el gradiente de riesgo por antigüedad.** La tabla de tasas por banda no muestra diferencia real (chi²=5,68, p=0,339); la serie ni es monótona. **Por qué:** es el mismo error de DEC-016 —leer tendencia sin margen— aplicado a antigüedad. **Regla:** antes de afirmar una tendencia sobre categorías ordenadas, correr un test de homogeneidad.

**DEC-027 — Ningún insight justifica pasar a Automation.** Los 12 insights evaluados dan "ninguno", cada uno con su umbral escrito. **Por qué:** en los casos principales falta el dato que explicaría el fenómeno (causa raíz, motivo de salida), no el algoritmo que lo predeciría. **Regla:** no recomendar ML porque sea técnicamente posible; publicar siempre el umbral de un "no".

**DEC-028 — Notebook celda 33: actualizar a los nombres de gráfico vigentes.** Pide `G12_capacitacion_seguridad_vs_incidentes.png` y `G13_riesgo_sucesion_por_puesto.png`, renombrados por DEC-024/025 a `G12_cobertura_capacitacion_seguridad.png` y `G13_alerta_sucesion.png`. **Por qué:** `mostrar_graficos()` lanza `FileNotFoundError` si el archivo no existe, y los nombres viejos ya no están en disco — el notebook no corre hoy de punta a punta. **Regla:** un rename de archivo de salida es un cambio de contrato; revisar en el mismo commit todas las celdas que lo referencian.

**DEC-029 — Notebook celda 13: anotar que reproduce hallazgos ya retirados.** La celda calcula, sin nota, la tasa de incidentes por antigüedad sobre la fuente que DEC-004 descartó y la comparación de `meses_desde_ultimo_aumento` que DEC-023 prohibió. **Por qué:** el notebook nunca se corrió de punta a punta en una sola pasada (`execution_count` no monótono) — nadie notó que esta celda contradice a las que vienen después. **Regla:** cuando `decisions.md` retira un hallazgo, buscar todas las celdas del notebook que lo reproducen, no solo el script que lo originó.

**DEC-030 — Hora extra caracterizada como déficit de dotación estructural, no como volatilidad de demanda.** En las seis áreas cargadas la hora extra por persona es plana los 17 meses (CV 1–5%) y no covaría con la producción (R² ≈ 0,00–0,08); la producción incluso cayó (Estampado −7%, Pintura −12%) sin que la hora extra se moviera. Es aditiva a la jornada (correlación ≈ 0 con `horas_trabajadas`) y equivale al 6,2% de las horas-plantel estándar — **24–34 operarios de producción, $670 MM/año** ($985 MM en toda la planta). **Por qué:** DEC-009 comparó hora extra *flexible* contra dotación al margen y concluyó que no conviene contratar; este análisis muestra que la hora extra no es flexible, es un faltante fijo de ~7% sostenido 17 meses. No revierte DEC-009: lo condiciona. La decisión pasa a ser si ese déficit es deliberado y si el recargo (1,343x) más fatiga, ausentismo (DEC-009 detalle) y scrap sigue por debajo del costo de cubrir esas posiciones. **Regla:** antes de clasificar un costo recurrente como flexible, verificar que efectivamente varíe con su driver; un costo plano durante 17 meses es estructural por definición. **Código:** `04_scripts/19_hora_extra_estructural.py`, notebook §10b, gráficos `G8_hora_extra_no_se_mueve.png` y `G9_hora_extra_en_personas.png`. El número firme es el porcentaje; el conteo de FTE es un rango (supone rampa de 0,70, N2 no medido).

**DEC-031 — `es_top_performer` es `rating_performance == 5` de un mes, no un rasgo estable.** El flag coincide con rating 5 en 790 de 794 filas-mes; cambia a lo largo del panel para 344 de 694 empleados (~50%), y los 349 alguna vez marcados promedian 3,4/5 de rating de carrera contra 3,0 del resto. En la tabla nivel-persona (DEC-005) se toma del último snapshot, así que para quien se fue es el rating del mes de salida. **Por qué:** el hallazgo "los top performers rotan más" —ya retirado por DEC-016— resulta además un artefacto de definición: con excelencia sostenida (`perf_prom` ≥ 4,5, n=8) la rotación es 0, y con ≥ 6 meses en rating 5 (n=15) también; solo la definición ruidosa del flag mensual produce la diferencia. `crit_top_performer` del índice de criticidad (DEC-006) hereda el mismo ruido. **Regla:** para comparar rotación o riesgo por desempeño, definir el grupo con una métrica de carrera (media de rating, meses en el nivel máximo), nunca con un flag de un solo período.

**DEC-032 — Costo laboral por pieza: análisis descriptivo, sin número para el efecto de la rotación.** La pregunta Q1 se responde con estadística descriptiva sobre 51 filas área-mes de Estampado, Ensamble y Pintura: el costo laboral por pieza buena es ~$1.986 (Estampado $2.075), subió ~17% en el panel —aprox. mitad por menos piezas por persona-hora (liga con DEC-030), mitad por el precio de la hora—, y el scrap es 2,3% ($37–$54 por pieza). **Por qué:** la primera versión regresaba el costo por pieza contra rotación/HE/ausentismo sin controlar el tiempo, y una comparación de cuartiles daba "+5% en meses de rotación alta". Pero el costo por pieza subió solo por la caída de volumen a lo largo del panel, y los meses de rotación alta son los tardíos: al agregar `mes_idx` a la regresión el R² pasa de 0,49 a 0,84 y la rotación queda en t=−0,55. Y `costo_total_mes` incluye el costo de la hora extra, así que regresar el costo contra HE es circular —la variable de salida se cambió a productividad física (unidades/persona-hora), que no se arma con la nómina—. **Regla:** para preguntar si X encarece la producción, controlar el paso del tiempo antes de comparar períodos y usar una métrica física como variable de salida, no una que se construya con la misma nómina que se quiere explicar. Umbral del "no": costos deflactados, granularidad por línea/turno y costo de rampa N1/N2. **Código:** `04_scripts/20_costo_pieza_buena.py`, notebook §10c, `04_scripts/08_visualizaciones.py` (G15, G16), `tablas_soporte/Q1_costo_pieza_buena.csv`.
