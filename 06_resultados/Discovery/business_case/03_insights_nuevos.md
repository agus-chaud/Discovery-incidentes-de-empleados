# 03 · Insights del Discovery TechnoStamp

**Subentregable 5.** Tres secciones separadas a propósito, porque responden a cosas distintas:
lo que el negocio preguntó, lo que el negocio no sabía que no sabía, y lo que hoy no se puede
saber con los datos que existen.

Ningún insight de este documento entra sin una fuente verificable detrás. Donde la evidencia no
alcanza para afirmar, dice qué no puede afirmarse.

---

# 1. Preguntas iniciales respondidas

Martina Rosales trajo cuatro preocupaciones. El análisis agregó una quinta que no estaba en la
lista y resultó ser la más cara.

| # | Pregunta original | Respuesta | Lectura |
|---|---|---|---|
| **P1** | ¿Cuántos puestos críticos están en riesgo por jubilación a 12 meses? | **No es el riesgo que se cree.** El campo del sistema destinado a marcar posiciones críticas cubre 10 de 694 personas (1,4%) y no cambia en 17 meses | El riesgo real y verificable es distinto: **un** puesto unipersonal sin sucesor (ver I9) |
| **P2** | ¿Hay desbalance de género? | **Sí en representación y promoción; no en salario.** La brecha salarial controlada por nivel, área, antigüedad, edad y performance (OLS, n=562, R²=0,865) no sostiene inequidad retributiva | Es un problema de pipeline, no de compensación. No entra al deck ejecutivo; va al anexo |
| **P3** | ¿Hay equipos sobrecargados con horas extra? | **Sí, y son seis áreas identificadas. Pero sustituir horas extra por dotación destruye valor** | $987,6M anuales que son costo de operar, no ahorro capturable (ver I3) |
| **P4** | ¿Cómo mejorar la prevención de accidentes? | **Empezando por el turno noche: 5,4x la tasa de mañana o tarde**, con exposición comparable | Es el hallazgo más sólido del proyecto y la prioridad de la presentación (ver I4) |
| **P5** | *(no estaba en la lista)* ¿Qué nos cuesta la rotación? | **16,7% en el período limpio, plana, ≈55 renuncias voluntarias al año** | La oportunidad económica más grande: $23M–$195M anuales (ver I10) |

**Tres de las cuatro preocupaciones originales no sostienen la conclusión que se esperaba de
ellas.** No porque estuvieran mal planteadas, sino porque el dato disponible respondía otra cosa.
Eso es un resultado del Discovery, no una falla.

---

# 2. Insights nuevos — lo que el negocio no sabe que no sabe

Doce hallazgos, todos anclados en una fuente que se puede ir a verificar.

**Sobre la columna de veredicto.** Se aplica el criterio de `ESTUDIO_conceptos_technostamp.md` §1:
un modelo se justifica cuando la decisión que alimenta pasa **muchas veces, rápido, y a una escala
que una persona no puede revisar caso por caso**. Ninguno de los doce cumple hoy esas tres cosas.
El detalle de por qué, insight por insight, se desarrolla en `04_puente_discovery_automation.md`.

| # | Insight nuevo | Fuente / evidencia | Decisión habilitada | Qué hoy **no** puede afirmarse | Brecha de datos real | Proyecto derivado | Variable objetivo o patrón | Veredicto Discovery → Automation | Etapas ds-* |
|---|---|---|---|---|---|---|---|---|---|
| **I1** | Enero 2024 no fue una crisis: fue arrastre del corte del archivo. La rotación es plana, no descendente | DEC-017; las 19 salidas de enero aparecen **1 solo mes** cada una, contra 9,5 del resto. Pendiente limpia: +0,05 puntos/año | Dejar de leer una mejora que no ocurrió; fijar 16,7% como base única de compañía (DEC-019) | Que la rotación tenga tendencia. 16 meses limpios no alcanzan. Y toda tasa subestima por censura a derecha | Ninguna — es una regla de higiene, no un dato faltante | Chequeo de bordes obligatorio en todo panel con fecha de corte | — | **Ninguno — sigue siendo Discovery** | No aplica |
| **I2** | De diez áreas, **una sola** rota distinto del promedio, y rota al doble | `P5_rotacion_por_area_con_IC.csv`: Mant. Eléctrico 34,8% (16/46), IC95 22,7–49,2, p=0,00105 vs umbral Bonferroni 0,005 | Intervención de retención focalizada en 46 personas, no plan general de empresa | **Por qué** se van. Ni que Estampado rote mal: su IC contiene al promedio | **N3** — entrevistas de salida estructuradas | Programa de retención acotado a un área | Motivo de salida estructurado | **Ninguno — sigue siendo Discovery** | No aplica |
| **I3** | Las horas extra parten la empresa en dos grupos limpios, y el grupo cargado no es sustituible por dotación | `P3_horas_extra_por_area.csv`: seis áreas ≥11,2 h/mes (mediana), cinco ≤6,1. Sin zona gris. DEC-009: recargo HE 1,343x vs costo cargado del ingresante >1,40x | Revisión de capacidad y cobertura en seis áreas nombradas; **no** una política general de recorte | Que los $987,6M sean ahorro. El punto de equilibrio pide cargas <34,3%: en Argentina no se cumple | Ninguna para la conclusión; el costo cargado real de TechnoStamp la afinaría | Revisión de capacidad por área | — | **Ninguno — sigue siendo Discovery** | No aplica |
| **I4** | El turno noche concentra 5,4x la tasa de incidentes, con exposición comparable | `P4_incidentes_por_turno.csv`: 11,8 vs 2,2 ×1.000 empleado-mes. 2.124 empleado-mes de noche vs 2.254 y 2.256. 25 de 45 incidentes, 102 de 138 días perdidos | **Auditoría operativa nocturna focalizada de 90 días** — la recomendación principal del caso | La causa. Dotación, tareas, supervisión, fatiga, mantenimiento y relevo son hipótesis, no hallazgos | **N5** — ficha de investigación con causa raíz obligatoria | Auditoría operativa, no analítica | — | **Ninguno — sigue siendo Discovery** | No aplica |
| **I5** | El turno que figura en el incidente es el turno **asignado a la persona**, no el turno del hecho | `turno_evento` = `turno_trabajo` del panel en **45 de 45** casos. `hora_evento` de los 25 casos "Noche" va de **06:53 a 22:00**; ningún incidente entre 23:00 y 06:00 en todo el dataset | Declarar el límite en la propia slide, y pedir la hora real del hecho como parte del arreglo de registro | Que los accidentes ocurran de madrugada, ni atribuirlos a oscuridad, horario o sueño | **Hora real del hecho**, validada contra el parte de turno. El backlog N4 decía que faltaba la columna de turno: la columna existe, el problema es otro | Corrección de captura en el formulario de incidentes | — | **Ninguno — es un arreglo de registro** | No aplica |
| **I6** | El daño está concentrado en poquísimos casos: **6 graves explican 109 de los 138 días perdidos** | `eventos_limpio.parquet`: Grave n=6 → 109 días; Moderado n=9 → 29; Leve n=30 → 0. Cinco de los seis graves son del turno noche (84 días) | Priorizar la prevención de eventos graves sobre el conteo total de incidentes: son objetivos distintos | Que reducir incidentes leves reduzca días perdidos. Los 30 leves suman **cero** días | **N5** — sin causa raíz no se sabe qué separa un grave de un leve | Prevención focalizada en severidad | — | **Ninguno — sigue siendo Discovery** | No aplica |
| **I7** | El riesgo de accidente **sube** con la experiencia, no baja. No hay un solo accidente de ingresante | `eventos_limpio.parquet`: antigüedad mínima de un accidentado **14 meses**, mediana **79 meses** (6,6 años). Cero incidentes en el primer año de cualquier persona | No invertir en inducción como respuesta al problema de seguridad: el problema no está ahí | Que la experiencia cause accidentes. Puede ser asignación de tareas de riesgo a los más veteranos | Qué tarea hacía la persona en el momento del hecho | Revisión de asignación de tareas por antigüedad | — | **Ninguno — sigue siendo Discovery** | No aplica |
| **I8** | Nadie mide si la capacitación en seguridad previene algo. La acción correctiva es un campo de formulario | 30 de 45 incidentes **sin ninguna acción correctiva**; los 15 restantes con la **misma frase** ("Capacitación refuerzo seguridad"). No existe campo de causa raíz. Correlación área a área capacitación–incidentes: **r=0,394, p=0,260** | No ampliar capacitación general antes de la auditoría; instrumentar medición de eficacia preventiva | Que capacitar coincida con accidentarse (la correlación no se distingue de cero) **ni** que la capacitación ocurra después del incidente: **el código no compara fechas** | **N5** + cruce fecha de capacitación vs fecha de incidente por empleado | Medición de eficacia preventiva | Incidente posterior a la capacitación, por persona | **Ninguno — primero hay que medir** | No aplica |
| **I9** | El riesgo de sucesión real es **un** puesto unipersonal sin sucesor, y el flag del sistema que debería detectarlo no se mantiene | `P1_riesgo_sucesion_por_puesto.csv`: una sola fila — Supervisor de Logística, dotación 1, sucesores 0. DEC-006: `es_posicion_critica` marca 10 de 694 (1,4%) y **nunca cambia** en 17 meses | Documentar rutinas y asignar formación cruzada para ese puesto. Devolverle a RR.HH. la brecha del flag | Que haya un patrón de sucesión: con un caso no hay patrón. Ni repetir "4 de 5 posiciones críticas", construido sobre el flag descartado | Mantenimiento del flag en el sistema origen, o adopción formal del índice propio | Plan de continuidad de un puesto | — | **Ninguno — un solo caso** | No aplica |
| **I10** | El caso económico de la retención es un rango de **8,4x**, y el 97% del costo por salida es supuesto nuestro | `BC_supuestos.json`: $23,3M / $82,7M / $194,8M. Del costo central de $6.044.356, solo **$200.000** son dato del cliente; vacancia $2.991.905 y rampa $2.852.451 son supuestos | Publicar el rango con los supuestos a la vista y el piso verificable de **$1,64M** al lado | Que exista un ahorro de $82,7M. Es una oportunidad estimada bajo supuestos declarados | **N1** (producción de un operario formado) + **N2** (meses hasta rendimiento pleno) | Medición del costo real de vacancia y rampa | — | **Ninguno — es una medición, no un modelo** | No aplica |
| **I11** | Mantenimiento Eléctrico es la **única** área donde la media de horas extra supera a la mediana: tiene cola larga | Media 12,1 vs mediana 11,3 h/empleado-mes. En las otras diez áreas la relación es la inversa o pareja. Es la misma área con la peor rotación | Mirar la distribución interna del área, no solo su promedio, en la intervención de retención | Que la cola de horas extra explique la rotación del área. Es coincidencia observada, no relación medida | **N3** — la entrevista de salida es lo que conectaría ambas cosas | Diagnóstico interno de un área | — | **Ninguno — sigue siendo Discovery** | No aplica |
| **I12** | Quien renuncia había recibido un aumento hace **1,0 mes**; quien se queda, hace **4,5** | `empleados_nivel_persona.parquet`: `meses_desde_ultimo_aumento` = 1,0 en renuncias voluntarias (n=89) vs 4,5 en activos (n=562) | Auditar cómo se escribe el campo al registrar una baja, antes de interpretarlo | **Nada todavía.** Puede ser contraoferta fallida (señal real y valiosa) o artefacto de registro. Es contraintuitivo y por eso hay que auditarlo primero | **N6** — auditoría del campo en las bajas. Es la validación más barata del proyecto | Tablero de señal de fuga temprana, **solo si resulta real** | Salida en los próximos N meses | **Ninguno — hoy no se sabe si el dato significa lo que parece** | No aplica |

---

## Un candidato que se verificó y se descartó

Se deja escrito para que no reaparezca más adelante presentado como hallazgo.

**"La sobrecarga crónica se concentra en el turno noche."** Parecía conectar el bloque de horas
extra con el de seguridad. Los números: Noche 15,4% (19 de 123), Mañana 11,5% (16 de 139), Tarde
9,0% (12 de 134). **No se distingue del azar** — z = 1,48, y los intervalos se solapan. No entra al
deck. Es exactamente el tipo de diferencia que parece un hallazgo hasta que se le calcula el margen
de error (DEC-016).

---

# 3. Brechas de medición y próximos datos a pedir

Seis brechas. Ninguna se propone "porque sí": cada una desbloquea una decisión que hoy no puede
tomarse.

| Prioridad | # | Dato | Qué desbloquea | Costo de conseguirlo |
|---|---|---|---|---|
| **1** | **N5** | Ficha de investigación con causa raíz obligatoria + **hora real del hecho** | Vuelve defendible toda conclusión de seguridad. Es el habilitador de la auditoría nocturna, que es la recomendación principal del caso | Control de proceso en el sistema actual. No es analítica, es una validación de carga |
| **2** | **N3** | Entrevistas de salida estructuradas | Separa "sabemos quién se va y cuánto cuesta" de "sabemos por qué". Sin esto, cualquier programa de retención en Mantenimiento Eléctrico es una apuesta | Proceso nuevo de RR.HH.; experimento de 3 meses, sin prerrequisitos técnicos |
| **3** | **N6** | Auditoría de `meses_desde_ultimo_aumento` en las bajas | Define si la señal de fuga temprana (I12) es real o un artefacto de registro. Si es real, es la señal más valiosa que hoy existe sin usar | Una sola auditoría. La validación más barata del proyecto |
| **4** | **N1** | Producción promedio mensual de un operario formado, por puesto | Convierte la rampa del ingresante de supuesto a medición | Sistema de producción / MES. El proyecto ya observa `unidades_producidas` en las tres áreas de producción |
| **5** | **N2** | Meses desde el ingreso hasta alcanzar ese nivel | Cierra el segundo supuesto del costo por salida. Con N1 y N2, el rango de 8,4x se comprime a incertidumbre acotada | Derivable de N1 cruzado con la fecha de ingreso del panel |
| **6** | — | Conciliación de las dos fuentes de incidentes | El panel suma **100** incidentes, el registro auditable **45**. Hasta que coincidan, la mitad del fenómeno es invisible | Depende de N5: la ficha obligatoria es lo que fuerza la conciliación |

## Dos brechas que el proyecto declara sobre sí mismo

No son datos que falten del cliente: son límites del análisis, y nombrarlos antes de que los
pregunten es parte del entregable.

**Censura por la derecha, sin tratar.** Quien figura como activo no es alguien que se queda: es
alguien cuyo final todavía no se observó. Toda tasa de rotación de este trabajo subestima
técnicamente el riesgo real. Con 16 meses el efecto es chico y es improbable que cambie una
conclusión, pero está ahí. Tratarlo pediría análisis de supervivencia, que es un campo aparte
precisamente por esto.

**El costo real de un accidente no está medido.** El sistema imputa $975.000 al total de los 45
incidentes: eso cubre la atención del hecho, no los 138 días de producción perdidos, ni el
reemplazo, ni la cobertura del puesto. Por eso el caso de seguridad se presenta en días de
operación y no en pesos.

## Sobre el "~14 incidentes al año evitables"

Esa cifra circula en el informe técnico. Es aritmética de brecha, y conviene saber de dónde sale
antes de repetirla en una slide:

| Supuesto de convergencia | Incidentes esperados de noche | Exceso anualizado |
|---|---:|---:|
| Si la noche tuviera la tasa de mañana/tarde (2,2) | 4,7 | **14,3/año** |
| Si la noche convergiera al promedio de compañía (4,7) | 10,0 | **10,6/año** |

Ninguna de las dos es una promesa: son la distancia entre lo observado y una referencia elegida.
Si se usa, va etiquetada como brecha, nunca como resultado esperado de la auditoría.

---

**Siguiente:** subentregable 6 en adelante — puente Discovery → Automation, uno o dos insights por
entrega, con el criterio de `ESTUDIO_conceptos_technostamp.md` §1 aplicado sin ambigüedad.
