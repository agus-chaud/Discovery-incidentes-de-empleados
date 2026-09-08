# Registro de Decisiones Técnicas — detalle completo

**Este es el archivo de detalle.** `decisions.md` tiene el índice, el resumen corto de
cada decisión y la lista de pendientes reales — es el que conviene leer primero.
Acá está el razonamiento completo de cada una: alternativa descartada, cifras exactas,
lección aprendida y código afectado. Mismos IDs que `decisions.md`, en el mismo orden.
Las decisiones superadas NO se borran.

---

## DEC-001: Raw inmutable en `02_datos/01_Originales/`

**Área:** setup | **Fase:** Discovery — preparación | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Copiar los tres CSV entregados por el cliente a `02_datos/01_Originales/` y tratarlos como de solo lectura. Toda transformación se persiste aparte, en `06_resultados/Discovery/datos_transformados/`, con un `_linaje.json` que registra origen, encoding, lista de transformaciones y propósito.

**Alternativa descartada:** Limpiar los CSV en el lugar (sobrescribirlos con la versión corregida) y trabajar directamente sobre la carpeta raíz del proyecto.

**Por qué la descartamos:** Durante el análisis cambiamos el encoding de `latin-1` a `utf-8` (ver DEC-002). Si hubiéramos sobrescrito los originales en la primera pasada, el segundo intento habría leído un archivo ya corrompido por la decodificación errónea y el mojibake sería irreversible — no habría existido un byte original contra el cual verificar con hexdump. La inmutabilidad del raw fue lo que permitió detectar y revertir el error.

**Conclusión:** Nunca escribir sobre un archivo entregado por el cliente, ni siquiera para "arreglarlo". Siempre copiar a `01_Originales/` 
**Bug evitado:** Corrupción irreversible del dataset original por decodificación errónea.
---


## DEC-003: Marcar inconsistencias con flags en vez de borrar filas

**Área:** calidad-datos | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Las 605 filas con inconsistencias internas (483 con antigüedad declarada distinta de la calculada, 71 con snapshot previo a la fecha de ingreso, 51 con edad incompatible con la fecha de nacimiento) se conservan y se marcan con columnas booleanas `flag_antig_inconsistente`, `flag_snapshot_pre_ingreso` y `flag_edad_inconsistente`. No se eliminó ninguna fila del panel.

**Alternativa descartada:** Filtrar esas filas del dataset de trabajo por considerarlas datos sucios.

**Por qué la descartamos:** Son el 6,2% del panel, y no están distribuidas al azar — la inconsistencia de antigüedad se concentra en empleados con reingresos o cambios de contrato, exactamente el perfil que importa para el análisis de rotación. Borrarlas habría sesgado la tasa de rotación hacia abajo 

**Conclusión:** Nunca borrar filas por inconsistencia interna en un análisis de discovery. Siempre marcarlas con un flag booleano y reportar el conteo. Si una inconsistencia obliga a excluir registros de un cálculo puntual, hacerlo en ese cálculo y declararlo, nunca en la capa de datos.

---

## DEC-004: `eventos_rrhh` como fuente de incidentes, por que tiene mas argumentos para poder verificar

**Área:** calidad-datos | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Todo análisis de seguridad se calcula sobre la tabla `eventos_rrhh` filtrada por `tipo_evento == "incidente_seguridad"` (45 registros). La columna `incidentes_seguridad_count` del panel mensual (100 incidentes) se usa únicamente para **cuantificar la brecha de trazabilidad**, nunca para estimar tasas ni sustentar recomendaciones.

**Alternativa descartada:** Usar `incidentes_seguridad_count` del panel, que tiene el doble de casos y se cruza trivialmente con todas las variables del empleado-mes (turno, antigüedad, horas extra) sin necesidad de joins.

**Por qué la descartamos:** El cruce a nivel empleado-mes mostró que los 45 eventos coinciden todos con el panel, pero hay **54 empleado-mes con `count > 0` sin ficha en `eventos_rrhh`** — es decir, sin causa raíz, parte del cuerpo afectada ni acción correctiva registrada. Elegir la fuente cambió conclusiones enteras, no matices:

| Hallazgo | Fuente `panel` | Fuente `eventos_rrhh` | Veredicto |
|---|---|---|---|
| Incidentes en los primeros 6 meses | 78,0 ×1.000 (10x el promedio) | **0,0 — ninguno** | El hallazgo era un artefacto |
| Sobrecarga crónica y accidentes | 3,71x más riesgo | **0,47x — menos riesgo** (z = −1,09) | Las fuentes se contradicen |
| Exceso de riesgo en turno noche | 22,1 vs 5,3 ×1.000 | 11,8 vs 2,2 ×1.000 | Robusto en ambas — se sostiene |

Con la fuente del panel, la recomendación al directorio habría sido reforzar el onboarding de seguridad. La fuente auditable dice que **la antigüedad mínima de un accidentado es 13 meses y la mediana 6,6 años**: el problema es la complacencia del personal experimentado, no la inexperiencia. Habríamos dirigido presupuesto a un problema inexistente.

**Conclusión:** Cuando dos fuentes miden el mismo fenómeno y difieren, nunca elegir la de mayor volumen ni la más cómoda de cruzar. Siempre elegir la auditable — la que trae causa, contexto y trazabilidad — y usar la diferencia entre ambas como hallazgo de gobierno del dato. 

**Bug evitado:** Recomendación de inversión en onboarding de seguridad sustentada en un artefacto de una columna no auditable.

**Lección aprendida:** Un hallazgo espectacular (10x de riesgo) es una señal de alarma metodológica antes que un insight. Los efectos grandes en datos observacionales suelen ser errores de medición.

**Código afectado:** `04_scripts/07_verif_incidentes_p5.py`, `04_scripts/11_verif_cronicos_seguridad.py`.

---

## DEC-005: Tabla nivel-persona = último snapshot + agregados de historial

**Área:** feature-engineering | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Construir `empleados_nivel_persona.parquet` tomando el **último snapshot** de cada empleado (atributos de estado: área, puesto, salario, edad, motivo de salida) y adjuntando **agregados de todo su historial** (`he_prom`, `ausencias_total`, `incidentes_total`, `perf_prom`, `meses_observados`). Las preguntas de nivel persona — rotación, sucesión, brecha salarial — se responden sobre esta tabla, no sobre el panel.

**Alternativa descartada:** Responder las preguntas de nivel persona directamente sobre el panel de 9.733 filas empleado-mes.

**Por qué la descartamos:** El panel repite cada empleado hasta 17 veces, y la cantidad de repeticiones **no es uniforme**: quien se fue en marzo de 2024 aparece 3 veces, quien sigue activo aparece 17. Cualquier promedio sobre el panel pondera implícitamente por permanencia, sesgando sistemáticamente contra los que se van. El caso concreto: `motivo_salida` tiene 132 valores no nulos a nivel fila, pero eso son 132 **filas**, no 132 personas — sin la tabla nivel-persona el conteo de salidas es incorrecto.

**Conclusión:** Siempre que un dataset sea un panel longitudinal, construir explícitamente la tabla de entidad antes de responder preguntas de entidad. Nunca promediar sobre el panel para caracterizar personas. Al comparar grupos sobre el panel, verificar primero que la exposición (`meses_observados`) sea comparable, o normalizar por ella.

**Bug evitado:** Conteo de salidas y promedios de perfil sesgados por permanencia desigual
---

## DEC-006: Índice de criticidad propio en vez de `es_posicion_critica`

**Área:** feature-engineering | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Para el análisis de riesgo de sucesión se construyó un índice de criticidad de 0 a 4 sumando cuatro señales observables: puesto con dotación ≤ 3 (`escaso`), `span_of_control ≥ 3` o nivel jerárquico ≥ 3 (`manda`), antigüedad ≥ 10 años (`knowhow`) y `es_top_performer` (`top`). El flag `es_posicion_critica` se reporta al cliente como brecha de calidad, no se usa como insumo analítico.

**Alternativa descartada:** Usar `es_posicion_critica` tal como viene, que es el campo que el sistema del cliente destina precisamente a esto.

**Por qué la descartamos:** El flag marca **10 empleados de 694 (1,4%)**, y es constante por empleado — nunca cambia a lo largo de los 17 meses, lo que indica que se cargó una vez y no se mantuvo. Con 5 posiciones críticas activas es imposible hacer planificación de sucesión: la pregunta de Martina ("¿cuántos puestos críticos están en riesgo?") tendría como respuesta literal "cuatro", que es cierto pero inútil. El índice propio identifica 47 empleados (8,4%) con criticidad estimada, una base sobre la que sí se puede planificar.

**Conclusión:** Antes de usar un flag de negocio como insumo analítico, verificar su cobertura y su variación temporal. Si marca menos del 5% del universo y es constante por entidad, tratarlo como no mantenido: construir un proxy con señales observables y reportar la brecha al cliente. Nunca presentar un resultado basado en un flag sin mantener sin declarar esa limitación.

**Lección aprendida:** Un campo que existe no es un campo que se usa. La cobertura del flag es un chequeo de calidad tan obligatorio como los nulos.

---

## DEC-007: Tasas normalizadas por empleado-mes, no conteos absolutos

**Área:** eda | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Toda comparación de incidencia entre grupos (área, turno, banda de antigüedad, decil de horas extra) se expresa como **tasa cada 1.000 empleado-mes**, dividiendo los eventos por la exposición real del grupo en el panel.

**Alternativa descartada:** Comparar conteos absolutos de incidentes por grupo, que es como vienen naturalmente de un `value_counts()` sobre la tabla de eventos.

**Por qué la descartamos:** Los grupos tienen exposiciones muy distintas y el ranking se invierte. Ensamble tiene 14 incidentes absolutos y Calidad 3, lo que sugiere que Ensamble es cuatro veces peor; normalizado por empleado-mes las tasas son 19,6 y 15,5 — la brecha real es del 26%, no del 366%. En el caso del turno el efecto es aún más marcado: `Administrativo` acumula 8 incidentes absolutos, pero sobre 2.099 empleado-mes su tasa (3,8) es la tercera más baja.

**Conclusión:** Nunca comparar conteos de eventos entre grupos de tamaño distinto. Siempre construir explícitamente el denominador de exposición (empleado-mes del panel, no headcount al cierre) y expresar la métrica como tasa. Verificar que el denominador cubra el mismo período que el numerador antes de dividir.

---

## DEC-008: Brecha salarial por OLS multivariado, no diferencia de medias

**Área:** eda | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** La brecha salarial de género se estima con una regresión OLS de `log(salario_base_mensual)` contra género, nivel jerárquico, área, antigüedad, edad y rating de performance (n = 562, R² = 0,865). Se reportan además las brechas dentro de cada nivel jerárquico como control parcial. La diferencia de medias se muestra solo etiquetada como "cruda — no usar sola".

**Alternativa descartada:** Reportar la brecha como diferencia de salarios promedio entre mujeres y hombres (0,9%).

**Por qué la descartamos:** La media simple confunde el efecto del género con la composición de la plantilla — mezcla de niveles jerárquicos, áreas y antigüedades. Con una distribución distinta por área (Ensamble 26,8% de mujeres, Estampado 46,6%) y salarios que varían 45% por cada nivel jerárquico, la brecha cruda puede reflejar segregación ocupacional en lugar de trato desigual. Es la diferencia entre "las mujeres cobran menos" y "las mujeres están en puestos que pagan menos" — dos problemas distintos con dos remedios distintos. El resultado ajustado (0,02%, t = −0,03) permite afirmar ante una auditoría que el género no explica el salario, cosa que la media simple no sostiene.

**Conclusión:** Nunca reportar una brecha salarial como diferencia de medias. Siempre controlar por nivel, área y antigüedad como mínimo, y reportar cruda y ajustada juntas para que se vea cuánto de la brecha es composición. Si el n por celda cae por debajo de 5 en un corte like-for-like, omitir esa celda en vez de publicar un porcentaje sobre ruido.

---

## DEC-009: Reportar en negativo el business case de horas extra

**Área:** evaluacion | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** La oportunidad "sustituir horas extra por dotación" se presenta al directorio como **descartada, con flujo neto negativo en los tres escenarios** (−$15,7M / −$27,6M / −$39,4M anuales), acompañada del análisis de sensibilidad que muestra el punto de equilibrio. La preocupación por horas extra se reencuadra como riesgo operativo y de capacidad, no como bolsa de ahorro.

**Alternativa descartada:** Presentar la conversión de horas extra en contrataciones como oportunidad de ahorro, apoyada en la cifra de $988M anuales (8,3% de la nómina) y el equivalente de 34,8 FTE.

**Por qué la descartamos:** El recargo efectivo de la hora extra en los datos es **1,343x** el costo de la hora normal, mientras que el costo cargado de un empleado nuevo (cargas patronales + ART + aguinaldo + vacaciones) supera el 1,40x. El punto de equilibrio está en cargas del 34,3%: por debajo conviene contratar, por encima conviene la hora extra. En Argentina la condición no se cumple. Los argumentos de respaldo tampoco sobrevivieron: los sobrecargados crónicos rotan igual que el resto (19,7% vs 19,0%), su exceso de ausentismo es real pero marginal (+11,1%, t = 2,73, unos $4,75M anuales) y el vínculo con accidentes no es concluyente (ver DEC-004). La cifra de $988M es grande y tentadora, pero no es capturable.

**Conclusión:** Nunca convertir un costo grande en una oportunidad de ahorro sin calcular el costo de la alternativa. Siempre publicar el punto de equilibrio y el supuesto que lo mueve — acá, las cargas sociales — para que el directorio pueda revisar la conclusión si ese supuesto cambia. Si un business case da negativo, se reporta negativo: recomendar la acción intuitiva contra la evidencia propia destruye la credibilidad de todo el resto del informe.

**Lección aprendida:** La recomendación instintiva ("contratá gente en vez de pagar horas extra") era la que el cliente esperaba escuchar. El valor del análisis estuvo en poder demostrar que estaba mal, no en confirmarla.

**Código afectado:** `04_scripts/09_business_case.py`, `04_scripts/10_sensibilidad_he.py`.

---

## DEC-010: Clasificar por qué falta cada dato, antes de promediar nada

**Área:** calidad-datos | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Cada columna con casillas vacías se clasificó en uno de tres motivos: **no aplica** (la métrica no existe para ese grupo), **estructural** (falta por cómo está armado el registro) y **real** (vacío genuino). Las métricas de producción — desperdicio, unidades, eficiencia — se promedian solo dentro de las tres áreas donde existen.

**Alternativa descartada:** Dejar que el promedio saltee las casillas vacías por su cuenta, que es lo que hace la herramienta por defecto y sin avisar.

**Por qué la descartamos:** El desperdicio está vacío en el 0,1% de los registros de producción y en el 99,7% del resto. No es un dato perdido: es un dato que no aplica, porque las áreas administrativas no fabrican piezas y por lo tanto no generan desperdicio. Si se promedia sobre toda la empresa, el número describe solo a los operarios pero se presenta como si describiera a todos. Son dos poblaciones distintas mezcladas en un solo número.

**Conclusión:** Antes de calcular cualquier promedio, revisar si las casillas vacías se concentran en un grupo entero. Si un grupo está casi todo vacío y otro casi todo lleno, el dato no aplica a ese grupo: hay que sacarlo del universo, no promediarlo. Nunca dejar que el promedio decida solo qué filas ignora.

---

## DEC-011: Detectar los sueldos extremos pero no tocarlos

**Área:** calidad-datos | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** La regla estadística habitual marca 1.388 registros de sueldo (14,3%) como valores extremos. No se recortó ni se modificó ninguno: solo se agregó una columna que los señala.

**Alternativa descartada:** Recortar los sueldos más altos para que no distorsionen los promedios, que es el tratamiento estándar.

**Por qué la descartamos:** Los sueldos altos no son errores de carga: son los gerentes. El sueldo del medio sube de forma estricta con cada escalón jerárquico — $1,54M, $2,22M, $3,16M, $5,33M, $8,20M. Cada nivel paga más que el anterior, sin ninguna excepción. Recortarlos habría aplastado a la conducción contra el resto de la plantilla y roto el cálculo de brecha salarial, que justamente compara sueldos dentro de cada nivel.

**Conclusión:** Un valor extremo no es un error. Antes de recortar nada, verificar si los valores altos siguen algún orden conocido: jerarquía, antigüedad, categoría. Si lo siguen, son estructura real y se dejan como están. Alcanza con marcarlos en una columna aparte — quien después quiera excluirlos, puede.

---

## DEC-012: Nombres de columna sin eñes, identificadores como enteros

**Área:** calidad-datos | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Se renombraron `años_en_puesto_actual` y `horas_training_acumulado_año` a `anios_en_puesto_actual` y `horas_training_acumulado_anio`. Se convirtió `manager_id` de número con decimales a número entero que admite casillas vacías.

**Alternativa descartada:** Dejar las dos cosas como venían, ya que ninguna rompía el análisis actual.

**Por qué la descartamos:** Las dos son bombas de tiempo silenciosas. La eñe impide escribir el nombre de la columna de forma directa y falla al mover los datos entre sistemas que codifican los caracteres distinto. El identificador del jefe valía `1129.0` en vez de `1129`: al cruzarlo contra otra tabla que lo guarde como entero, el cruce no encuentra nada y devuelve una tabla vacía **sin dar ningún error**. Verificamos que ningún valor tiene decimales reales, así que convertirlo no pierde información.

**Conclusión:** Normalizar los nombres de columna apenas se cargan los datos: sin acentos, sin eñes, todo en minúscula. Guardar siempre los identificadores como enteros, nunca con decimales. Si el motivo del decimal eran las casillas vacías, usar el tipo entero que las admite.

---

## DEC-013: Revisar todas las columnas, no solo las que hacen falta

**Área:** eda | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Se agregó un paso que recorre las 95 columnas de las tres tablas, clasifica cada una por tipo y dispara alertas automáticas: más del 20% vacío, un solo valor que ocupa el 99% o más, categorías con menos del 1% de los casos, distribuciones con cola larga, y columnas con demasiados valores distintos. Levantó 54 alertas.

**Alternativa descartada:** Seguir con el enfoque anterior — ir directo a las preguntas de negocio y mirar solo las columnas que cada pregunta necesita.

**Por qué la descartamos:** El enfoque anterior encuentra las cosas solo si alguien las va a buscar. Dos de los hallazgos más importantes del informe aparecieron de casualidad, porque un número olió mal. La revisión sistemática los encuentra sola, en la primera pasada. De hecho descubrió algo que nadie había buscado: de los 45 incidentes de seguridad, solo 15 tienen acción correctiva registrada, y las 15 dicen exactamente la misma frase. No hay análisis de causa raíz — hay una respuesta refleja.

**Conclusión:** Antes de responder la primera pregunta de negocio, pasar por todas las columnas con alertas automáticas. Es más lento al principio y deja de depender de que al analista se le ocurra desconfiar justo del número correcto. Una alerta no es un error: es una columna que necesita una decisión explícita.

---

## DEC-014: Guardar la limpieza como receta, no como relato

**Área:** transversal | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Toda la limpieza quedó registrada en `transformaciones.json` como una lista ordenada de 31 pasos. Cada paso guarda qué operación se hizo, sobre qué columna, y con qué valores concretos.

**Alternativa descartada:** El registro anterior, que era una lista de frases describiendo en prosa lo que se había hecho.

**Por qué la descartamos:** Una persona entiende la prosa; un programa no puede reejecutarla. Cuando TechnoStamp mande los próximos seis meses de datos, nadie va a poder reaplicar la misma limpieza salvo que reconstruya a mano lo que hizo otro. Con la receta se corren los 31 pasos en orden y se obtiene exactamente el mismo tratamiento.

**Conclusión:** Guardar cada paso de limpieza con sus valores ya calculados, no con la instrucción que los calcula. Si mañana se rellenan casillas vacías con un promedio, guardar el número, no la palabra "promedio": así los datos nuevos reciben el mismo tratamiento que los viejos y no se mezcla información entre ambos.

---

## DEC-015: Presentar el ahorro como rango, no como cifra única

**Área:** evaluacion | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** El caso económico de retención se presenta como un rango de $23M a $195M anuales, con tres escenarios y sus supuestos escritos al lado. Se agrega además un piso verificable de $1,6M, que es lo que da el cálculo usando solo los datos que TechnoStamp mide.

**Alternativa descartada:** Publicar $92M anuales, que era la cifra única de la versión anterior.

**Por qué la descartamos:** Fuimos a ver de qué estaba hecho el costo por salida de $5,88M. Solo $200.000 vienen de datos del cliente — reclutamiento y onboarding. Los otros $5,68M son dos supuestos nuestros: cuánto sueldo se pierde mientras el puesto está vacío, y cuánto tarda un ingresante en rendir como el que se fue. Es el 97% del número. Moviendo esos supuestos dentro de rangos razonables, el ahorro anual va de $23M a $195M. Una cifra única esconde esa amplitud y la presenta como precisión que no existe. Un directorio que lo descubra por su cuenta desconfía del informe entero.

**Conclusión:** Antes de publicar cualquier cifra económica, desarmarla y calcular qué porcentaje viene de datos del cliente y qué porcentaje de supuestos propios. Si los supuestos pesan más que los datos, se publica un rango con los supuestos a la vista, nunca un promedio. Siempre agregar el piso que se sostiene solo con datos duros, e indicar qué le falta al cliente medir para cerrar el rango.

---

## DEC-016: Mostrar el margen de error en toda comparación entre grupos

**Área:** eda | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Cada comparación entre áreas o grupos lleva su margen de error, y solo se marca como problema aquello que se distingue del promedio de la compañía. Se retiraron dos afirmaciones que no pasaron ese control.

**Alternativa descartada:** Ordenar las áreas por porcentaje y marcar en rojo las más altas, que es lo que hacía la versión anterior.

**Por qué la descartamos:** Los grupos tienen tamaños muy distintos y un porcentaje sobre pocas personas dice poco. Al calcular el margen de error cayeron dos afirmaciones publicadas:

- **Estampado, 20,0% de rotación**, estaba marcado como área problemática. Su rango real va de 14,9% a 26,3% y contiene al promedio de la compañía (16,7%). No se puede afirmar que rote distinto.
- **"Los top performers rotan un 35% más"** era un hallazgo del informe. Los rangos se solapan: 14,7–36,0% contra 13,4–19,2%. Con 59 top performers la diferencia puede ser azar.

Mantenimiento Eléctrico, en cambio, aguantó: su rango va de 22,7% a 49,2%, y hasta el piso está por encima del promedio. Es la única área que se distingue.

**Conclusión:** Nunca marcar un grupo como problemático solo porque su porcentaje es el más alto de la lista. Calcular siempre el rango de error y marcar únicamente cuando el rango entero queda por encima del promedio. Con menos de 50 personas en un grupo, asumir que casi nada va a distinguirse y decirlo, en vez de presentar el porcentaje como si fuera un dato firme.

---

## DEC-017: Excluir enero 2024 del cálculo de rotación

**Área:** calidad-datos | **Fecha:** 2026-09-03 | **Estado:** Vigente

**Decisión:** Las 19 salidas de enero de 2024 se excluyen del cálculo de rotación. El período de análisis pasa a ser febrero 2024 – mayo 2025. La tasa corregida es 15,0% anual, no 16,5%.

**Alternativa descartada:** Contar los 17 meses completos, que es lo que hacía la versión anterior.

**Por qué la descartamos:** Enero de 2024 es el primer mes del archivo y registra 19 salidas, el triple de un mes normal. La prueba está en cuántos meses aparece cada persona antes de irse: **los 19 aparecen una sola vez**, sin ninguna excepción, contra 9,5 meses de todas las demás salidas. Son personas que ya estaban saliendo cuando se hizo el corte del archivo. No son rotación generada en el período: son arrastre.

Esto además corrigió una segunda afirmación equivocada. Con enero incluido, la rotación parecía estar bajando — y así se había interpretado. Sacando el arrastre, la tendencia es de +0,05 puntos por año, que es ruido, no tendencia. La rotación es plana. Las 19 salidas artificiales al principio del período dibujaban una caída que no existe.

**Conclusión:** En cualquier panel con fecha de corte, revisar siempre el primer y el último mes por separado antes de calcular tasas. Si los casos del primer mes aparecen una sola vez, son arrastre del corte y no pertenecen al período. Nunca leer una tendencia sin antes limpiar los bordes: un pico artificial en un extremo inventa pendientes que no están en los datos.

**Actualización (2026-09-06):** el "15,0% anual" de esta entrada usaba la tasa anualizada sobre dotación activa promedio (definición B). DEC-019 unificó el reporte de rotación en la tasa acumulada del período (definición A): con ese criterio, la corrección de esta decisión pasa a leerse **19,0% → 16,7%**, no 16,5% → 15,0%. La decisión de excluir el arrastre de enero no cambia; solo cambia la fórmula con la que se expresa el resultado. Ver DEC-019.

---

## DEC-018: Comunicar hallazgos ejecutivos como riesgos focalizados y verificables

**?rea:** transversal | **Fase:** Comunicaci?n ejecutiva | **Fecha:** 2026-09-05 | **Estado:** Vigente

**Decisi?n:** La s?ntesis para Martina Rosales, CEO y directorio se estructura en cuatro riesgos focalizados: rotaci?n en Mantenimiento El?ctrico, horas extra estructurales, seguridad nocturna y sucesi?n cr?tica. Cada insight debe incluir una conclusi?n titular, impacto de negocio, una evidencia visual simple y una o dos acciones correctivas concretas.

**Alternativa descartada:** Presentar el an?lisis como una secuencia de m?tricas de RR.HH., gr?ficos exploratorios o un pedido de aprobaci?n de un plan gen?rico de 90 d?as.

**Por qu? la descartamos:** La audiencia necesita entender qu? decisi?n merece atenci?n, no reconstruir el an?lisis desde la planilla. La evidencia disponible permite priorizar sin sobreactuar: Mantenimiento El?ctrico es la ?nica ?rea cuya rotaci?n se distingue del promedio; seguridad se sostiene en eventos auditables; las horas extra son un costo estructural, pero no un ahorro autom?ticamente capturable; y los puestos cr?ticos pr?ximos a jubilarse exponen continuidad operativa. Pedir aprobaciones o responsables sin cerrar el diagn?stico desplaza la conversaci?n desde la evidencia hacia burocracia.

**Conclusi?n:** Siempre presentar a C-level un insight como conclusi?n + impacto + evidencia + acci?n focalizada. Nunca usar un gr?fico como conclusi?n ni afirmar causalidad, ahorro garantizado o prioridad generalizada cuando los datos solo sostienen una se?al acotada.

**C?digo afectado:** `06_resultados/Discovery/conclusiones_ejecutivas_technostamp.md`, `06_resultados/Discovery/visualizaciones/`.

---

## DEC-019: Unificar la rotación en la tasa acumulada del período (16,7%)

**Área:** comunicación | **Fase:** Auditoría de calidad | **Fecha:** 2026-09-06 | **Estado:** Vigente

**Decisión:** Toda cifra de rotación anual de la compañía se reporta con una sola fórmula: **salidas del período limpio ÷ personas expuestas en ese período** (113 / 675 = **16,7%**). Es la misma fórmula que ya usaban las diez áreas individuales en `P5_rotacion_por_area_con_IC.csv` — incluido el 34,8% de Mantenimiento Eléctrico — y la que alimenta los intervalos de confianza de Wilson y el gráfico G9.

**Alternativa descartada:** Reportar la rotación anualizada sobre dotación activa promedio (113 salidas ÷ 16 meses × 12 ÷ 563 activos promedio = 15,0%), que es lo que usaba el titular del insight ejecutivo 1 y la Ficha A del informe técnico.

**Por qué la descartamos:** Con los mismos 113 casos convivían tres tasas defendibles (15,0% / 16,7% / 12,6%, según denominador y si se anualiza). El documento ejecutivo publicaba dos sin distinguirlas: el titular decía 15,0% y, dos párrafos abajo, la propia tabla de evidencia comparaba 16,7% contra el 34,8% de Mantenimiento Eléctrico. Como ese 34,8% ya estaba calculado con la fórmula acumulada (16/46), compararlo contra el titular de 15,0% inflaba la brecha de 2,08x a 2,32x. Además, la fórmula acumulada era la que de hecho sostenía todo el trabajo fino del proyecto — las diez áreas, los IC95, G9 — mientras que la anualizada se calculaba una sola vez, aparte, solo para el titular. Adoptarla como oficial significaba recalcular diez áreas para que coincidieran con el titular, en vez de corregir un solo titular para que coincida con el resto del análisis.

**Conclusión:** Cuando una tasa se reporta con más de una fórmula posible, adoptar la que ya sostiene el resto del análisis (comparaciones entre grupos, intervalos de confianza), no la que resulte más habitual para comunicar hacia afuera. Si en el futuro RR.HH. necesita una cifra anualizada para comparar contra un benchmark de industria, calcularla aparte y etiquetarla explícitamente como proyección — nunca reemplazar con ella la base de comparación entre áreas.

**Bug evitado:** Que el directorio viera dos tasas de rotación de la misma empresa en la misma slide y descartara el informe completo por esa sola inconsistencia.

**Código afectado:** `06_resultados/Discovery/conclusiones_ejecutivas_technostamp.md`, `06_resultados/Discovery/Discovery_report.md`, `04_scripts/16_rotacion_temporal.py`.

---

## DEC-020: Corregir por comparaciones múltiples (Bonferroni) sobre las diez áreas testeadas

**Área:** eda | **Fase:** Auditoría de calidad | **Fecha:** 2026-09-06 | **Estado:** Vigente

**Decisión:** `P5_rotacion_por_area_con_IC.csv` ahora incluye `p_valor` (bilateral, sobre el mismo z que ya se calculaba) y `sig_bonferroni`, que compara ese p contra 0,05 ÷ 10 áreas = 0,005. Mantenimiento Eléctrico tiene p = 0,00105: **sobrevive** la corrección con margen.

**Alternativa descartada:** Dejarlo como estaba — reportar el hallazgo con el z sin corregir (3,28) y declarar en el `ESTUDIO` que faltaba correr Bonferroni, sin correrlo.

**Por qué la descartamos:** El proyecto testea diez áreas contra el promedio de la empresa. Al umbral habitual del 5% por prueba, la chance de que **alguna** de las diez salga "significativa" por puro azar ronda el 40% — no el 5%. Bonferroni corrige eso bajando el umbral individual a 0,05 ÷ 10. No correrlo no invalidaba el hallazgo, pero lo dejaba con un asterisco implícito ("probablemente real") que un directorio no puede evaluar por su cuenta. Correrlo no pedía ningún dato nuevo — se calcula sobre el mismo z que ya existía en la tabla.

**Conclusión:** Cuando se testean más de dos grupos contra un mismo promedio, correr la corrección por comparaciones múltiples es tan barato como declarar que falta correrla. Si el hallazgo la sobrevive, queda más fuerte que antes; si no la sobrevive, es mejor saberlo antes de presentarlo. Nunca dejar un hallazgo con múltiples pruebas sin corregir solo porque "probablemente" alcanza.

**Código afectado:** `04_scripts/17_business_case_v2.py`, `06_resultados/Discovery/tablas_soporte/P5_rotacion_por_area_con_IC.csv`, `06_resultados/Discovery/Discovery_report.md`, `ESTUDIO_conceptos_technostamp.md`.

---

## DEC-021: Rehacer G11 por turno y tasa, no por area y conteo

**Área:** eda | **Fase:** Auditoría de calidad | **Fecha:** 2026-09-06 | **Estado:** Vigente

**Decisión:** El gráfico G11 pasa de mostrar incidentes por área y severidad (conteo bruto) a mostrar la **tasa de incidentes cada 1.000 empleado-mes por turno**, con el turno noche destacado. Se persiste `tablas_soporte/P4_incidentes_por_turno.csv` (emp_meses, incidentes, días perdidos, tasa) generado por `07_verif_incidentes_p5.py`, que ya calculaba esta tasa para el cuerpo del informe pero nunca la guardaba en un archivo.

**Alternativa descartada:** Mantener G11 como estaba (área y severidad en conteo) y agregar una tabla aparte con la tasa por turno, como sugería una nota previa del propio informe.

**Por qué la descartamos:** El insight ejecutivo 3 titula sobre el turno noche, y G11 era el "visual de soporte" citado para ese insight — pero mostraba área, no turno, y en conteo bruto. Dos problemas, no uno: (1) el gráfico no probaba el titular que ilustraba; (2) el conteo bruto viola DEC-007 ("nunca comparar conteos de eventos entre grupos de tamaño distinto") — Ensamble mostraba 14 incidentes contra 3 de Calidad, sugiriendo 4,7x, cuando la tasa real es 26% de diferencia. Agregar una tabla aparte dejaba el gráfico principal sosteniendo un titular que no le corresponde; reemplazarlo resuelve las dos cosas con un solo cambio.

**Conclusión:** Cuando un gráfico se cita como evidencia de un hallazgo, verificar que la variable que titula sea la variable que el gráfico grafica. Si no lo es, no alcanza con agregar una aclaración al pie: hay que reemplazar el gráfico. El cálculo correcto ya existía en el proyecto (impreso por consola desde el discovery original) — el error no era de análisis, era de qué cálculo se convirtió en visual y cuál se quedó en el stdout.

**Código afectado:** `04_scripts/07_verif_incidentes_p5.py` (persiste `P4_incidentes_por_turno.csv`), `04_scripts/18_visualizaciones_decision.py` (rehace G11, ahora `G11_incidentes_por_turno.png`), `06_resultados/Discovery/conclusiones_ejecutivas_technostamp.md`.

---

## DEC-022: Declarar los dos límites del hallazgo de seguridad nocturna en la propia slide

**Área:** comunicación | **Fase:** Business case | **Fecha:** 2026-09-07 | **Estado:** Vigente

**Decisión:** El hallazgo del turno noche se presenta como **tasa de incidentes** (11,8 vs 2,2 cada 1.000 empleado-mes, 5,4x, sobre exposiciones comparables), con dos límites declarados en la misma slide y no en un apéndice: (1) el turno registrado es el **asignado a la persona**, no el del hecho; (2) la concentración de casos graves en la noche es un **conteo**, no un patrón demostrado. Los días perdidos y los casos graves se presentan como **impacto observado** del hallazgo, no como un segundo hallazgo con entidad propia.

**Alternativa descartada:** Presentar "el turno noche concentra el riesgo severo" como una conclusión con entidad propia, apoyada en que 5 de los 6 casos graves y 102 de los 138 días perdidos son nocturnos.

**Por qué la descartamos:** Al ir a verificar el dato antes de ponerlo en una slide aparecieron dos cosas. **Primera:** `turno_evento` coincide con `turno_trabajo` del panel en **45 de 45 casos** —coincidencia perfecta, así que es el turno asignado, no un dato levantado del accidente— y `hora_evento` de los 25 incidentes rotulados "Noche" va de las **06:53 a las 22:00**: en todo el dataset no hay un solo incidente entre las 23:00 y las 06:00. **Segunda:** la concentración de gravedad no se distingue del azar. Fisher exacto bilateral sobre graves (5 vs 1) da **p = 0,205**, y sobre incidentes con días perdidos (10 vs 5) da **p = 0,352**. Los incidentes leves se reparten **15 y 15**, exactamente iguales.

Nada de esto toca el hallazgo principal, que está calculado sobre 45 casos con exposición comparable y sigue en pie. Pero afirmar que los accidentes ocurren de madrugada, o que la gravedad se concentra en la noche, son dos generalizaciones que un directorio desarma con una pregunta — y que además llevarían la auditoría hacia la hipótesis equivocada.

**Conclusión:** Antes de convertir un hallazgo en slide, verificar **qué mide exactamente cada campo que lo sostiene**, no solo que el cálculo esté bien. Un campo que coincide al 100% con otro no es una medición independiente. Y distinguir siempre **reportar un conteo observado** de **afirmar un patrón**: lo primero necesita que el número esté bien; lo segundo necesita que sobreviva a un test. Declarar el límite primero es lo que vuelve creíble el resto, y acá además refuerza el pedido: hay una diferencia grande, real y medida, y ningún dato disponible que la explique.

**Código afectado:** `06_resultados/Discovery/business_case/02_guion_ejecutivo.md` (§A.2, A.4, A.7), `01_matriz_evidencia.md`, `06_resultados/Discovery/Discovery_report.md`, `06_resultados/Discovery/conclusiones_ejecutivas_technostamp.md`.

---

## DEC-023: Retirar `meses_desde_ultimo_aumento` como variable de cualquier análisis de rotación

**Área:** calidad-datos | **Fase:** Business case | **Fecha:** 2026-09-07 | **Estado:** Vigente

**Decisión:** El campo `meses_desde_ultimo_aumento` **no se usa** como variable en ningún análisis de rotación ni como feature en ningún modelo futuro. El patrón que mostraba —1,0 mes en renuncias voluntarias contra 4,5 en activos— es un **artefacto de registro**, no una señal de comportamiento.

**Alternativa descartada:** Tratarlo como la señal de fuga temprana más discriminante del dataset y construir sobre él un tablero de retención, previa auditoría con RR.HH.

**Por qué la descartamos:** Abriendo el campo por motivo de salida, el patrón se repite en los cinco motivos: renuncia voluntaria 1,03 · despido 0,96 · **jubilación 1,43** · reestructuración 1,40 · fin de contrato 0,50. Y el número que cierra la discusión: **ninguna de las 132 bajas supera el valor 3**, mientras que **183 de 562 activos sí** lo superan (activos: media 4,53, mediana 2,0, máximo 17 — que es exactamente el largo del panel).

Si el aumento reciente fuera un predictor de renuncia, el patrón sería específico de las renuncias voluntarias. No lo es. **Nadie se jubila porque le dieron un aumento hace un mes**, y sin embargo los siete jubilados del período muestran el mismo perfil que los 89 renunciantes. El campo se reescribe o se trunca en el momento de registrar la baja, para todas las bajas por igual.

**Conclusión:** **Cuando una variable separa demasiado bien, la primera pregunta no es "qué buen predictor" sino "¿cuándo se escribe este dato?".** Un campo cuyo contenido depende del acto administrativo de registrar el desenlace está prediciendo el registro, no el fenómeno — es fuga de la variable objetivo disfrazada de hallazgo de negocio. La prueba diagnóstica es barata: abrir la variable por categorías del desenlace que *no* deberían compartir el patrón. Si lo comparten, es artefacto.

**Bug evitado:** Entrenar un modelo de retención que hubiera parecido excelente en validación y no habría predicho nada, porque su mejor variable era un subproducto de dar de baja.

**Código afectado:** `06_resultados/Discovery/business_case/03_insights_nuevos.md` (I12), `04_puente_discovery_automation.md` (entregas 6 y 8).

---

## DEC-024: Rehacer G12 sobre el cruce temporal y la cobertura, no sobre correlación por área

**Área:** eda | **Fase:** Business case | **Fecha:** 2026-09-07 | **Estado:** Vigente

**Decisión:** G12 pasa de un scatter de horas de capacitación contra incidentes por área —titulado "más capacitación coincide con más incidentes (se entrena después del accidente, no antes)"— a dos paneles: el **cruce temporal** sobre los 45 incidentes y la **cobertura** de capacitación entre accidentados y no accidentados. Nuevo archivo: `G12_cobertura_capacitacion_seguridad.png`.

**Alternativa descartada:** Conservar el scatter agregándole una etiqueta al pie que aclarara que no prueba causalidad.

**Por qué la descartamos:** El título afirmaba dos cosas y ninguna se sostiene. **Una:** la correlación área a área entre horas de capacitación por empleado y tasa de incidentes es **r = 0,394 con p = 0,260** sobre 10 áreas — no se distingue de cero (sin Logística, que con 35,2 h por empleado es un caso aparte, baja a r = 0,279). **Dos:** la temporalidad nunca se había calculado. El código agregaba totales de todo el período por área; **no comparaba una sola fecha**.

Corrido el cruce con los archivos que ya existían —`capacitaciones_limpio.parquet` tiene `fecha_inicio` y `fecha_fin`; `eventos_limpio.parquet` tiene `fecha_evento`—: de los 45 incidentes, **5 tenían capacitación previa, 4 posterior y 36 (80%) ninguna**. "Se entrena después del accidente" describe **4 casos de 45**, y esos cuatro recibieron el curso a una mediana de **108 días** del hecho (máximo 344): es el calendario normal, no una reacción. A nivel persona, los accidentados tienen capacitación en el **22,0%** de los casos contra **19,1%** de los no accidentados (Fisher, **p = 0,683**), que es la proporción de toda la empresa (**19,3%**).

Una etiqueta al pie no arregla un título que afirma lo contrario de lo que muestran los datos. El hallazgo que sí se sostiene —**la capacitación de seguridad cubre al 19,3% de la gente y se asigna sin ninguna relación con quién se lastima**— es más fuerte y más accionable que la brecha de medición que se había publicado.

**Conclusión:** Un gráfico que se cita como evidencia debe graficar la variable de la que habla su título (DEC-021), y su título no debe afirmar una relación temporal que el código no calculó. Antes de escribir "después" o "antes" en un titular, verificar que exista una comparación de fechas en el código. Y **antes de declarar una brecha de datos, agotar los archivos que ya están en la mesa**: este cruce no necesitaba ningún dato nuevo.

**Código afectado:** `04_scripts/18_visualizaciones_decision.py`, `06_resultados/Discovery/Discovery_report.md`, `06_resultados/Discovery/business_case/` (guion §C.3, matriz, insights I8).

---

## DEC-025: Presentar la sucesión sobre jubilación a 12 meses, sin el rótulo "posiciones críticas"

**Área:** comunicación | **Fase:** Business case | **Fecha:** 2026-09-07 | **Estado:** Vigente

**Decisión:** El insight de sucesión se presenta sobre **jubilación a 12 meses en la dotación activa** — cuatro personas, tres puestos — conservando la tabla de cobertura por puesto y **retirando el rótulo "posiciones críticas"**. El visual pasa de un scatter a **tarjetas de alerta** (`G13_alerta_sucesion.png`) que muestran dotación, personas que se jubilan y sucesores potenciales de cada puesto.

**Alternativa descartada, en dos pasos.** Primero: la versión previa, "cuatro de las cinco **posiciones críticas** activas se jubilan en 12 meses o menos". Segundo, y este fue un error propio del business case: reemplazar toda esa sección por el único caso del Supervisor de Logística, descartando la tabla de tres puestos por considerarla apoyada en el flag.

**Por qué la descartamos:** El rótulo estaba mal, pero **la tabla estaba bien**, y hubo que corregir la corrección. Las cuatro personas que se jubilan a 12 meses y los tres puestos que ocupan están verificados sobre `meses_hasta_jubilacion` en los 562 activos. Lo que no corresponde es llamarlas "posiciones críticas": ese rótulo importa `es_posicion_critica`, que DEC-006 descartó por marcar 10 de 694 (1,4%) y no cambiar en 17 meses.

La confusión de fondo era que dos análisis distintos daban números distintos y se los estaba tratando como si respondieran lo mismo. `P1_riesgo_sucesion_por_puesto.csv` cruza el índice propio de criticidad con jubilación a **24** meses y devuelve **un** puesto; la pregunta de Martina era a **12** meses y sin filtro de criticidad, y devuelve **tres**. Las dos son correctas. Mezclarlas fue lo que produjo primero una afirmación inflada y después una recortada de más.

**Conclusión:** Cuando dos cálculos sobre el mismo tema devuelven números distintos, la respuesta casi nunca es elegir uno: es escribir al lado de cada uno **qué pregunta contesta**, con su filtro y su horizonte. Y al corregir una afirmación, separar el **rótulo** del **cálculo**: retirar una etiqueta mal puesta no es motivo para descartar la tabla que la acompañaba. La criticidad defendible acá es la observable —cuánta gente ocupa el puesto y cuántos quedan si esa persona se va—, no un flag sin mantener.

**Código afectado:** `04_scripts/18_visualizaciones_decision.py` (G13 sobre base de jubilación a 12 meses), `06_resultados/Discovery/conclusiones_ejecutivas_technostamp.md` (§4), `06_resultados/Discovery/business_case/` (guion §B.4, matriz, insights I9).

---

## DEC-026: Retirar el gradiente de riesgo de accidente por antigüedad

**Área:** eda | **Fase:** Business case | **Fecha:** 2026-09-07 | **Estado:** Vigente

**Decisión:** Se retira la afirmación "el riesgo de accidente sube con la experiencia" y su explicación por **complacencia del personal experimentado**. El hallazgo se reformula en su valor real, que es **negativo**: refuta que los ingresantes sean el problema de seguridad, sin establecer ningún gradiente.

**Alternativa descartada:** Mantener la lectura de la tabla de tasas por banda de antigüedad (0,0 · 0,0 · 5,2 · 3,7 · 5,1 · 7,0 cada 1.000 empleado-mes) como evidencia de que el riesgo crece con los años.

**Por qué la descartamos:** La tabla está bien construida —normalizada por exposición, como manda DEC-007—, pero el gradiente que se le leyó no está. Un chi-cuadrado de homogeneidad sobre las seis bandas da **5,68 con 5 grados de libertad, p = 0,339**: las tasas no se distinguen entre sí. Y la serie ni siquiera es monótona, cae de 5,2 a 3,7 antes de volver a subir. Los ceros de las dos primeras bandas tampoco prueban nada: con 449 y 188 empleado-mes de exposición, lo esperable bajo tasa pareja son ~2 y ~1 incidentes, así que observar cero es compatible con el azar.

Es el mismo error que DEC-016 corrigió para Estampado y para los top performers: ordenar por valor y leer una tendencia sin calcular el margen. Con 45 eventos repartidos en seis bandas, ninguna comparación por antigüedad va a distinguirse de nada.

**Conclusión:** Una tabla correctamente normalizada no vuelve correcta cualquier lectura de esa tabla. Antes de afirmar una tendencia sobre categorías ordenadas, correr un test de homogeneidad — y desconfiar especialmente cuando la serie no es monótona, que es la señal más barata de que se está leyendo ruido. Y cuidado con la explicación causal que viene pegada: "complacencia del personal experimentado" era una historia atractiva sobre un efecto que no existía.

**Lo que sí conserva valor:** el accidentado más nuevo tenía 14 meses de antigüedad y la mediana de los accidentados es de 79 meses. Eso alcanza para **no** invertir en inducción como respuesta al problema de seguridad, que era la conclusión a la que llevaba la columna del panel mensual (con esa fuente los ingresantes parecían accidentarse a 10 veces el promedio — ver DEC-004). Un hallazgo negativo bien establecido vale tanto como uno positivo.

**Código afectado:** `06_resultados/Discovery/Discovery_report.md` (§6), `06_resultados/Discovery/business_case/03_insights_nuevos.md` (I7), `04_puente_discovery_automation.md` (entrega 9).

---

## DEC-027: Ningún insight del proyecto justifica pasar a Automation

**Área:** transversal | **Fase:** Business case | **Fecha:** 2026-09-07 | **Estado:** Vigente

**Decisión:** Los doce insights del Discovery se evaluaron uno por uno contra el criterio de `ESTUDIO_conceptos_technostamp.md` §1 —frecuencia de decisión, escala, y si el cuello de botella es velocidad de scoring o calidad de inferencia—. **Los doce dan `ninguno — sigue siendo Discovery`. Cero etapas `ds-*` habilitadas.** Cada veredicto negativo se publica con su **umbral**: qué tendría que cambiar para revisarlo.

**Alternativa descartada:** Derivar al menos un proyecto supervisado de los dos candidatos obvios — un modelo de riesgo de fuga sobre la rotación, o uno de riesgo de accidente sobre seguridad.

**Por qué la descartamos:** Ninguno de los dos sobrevive a los números. **Rotación:** la clase positiva real —renuncias voluntarias, que es lo único que una acción de retención puede evitar— son **89 casos en toda la empresa** y **11** en Mantenimiento Eléctrico, contra **60 columnas candidatas** en el panel; y la etiqueta está mal definida por censura a derecha, porque un activo no es un "no se va" sino un "todavía no se fue". **Seguridad:** 45 incidentes en 9.601 empleado-mes (tasa base 0,47%), repartidos en **41 personas distintas con solo 3 reincidentes** — no hay señal individual persistente que aprender.

Pero el motivo de fondo no es el tamaño de muestra: en los cuatro casos principales **falta el dato que explicaría el fenómeno, no el algoritmo que lo predeciría**. No hay entrevistas de salida (no se sabe *por qué* se van) ni ficha de causa raíz (no se sabe *por qué* pasan los accidentes). Un modelo entrenado sobre lo que hay automatizaría una decisión que todavía nadie sabe tomar.

Y hay una razón que no es estadística: en seguridad **la acción correctiva no es individual**. Lo que se recomienda —revisar dotación, supervisión, tareas, mantenimiento y relevo del turno noche— se ejecuta sobre el turno. Un score de riesgo por operario no cambiaría ninguna de esas decisiones, y pondría un número de "probabilidad de accidentarse" al lado del nombre de un trabajador cuando lo que falla es la configuración del turno.

**Conclusión:** No recomendar ML porque sea técnicamente posible. Evaluar las tres condiciones por separado y ser explícito sobre cuál falla, porque cada una se destraba distinto: el volumen solo con más años u otra escala; la falta del dato explicativo con control de proceso en el sistema origen, que no es analítica; y un problema que en realidad es de medición o de gestión, midiendo o decidiendo. **Y publicar siempre el umbral: un "no" sin umbral es una opinión, no un veredicto.**

**El próximo paso de TechnoStamp no es un modelo:** es un formulario de incidentes que pida la causa y una entrevista de salida que pida el motivo.

**Código afectado:** `06_resultados/Discovery/business_case/04_puente_discovery_automation.md` (entregas 6 a 9 y cierre), `03_insights_nuevos.md`.

---

## DEC-028: Actualizar la celda 33 del notebook a los nombres de gráfico vigentes

**Área:** trazabilidad | **Fase:** Auditoría de valor agregado | **Fecha:** 2026-09-08 | **Estado:** Vigente

**Decisión:** La celda 33 de `Technostamp_Completo.ipynb` debe actualizarse para pedir `G12_cobertura_capacitacion_seguridad.png` y `G13_alerta_sucesion.png` — los nombres vigentes desde DEC-024 y DEC-025 — en lugar de `G12_capacitacion_seguridad_vs_incidentes.png` y `G13_riesgo_sucesion_por_puesto.png`.

**Alternativa descartada:** Dejar el notebook como está, ya que el output guardado de la celda todavía muestra las imágenes (capturadas antes del rename).

**Por qué la descartamos:** `mostrar_graficos()` hace `raise FileNotFoundError` si el archivo no existe, y `06_resultados/Discovery/visualizaciones/` solo contiene los nombres nuevos. El commit que renombró los archivos (`1d8ad5a`, 2026-09-07 15:00) es posterior al último commit que tocó el notebook (`b4f3360`, 11:34). Si alguien re-ejecuta el notebook completo hoy, se corta en la celda 33 — la misma clase de falla que ya rompió la celda 24 antes de corregirse (ver `06_backlog_priorizado.md`, ítem 1).

**Conclusión:** Cada vez que un script de visualización cambie el nombre de un archivo de salida, revisar en el mismo commit todas las celdas del notebook que lo referencian por nombre. Un rename de archivo es un cambio de contrato, igual que un rename de columna.

**Bug evitado:** Que el próximo que reejecute el notebook completo se encuentre con un `FileNotFoundError` sin contexto, en vez de una explicación.

**Código afectado:** `03_notebooks/Technostamp_Completo.ipynb` (celda con `mostrar_graficos([...])` después de `ejecutar_etapa("18_visualizaciones_decision.py")`).

---

## DEC-029: Anotar en la celda 13 del notebook que dos de sus tablas están retiradas

**Área:** trazabilidad | **Fase:** Auditoría de valor agregado | **Fecha:** 2026-09-08 | **Estado:** Vigente

**Decisión:** La celda 13 (`04_scripts/06_p3_p4_p5.py`) necesita una nota que marque como retiradas dos de sus tablas: la tasa de incidentes por antigüedad calculada sobre la columna del panel (el "78,0 ×1.000 en los primeros 6 meses" que DEC-004 ya descartó) y la comparación de `meses_desde_ultimo_aumento` entre salidas y activos (el patrón que DEC-023 prohibió usar). Ninguna de las dos debe leerse sin la corrección que aparece después, en las celdas 15 y 29.

**Alternativa descartada:** Dejar la celda como está, confiando en que `decisions.md` ya documenta el retiro de ambos hallazgos.

**Por qué la descartamos:** El notebook no se corrió nunca de punta a punta en una sola pasada (`execution_count` no es monótono entre celdas), así que nadie tuvo la oportunidad de notar que la celda 13 contradice a las celdas 15 y 29 que vienen después. Un lector que se detiene en la celda 13 —o que la lee antes que las otras— se lleva el hallazgo falso sin ver la corrección. `decisions.md` documenta el retiro, pero el notebook es el artefacto que efectivamente ejecuta y muestra el número retirado.

**Conclusión:** Cuando `decisions.md` retira un hallazgo, buscar todas las celdas del notebook que lo reproducen —no solo el script que lo originó— y agregarles una nota o sacarlas de la lectura principal. Una decisión escrita en `decisions.md` no corrige por sí sola el artefacto que la contradice.

**Bug evitado:** Que alguien —cliente, auditor externo, o el propio equipo dentro de seis meses— lea el notebook de arriba hacia abajo y se lleve dos conclusiones ya refutadas como si siguieran vigentes.

**Código afectado:** `03_notebooks/Technostamp_Completo.ipynb` (celda con `ejecutar_etapa("06_p3_p4_p5.py")`); considerar además corregir `04_scripts/06_p3_p4_p5.py` para que no calcule esas dos tablas sobre la fuente y la variable retiradas.

---

## DEC-030: Caracterizar la hora extra como déficit de dotación estructural, no como volatilidad de demanda

**Área:** evaluación | **Fase:** Preguntas C-level (Q2) | **Fecha:** 2026-09-08 | **Estado:** Vigente

**Decisión:** La hora extra de las seis áreas cargadas se describe como un déficit de dotación permanente, no como una respuesta operativa a la carga. La evidencia: la hora extra por persona es plana los 17 meses del panel (coeficiente de variación 0,01–0,05 en Estampado, Ensamble, Pintura, Logística y Mantenimiento Mecánico; 0,22 en Mantenimiento Eléctrico y solo por un pico de tres meses), el R² de la hora extra contra la producción es 0,00–0,08 en las áreas planas, y la producción cayó en el período (Estampado −7 %, Pintura −12 %) sin que la hora extra se moviera. Es aditiva a la jornada (correlación intra-persona 0,03 con `horas_trabajadas`, mediana 165 h/mes contra un turno teórico de 168). Equivale al 6,2 % de las horas-plantel estándar: **24 a 34 operarios-equivalente en producción, 670 MM $/año** (35 a 50 personas y 985 MM $/año en toda la planta).

**Alternativa descartada:** Mantener el encuadre de DEC-009 sin matiz: "la hora extra no se convierte en dotación porque el recargo efectivo (1,343x) es menor al costo cargado de un ingresante (>1,40x), y el punto de equilibrio de cargas del 34,3 % no se cumple en Argentina".

**Por qué la descartamos:** DEC-009 compara hora extra *flexible* —la que se prende y se apaga con la carga— contra una contratación al margen. Este análisis muestra que la hora extra de TechnoStamp no es flexible: es un nivel fijo de alrededor del 7 % sostenido 17 meses corridos, que no baja ni cuando baja la producción. Con esa característica el 1,343x deja de ser la comparación relevante: no se está comprando capacidad flexible, se está postergando una decisión de dotación. Y el recargo no incluye los costos que el propio DEC-009 (detalle) identificó como el caso económico real —más fatiga y más ausentismo en los sobrecargados crónicos— ni el scrap, que es la pregunta abierta Q3. DEC-030 no revierte DEC-009: lo condiciona a que la comparación se rehaga con el encuadre estructural y con los costos colaterales sumados.

**Observación secundaria:** la detección genérica de picos (mes-área por encima del +25 % de su propia mediana) marca solo a Mantenimiento Eléctrico en febrero, marzo y abril de 2025 (+70 %, +67 %, +39 %). Es un evento puntual —proyecto, falla mayor o ausencias en cadena—, en la misma área que ya tiene la peor rotación (DEC-019, DEC-020) y la cola larga de hora extra. Amerita una conversación aparte con el área.

**Conclusión:** Antes de clasificar un costo recurrente como flexible, verificar que efectivamente varíe con su driver. Un costo que se mantiene plano durante 17 meses mientras su supuesto driver sube y baja es estructural por definición, y la decisión que exige no es "pagarlo o no" sino "cerrar el déficit o no".

**Código afectado:** `04_scripts/19_hora_extra_estructural.py` (nuevo); `03_notebooks/Technostamp_Completo.ipynb` (sección 10b con `ejecutar_etapa("19_hora_extra_estructural.py")` y registro en `ETAPAS_EJECUTADAS`); `04_scripts/08_visualizaciones.py` (bloques G8 y G9); `06_resultados/Discovery/visualizaciones/G8_hora_extra_no_se_mueve.png` y `G9_hora_extra_en_personas.png`; `06_resultados/Discovery/tablas_soporte/P3b_hora_extra_estructural.csv` y `P3b_hora_extra_picos.csv`. El número firme es el porcentaje de horas-plantel; el conteo de FTE es un rango porque el techo supone una curva de aprendizaje del ingresante (factor 0,70) y N2 —meses hasta rendimiento pleno— no está medido.

---

## DEC-031: `es_top_performer` es el rating de un mes, no un rasgo estable de la persona

**Área:** calidad-datos | **Fase:** Preguntas C-level / revisión de flags de negocio | **Fecha:** 2026-09-08 | **Estado:** Vigente

**Decisión:** `es_top_performer` no se usa como grupo estable en ningún análisis de rotación, riesgo o criticidad. Es una recodificación de `rating_performance == 5` en el snapshot mensual: coincide con rating 5 en 790 de 794 filas-mes y en 0 de las aproximadamente 8.900 filas con rating menor o igual a 4. Es un flag mensual y volátil: cambia a lo largo del panel para 344 de 694 empleados (cerca del 50 %), y los 349 alguna vez marcados promedian un `perf_prom` de 3,4 sobre 5 en su carrera contra 3,0 del resto. En la tabla nivel-persona (DEC-005) se toma del `tail(1)`, así que para quien se fue es el rating del mes de salida.

**Alternativa descartada:** Seguir usando el flag tal cual para comparar rotación entre "top performers" y "resto", y como componente `crit_top_performer` del índice de criticidad propio (DEC-006).

**Por qué la descartamos:** El hallazgo "los top performers rotan un 35 % más" ya había sido retirado por DEC-016 por intervalos solapados. Al revisarlo caso por caso aparece una segunda razón: es un artefacto de definición. Recalculada la rotación con definiciones de excelencia sostenida —`perf_prom` mayor o igual a 4,5 (n = 8) o al menos 6 meses con rating 5 (n = 15)— la rotación de ese grupo es 0 %; solo la definición ruidosa del flag mensual produce la diferencia de 23,7 % contra 16,1 %. De las 14 salidas marcadas como top performer, 4 son despidos (2 con 15 y 16 días de ausencia), 1 es jubilación y solo 9 son renuncias voluntarias, con el mismo mix de motivos que el resto de la empresa (64 % voluntario en ambos grupos). El componente `crit_top_performer` —`(no salió) y es_top_performer`— arrastra el mismo ruido al índice de 47 críticos de DEC-006: recalculado con `perf_prom` mayor o igual a 4,5, el índice baja a 35.

**Conclusión:** Para comparar rotación, riesgo o criticidad por desempeño, definir el grupo con una métrica de carrera —media de `rating_performance` a lo largo del panel, o cantidad de meses en el nivel máximo—, nunca con un flag de un solo período. Un flag que cambia para la mitad de la población en 17 meses no describe un rasgo, describe un estado.

**Código afectado:** `04_scripts/13_limpieza_v2.py` (definición de `crit_top_performer` y del `score_crit`), `04_scripts/05_verif_critica.py`, `04_scripts/08_visualizaciones.py` (panel de top performers en G6), `04_scripts/17_business_case_v2.py` (comparación top performers vs resto). Nota: `perf_prom` ya existe en `empleados_nivel_persona.parquet` como agregado del historial (DEC-005), así que la métrica de reemplazo no requiere ningún dato nuevo.

---

## DEC-032: Costo laboral por pieza — análisis descriptivo, sin número para el efecto de la rotación

**Área:** evaluación | **Fase:** Preguntas C-level (Q1) | **Fecha:** 2026-09-08 | **Estado:** Vigente

**Decisión:** La pregunta Q1 —¿cuánto cuesta, en mano de obra, una pieza que sale bien, y cómo varía ese costo?— se responde con estadística descriptiva sobre 51 filas área-mes de Estampado, Ensamble y Pintura. Se publica: el costo laboral por pieza buena es de alrededor de $1.986 (Estampado $2.075; Ensamble y Pintura $1.940), subió aproximadamente 17 % de punta a punta del panel, y esa suba se descompone en aproximadamente mitad menor productividad física —piezas por persona-hora, que cayó 3 a 8 % según el área— y mitad mayor precio de la hora. El scrap es del 2,3 % y agrega entre $37 y $54 por pieza buena. **No se publica** ningún número de "cuánto cuesta la rotación por pieza".

**Alternativa descartada:** La primera versión del script regresaba el costo laboral por pieza contra la rotación, la hora extra y el ausentismo del mes, sin control de tiempo, y comparaba los meses del cuartil superior de rotación contra los del cuartil inferior. Esa comparación daba "+5,0 % de sobrecosto por pieza en los meses de rotación alta", que se estuvo a punto de traducir a "unos $191 MM/año atribuibles a la rotación".

**Por qué la descartamos:** Dos problemas, y los dos hacen que ese +5 % no signifique lo que parece.

Primero, el tiempo. El costo por pieza subió aproximadamente 17 % a lo largo de los 17 meses, sobre todo porque la producción cayó mientras el gasto de sueldos se mantuvo casi plano (mismo fenómeno de DEC-030 visto desde el costo unitario). Y los meses de rotación alta son los del final del período. Así que "meses de rotación alta" y "meses tardíos, más caros" son casi el mismo conjunto: la comparación de cuartiles estaba midiendo la tendencia temporal y etiquetándola como rotación. Al agregar el índice de mes a la regresión, el R² sube de 0,49 a 0,84 —la tendencia hacía casi todo el trabajo— y el coeficiente de la rotación queda en t = −0,55, indistinguible de cero. Rehecha la comparación de cuartiles sobre los residuos de la tendencia, el +5,0 % se reduce a +0,8 %.

Segundo, la circularidad. `costo_total_mes` es `salario_base_mensual + costo_horas_extra`, así que el numerador del costo por pieza ya contiene el costo de la hora extra. Regresar el costo por pieza contra las horas extra es en parte una identidad contable, no un hallazgo; y el ausentismo aparece con signo invertido porque una ausencia no paga baja el gasto del mes. La variable de salida se cambió a la **productividad física** —unidades por persona-hora trabajada—, que no se construye con la nómina, de modo que la pregunta ("¿la rotación y el ausentismo reducen la producción por hora?") queda separada de la contabilidad. El costo por pieza se reconstruye aparte como `precio_hora / productividad`.

**Conclusión:** Para preguntar si una variable X encarece la producción: (1) controlar el paso del tiempo antes de comparar períodos —es el mismo error de DEC-016 y DEC-026, leer una diferencia entre grupos sin descontar lo que ya se movía solo—, y (2) usar una métrica física como variable de salida, no una que se arme con la misma nómina que se quiere explicar. Publicar el "no" con su umbral: haría falta costos deflactados o una serie más larga, granularidad por línea y por turno para tener más observaciones independientes, y el costo de rampa (N1 y N2) para modelar la disrupción de una salida en vez de inferirla de agregados mensuales.

**Bug evitado:** Que el business case sumara un "sobrecosto de producción por rotación" de nueve cifras que en realidad era la tendencia de caída del volumen, encima del rango de costo total de rotación de DEC-015, contando dos veces el mismo fenómeno.

**Código afectado:** `04_scripts/20_costo_pieza_buena.py` (nuevo); `03_notebooks/Technostamp_Completo.ipynb` (sección 10c con `ejecutar_etapa("20_costo_pieza_buena.py")` y `mostrar_graficos([...])`, y registro en `ETAPAS_EJECUTADAS`); `04_scripts/08_visualizaciones.py` (bloques G15 y G16); `06_resultados/Discovery/visualizaciones/G15_costo_pieza_sube.png` y `G16_rotacion_no_encarece.png`; `06_resultados/Discovery/tablas_soporte/Q1_costo_pieza_buena.csv`.
