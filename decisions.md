# Registro de Decisiones Técnicas

Este archivo documenta **por qué** tomamos cada decisión técnica relevante.
La pregunta "por qué" vale más que el "qué" — el código ya explica el qué.
Cada entrada: decisión tomada · alternativa descartada · por qué la descartamos ·
conclusión (regla a futuro). Las decisiones superadas NO se borran.


## Decisiones pendientes

| ID | Decisión | Área | Estado |
|----|----------|------|--------|
| — | Confirmar con el cliente si la dotación informada (450) excluye contratistas o una planta — los datos muestran 562 activos | calidad-datos | Abierta |
| — | Auditar con RRHH el comportamiento de `meses_desde_ultimo_aumento` en las bajas (1,0 mes en renuncias vs 4,5 en activos) | calidad-datos | Abierta |
| — | Definir si el índice de criticidad de DEC-006 se adopta como reemplazo formal de `es_posicion_critica` en el sistema origen | feature-engineering | Abierta |
| — | ~~Fijar UNA definición única de tasa de rotación anual~~ | comunicacion | **Resuelta — ver DEC-019** |
| — | Decidir si el insight ejecutivo de sucesión se reformula sobre el caso unipersonal observable (Supervisor de Logística) en vez de sobre `es_posicion_critica`, que DEC-006 declaró no utilizable como insumo analítico | comunicacion | Abierta — auditoría 2026-09-05 |
| — | Confirmar el retiro de `tablas_soporte/BC_resumen_oportunidades.csv`, salida superada de `09_business_case.py` que contradice el rango vigente de `17_business_case_v2.py` | trazabilidad | Abierta — auditoría 2026-09-05 |

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
