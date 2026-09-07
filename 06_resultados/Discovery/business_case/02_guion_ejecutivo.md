# 02 · Guion ejecutivo — TechnoStamp

**Documento base para el PowerPoint de Martina Rosales, CEO y Directorio.**
Cada bloque corresponde a una slide o a un par de slides. Estructura fija por bloque:
titular · impacto de negocio · evidencia · acción · límite de la evidencia · métrica de seguimiento.

Regla que gobierna todo el documento: **el titular es una conclusión, no la descripción de un
gráfico**. Si una slide no responde qué está pasando, cuánto afecta, qué dato lo sostiene y qué
conviene corregir, es exploración, no comunicación ejecutiva.

Estado: **completo**. Bloque A (problema operativo prioritario), bloque B (diagnóstico
organizacional) y bloque C (anexo financiero y selección visual).

---

# BLOQUE A · El problema operativo prioritario

## A.1 — Titular

> **El turno noche concentra el riesgo de seguridad que más días de operación cuesta,
> y no sabemos por qué.**

Las dos mitades del titular importan igual. La primera es un hecho medido. La segunda es la razón
por la que lo que se pide es una auditoría y no un programa.

---

## A.2 — Impacto de negocio

Lo que está en juego no es un indicador de RR.HH.: son **días de planta**.

| Dimensión | Cifra | Lectura |
|---|---|---|
| Días de trabajo perdidos en el período | **138** | Equivale a más de seis meses de una persona fuera de operación |
| Días perdidos que ocurren en turno noche | **102 (74%)** | Tres de cada cuatro |
| Casos graves del período | **6** | Explican **109 de los 138 días**: el 79% del daño está en el 13% de los casos |
| Casos graves en turno noche | **5 de 6** — 84 días | El riesgo severo es casi exclusivamente nocturno |
| Personas expuestas | ~125 por mes, **151 distintas** en el período | Concentradas en Estampado (51), Ensamble (40) y Pintura (24) |

**Sobre el costo registrado.** El sistema imputa $975.000 en total a los 45 incidentes. Esa cifra
**no debe usarse como impacto**: cubre la atención del hecho, no los 138 días de producción
perdidos, ni el reemplazo, ni la cobertura del puesto. El costo real no está medido. Por eso el
caso se presenta en días de operación, que sí están medidos.

---

## A.3 — Evidencia (visual G11)

**`visualizaciones/G11_incidentes_por_turno.png`** — incidentes cada 1.000 empleado-mes por turno,
con el turno noche destacado.

| Turno | Empleado-mes | Incidentes | Días perdidos | **Tasa ×1.000** |
|---|---:|---:|---:|---:|
| **Noche** | 2.124 | **25** | **102** | **11,8** |
| Administrativo | 2.099 | 8 | 35 | 3,8 |
| Rotativo | 868 | 2 | 0 | 2,3 |
| Mañana | 2.254 | 5 | 0 | 2,2 |
| Tarde | 2.256 | 5 | 1 | 2,2 |

**El turno noche tiene 5,4 veces la tasa de mañana o tarde.**

Tres razones por las que este número aguanta que lo discutan en la sala:

1. **Está normalizado por exposición, no es un conteo.** La noche tiene 2.124 empleado-mes contra
   2.254 de mañana y 2.256 de tarde: las tres poblaciones son del mismo tamaño. La diferencia no
   viene de que haya más gente de noche, porque no la hay.
2. **Viene de la fuente auditable.** Los 45 incidentes de `eventos_rrhh` traen fecha, severidad,
   parte del cuerpo y días perdidos. La columna del panel mensual suma 100 incidentes —más del
   doble— pero no trae ninguna de esas cosas y no puede verificarse. Se usó la que se puede ir a
   comprobar (DEC-004).
3. **No es un artefacto de gente nueva.** El accidentado más reciente tenía **14 meses** de
   antigüedad; la mediana de los accidentados es de **79 meses**. No hay un solo incidente en el
   primer año de nadie. Esto no es un problema de inducción.

### Qué se accidenta, de noche

| Tipo de incidente | Noche | Resto |
|---|---:|---:|
| Sobreesfuerzo | 6 | 7 |
| Caída | 5 | 3 |
| Quemadura | 5 | 1 |
| Corte / laceración | 4 | 2 |
| Golpe / contusión | 3 | 2 |
| Atrapamiento | 2 | 5 |

No hay un tipo único que explique la diferencia: la noche está peor en casi toda la tabla. Eso
descarta la lectura cómoda de "es una máquina" o "es una tarea", y apunta a condiciones de turno.
Es información para la auditoría, no una conclusión para la slide.

---

## A.4 — Límite de la evidencia (declararlo en la slide, no en el apéndice)

**El dato dice turno asignado, no hora del hecho.**

- El campo `turno_evento` coincide con el turno asignado a esa persona en el panel en **45 de 45
  casos**. Es el turno de la persona, no un dato levantado del accidente.
- La hora registrada de los 25 incidentes rotulados "Noche" va de las **06:53 a las 22:00**.
  En todo el dataset **no hay un solo incidente entre las 23:00 y las 06:00**.

**Qué sigue siendo cierto:** la gente asignada al turno noche se accidenta 5,4 veces más, y ahí
está el 74% de los días perdidos. Eso es una propiedad de esa población y de cómo se la opera.

**Qué no puede decirse:** que los accidentes ocurran de madrugada, ni que la causa sea la
oscuridad, el horario o el sueño. Nada en los datos lo sostiene.

Decirlo primero es lo que vuelve creíble el resto. Y además refuerza el pedido: hay una diferencia
grande, real y medida, y ningún dato disponible que la explique. Eso es exactamente lo que se va a
buscar al piso.

---

## A.5 — Recomendación: auditoría operativa nocturna focalizada, 90 días

No es un plan de capacitación. No es una campaña de seguridad. Es ir a mirar seis cosas concretas
en el turno donde está el daño, con un entregable con fecha.

| Eje | Qué se va a mirar | Por qué está en la lista |
|---|---|---|
| **1. Dotación** | Personas efectivamente presentes por línea y por hora, contra el estándar de la operación | Con la misma exposición total, la noche puede tener menos gente por máquina en el momento del hecho. El panel no lo muestra |
| **2. Tareas** | Qué se hace de noche que no se hace de día: limpieza, cambios de formato, puesta en marcha, mantenimiento correctivo | Quemaduras 5 vs 1 y caídas 5 vs 3 sugieren tareas distintas, no las mismas tareas peor hechas |
| **3. Supervisión** | Presencia y ratio de supervisión por hora del turno; quién decide cuando algo se desvía | Es la variable operativa más barata de corregir si aparece |
| **4. Fatiga** | Horas extra efectivas del personal nocturno, rotación de descansos, turnos consecutivos | Mantenimiento Eléctrico (12,1 h extra/mes) y Pintura (11,9) son áreas con presencia nocturna. Es hipótesis, no causa: ver A.6 |
| **5. Mantenimiento** | Estado y disponibilidad de equipos e instalaciones en el turno; iluminación y condición del piso | Las caídas y los atrapamientos apuntan a entorno, no a conducta |
| **6. Relevo entre turnos** | Cómo se transfiere información al entrar y al salir: qué quedó abierto, qué falló, qué está intervenido | Es el momento de mayor pérdida de contexto operativo y no está registrado en ningún sistema |

### Los tres arreglos de registro que se piden junto con la auditoría

Sin esto, la próxima medición no va a ser mejor que ésta.

1. **Hora real del hecho**, validada contra el parte de turno. Hoy la hora registrada contradice al
   turno rotulado.
2. **Ficha de investigación con causa raíz obligatoria.** De los 45 incidentes, **30 no tienen
   ninguna acción correctiva registrada** y los 15 restantes repiten la misma frase: "Capacitación
   refuerzo seguridad". No existe un campo de causa raíz. No hay análisis que analizar.
3. **Conciliar las dos fuentes de incidentes.** El panel suma 100, el registro auditable 45. Hasta
   que coincidan, la mitad del fenómeno es invisible.

---

## A.6 — Hipótesis a investigar (no son causas, y así deben presentarse)

Ninguna de las cinco está probada. Se listan porque son lo que la auditoría tiene que poder
confirmar o descartar en 90 días, y porque nombrarlas explícitamente evita que la sala las dé por
ciertas.

| # | Hipótesis | Qué la confirmaría | Qué la descartaría |
|---|---|---|---|
| H1 | **Menor dotación efectiva por línea de noche** | Conteo por hora que muestre menos operarios por máquina que el estándar diurno | Dotación equivalente turno a turno |
| H2 | **Menor presencia de supervisión** | Ratio de supervisión menor, o franjas sin supervisor asignado | Cobertura equivalente |
| H3 | **Fatiga acumulada** por horas extra o turnos consecutivos | Que los accidentados nocturnos tengan más horas extra o menos descanso que sus pares del mismo turno | Que no se distingan de sus pares. **Ya hay evidencia en contra**: DEC-009 encontró que los sobrecargados crónicos no muestran un vínculo concluyente con accidentes |
| H4 | **Tareas de mayor riesgo asignadas al turno** (limpieza, cambio de formato, correctivo) | Que el parte de turno muestre estas tareas concentradas de noche, coincidiendo con quemaduras y caídas | Distribución de tareas equivalente |
| H5 | **Pérdida de información en el relevo** | Incidentes ligados a equipos intervenidos o condiciones no comunicadas en el cambio de turno | Relevo documentado y sin correlación con los hechos |

**H3 merece cuidado en la sala.** Es la hipótesis que todo el mundo va a proponer sola, y es la
única para la que el proyecto ya tiene evidencia que no la acompaña. Presentarla como probable
sería el error más caro de esta presentación.

---

## A.7 — Métricas de seguimiento: antes y después

Línea de base medida sobre el período enero 2024 – mayo 2025. Todas se recalculan con la misma
fórmula al cierre de los 90 días y a los 12 meses.

### Métricas de resultado — miden si el riesgo bajó

| Métrica | Línea de base | Fórmula | Objetivo a 12 meses |
|---|---:|---|---|
| Tasa de incidentes, turno noche | **11,8** ×1.000 empleado-mes | Incidentes de la fuente auditable ÷ empleado-mes del turno × 1.000 | Acercarse al promedio de compañía: **4,7** (45 incidentes / 9.601 empleado-mes). Hoy la noche está **2,5x** por encima de ese promedio |
| Brecha noche vs mañana/tarde | **5,4x** | Cociente de tasas | Reducirla, no eliminarla: 5,4x → 3x ya es un cambio de régimen |
| Días perdidos, turno noche | **102** (74% del total) | Suma de `dias_perdidos` del turno | Bajar el peso relativo por debajo del 50% |
| Casos graves, turno noche | **5 de 6** | Conteo por severidad | Cero graves nocturnos en el período de medición |

### Métricas de proceso — miden si la auditoría se hizo, y se pueden leer a los 90 días

Estas son las que el Directorio va a poder mirar primero. Las de resultado necesitan tiempo;
éstas no.

| Métrica | Línea de base | Objetivo a 90 días |
|---|---:|---|
| Incidentes con hora real del hecho registrada y validada | **0%** | 100% |
| Incidentes con ficha de investigación y causa raíz | **0%** (el campo no existe) | 100% de los nuevos |
| Incidentes con acción correctiva específica, distinta del texto por defecto | **0 de 45** | 100% de los nuevos |
| Brecha entre las dos fuentes de incidentes | **100 vs 45** (2,2x) | Conciliadas, una sola fuente |
| Ejes de la auditoría con hallazgo documentado y responsable asignado | 0 de 6 | 6 de 6 |

### Qué no se promete

No se promete un ahorro. El costo real de un accidente en TechnoStamp no está medido —los $975.000
del sistema cubren la atención del hecho, no los 138 días de producción—. Este caso se sostiene en
continuidad operativa y en riesgo para las personas, que es donde la evidencia es firme. La
cuantificación económica de seguridad queda como brecha declarada, no como número de la slide.

---

# BLOQUE B · Diagnóstico organizacional

Cuatro preguntas que el negocio trajo, respondidas con lo que la evidencia sostiene y nada más.
Cada apartado cierra con el límite de esa evidencia: es lo que impide que una decisión correcta se
tome por el motivo equivocado.

---

## B.1 — La rotación no está bajando. Nunca subió. (visual G8)

### Pregunta
¿La rotación de TechnoStamp está mejorando?

### Titular
> **La rotación es plana. La caída que se veía era un artefacto del corte del archivo.**

### Evidencia
`visualizaciones/G8_rotacion_original_vs_limpia.png` — serie mensual original contra período limpio.

Enero de 2024, primer mes del archivo, registra **19 salidas**: el triple de un mes normal. La
prueba de que no pertenecen al período es cuántas veces aparece cada persona antes de irse:

| Grupo | Meses observados antes de la salida |
|---|---:|
| Las 19 salidas de enero 2024 | **1, las 19 sin excepción** |
| Todas las demás salidas | 9,5 en promedio |

Son personas que ya estaban saliendo cuando se hizo el corte del archivo. No es rotación generada
en el período: es **arrastre**.

Con enero adentro, la serie arranca alta y baja — y así se había leído. Sacando el arrastre, la
pendiente es de **+0,05 puntos por año**: ruido, no tendencia. La serie limpia se mueve entre 0,5%
y 3,0% mensual sin dirección, con picos aislados en marzo 2024 (17 salidas), diciembre 2024 (14) y
abril 2025 (15).

**Efecto sobre la cifra de compañía: 19,0% → 16,7%** (DEC-017 + DEC-019).

### Decisión habilitada
No celebrar una mejora que no ocurrió, y no diseñar un programa general de retención sobre una
tendencia inexistente. La rotación de compañía es un dato de contexto estable; el problema real
está concentrado en un área (B.2), no repartido.

### Límite de la evidencia
Dieciséis meses limpios son pocos para hablar de tendencia con confianza. Y toda tasa de rotación
de este trabajo **subestima técnicamente** el riesgo: quien figura como activo no es alguien que se
queda, es alguien cuyo final todavía no se observó. Con este horizonte el efecto es chico, pero se
nombra antes de que lo pregunten.

### Métrica de seguimiento
Rotación acumulada del período con denominador fijo (personas expuestas), recalculada cada
trimestre con la misma fórmula. **Línea de base: 16,7%.** Nunca compararla contra una tasa
anualizada: son fórmulas distintas sobre los mismos 113 casos.

---

## B.2 — Mantenimiento Eléctrico es la única diferencia que se sostiene (visual G9)

### Pregunta
¿Qué áreas rotan peor que el resto de la empresa?

### Titular
> **Una sola de las diez áreas rota distinto del promedio, y rota al doble.**

### Evidencia
`visualizaciones/G9_rotacion_area_ic95.png` — rotación por área con intervalo de confianza del 95%.

| Área | Personas | Salidas | Rotación | IC 95% | Veredicto |
|---|---:|---:|---:|---|---|
| **Mantenimiento Eléctrico** | 46 | 16 | **34,8%** | **22,7 – 49,2%** | **Peor que el promedio** |
| Estampado | 185 | 37 | 20,0% | 14,9 – 26,3% | Sin diferencia |
| Ensamble | 151 | 24 | 15,9% | 10,9 – 22,6% | Sin diferencia |
| Pintura | 80 | 12 | 15,0% | 8,8 – 24,4% | Sin diferencia |
| Calidad | 71 | 9 | 12,7% | 6,8 – 22,4% | Sin diferencia |
| Mantenimiento Mecánico | 51 | 6 | 11,8% | 5,5 – 23,4% | Sin diferencia |
| Logística | 35 | 4 | 11,4% | 4,5 – 26,0% | Sin diferencia |
| Ingeniería | 23 | 2 | 8,7% | 2,4 – 26,8% | Sin diferencia |
| Administración | 16 | 1 | 6,2% | 1,1 – 28,3% | Sin diferencia |
| RRHH | 16 | 1 | 6,2% | 1,1 – 28,3% | Sin diferencia |

*Promedio de compañía: 16,7%.*

**Por qué solo una.** El intervalo completo de Mantenimiento Eléctrico —incluido su piso de 22,7%—
queda por encima del promedio. Estampado también parecía problemático con su 20,0%, pero su rango
va de 14,9% a 26,3% y **contiene al 16,7%**: con estos datos no se distingue de lo normal. Mismo
test, respuestas distintas, porque los tamaños de grupo lo son: 46 personas contra 185.

**Y aguanta la corrección estadística.** Testear diez áreas al umbral habitual del 5% hace que la
probabilidad de que *alguna* parezca significativa por puro azar ronde el 40%. Corrigiendo por eso
(Bonferroni: umbral 0,05 ÷ 10 = 0,005), Mantenimiento Eléctrico tiene **p = 0,00105**. Sobrevive
con margen. No es un hallazgo con asterisco.

### Decisión habilitada
Intervención de retención **focalizada en Mantenimiento Eléctrico**, no un plan general de empresa.
Cuarenta y seis personas, dieciséis salidas: es un problema del tamaño de un equipo, y por eso es
abordable.

### Límite de la evidencia
**Sabemos que se van; no sabemos por qué.** No hay entrevistas de salida ni encuesta de clima.
Competencia salarial externa, carga de guardias o liderazgo local son hipótesis sin testear.
Diseñar el programa de retención antes de instrumentar la entrevista de salida es apostar.

Dos afirmaciones que circularon y no sobreviven al margen de error, y que **no deben volver a la
presentación**: "Estampado rota mal" (su intervalo contiene al promedio) y "los top performers
rotan un 35% más" (los intervalos se solapan, 14,7–36,0% contra 13,4–19,2%, sobre 59 personas).

### Métrica de seguimiento
Rotación de Mantenimiento Eléctrico con su IC95, trimestral. **Línea de base: 34,8% (22,7–49,2).**
El objetivo se declara cuando el intervalo deje de estar íntegramente por encima del 16,7%, no
cuando el punto baje: con 46 personas, el punto se mueve solo por azar.
Métrica de proceso, leíble a los 90 días: **% de bajas con entrevista de salida estructurada.
Línea de base: 0%.**

---

## B.3 — Las horas extra son capacidad concentrada, no un problema de toda la empresa (visual G10)

### Pregunta
¿Las horas extra son un exceso generalizado que conviene recortar?

### Titular
> **La empresa se parte en dos: seis áreas viven sobre once horas extra al mes y cinco no llegan a
> seis. No es un exceso repartido, es capacidad faltante en un lado.**

### Evidencia
`visualizaciones/G10_distribucion_horas_extra_area.png` — distribución de horas extra por
empleado-mes, por área.

**El gráfico es un boxplot, así que muestra medianas.** Para que la slide y la tabla digan lo
mismo, todo este apartado cita **mediana de horas extra por empleado-mes**. La media está en
`tablas_soporte/P3_horas_extra_por_area.csv` y difiere poco, salvo en un caso que se explica abajo.

| Área | Mediana h extra/mes | Media | % de la nómina base |
|---|---:|---:|---:|
| Pintura | **12,2** | 11,9 | 10,2% |
| Logística | 11,8 | 11,5 | 9,8% |
| Mantenimiento Mecánico | 11,8 | 11,1 | 9,4% |
| Estampado | 11,7 | 11,3 | 9,6% |
| Mantenimiento Eléctrico | 11,3 | **12,1** | 10,3% |
| Ensamble | 11,2 | 11,1 | 9,5% |
| — corte — | | | |
| Dirección *(1 persona)* | 6,1 | 5,5 | 4,7% |
| RRHH | 5,0 | 4,3 | 3,7% |
| Calidad | 4,7 | 5,2 | 4,4% |
| Administración | 4,2 | 4,1 | 3,5% |
| Ingeniería | 3,5 | 3,6 | 3,0% |

**El corte es limpio: 11,2 h de un lado, 6,1 del otro.** No hay zona gris. Costo anual total de
horas extra: **$987,6M**.

**Un detalle que vale mirar.** Mantenimiento Eléctrico es la única área donde la media (12,1)
supera claramente a la mediana (11,3). Eso significa que tiene una cola larga: algunas personas del
área acumulan mucho más que sus propios compañeros. Es la misma área con la peor rotación (B.2).
No se afirma que una cosa cause la otra —no hay evidencia de eso—, pero es una coincidencia que la
intervención de retención debería mirar.

**Sobrecarga crónica:** 49 empleados activos, de 562, tienen horas extra altas en al menos el 70%
de sus meses. Concentrados en Estampado (13), Pintura (12) y Ensamble (11).

### Decisión habilitada
Revisión de **capacidad y cobertura** en las seis áreas cargadas, con nombre y apellido. No una
política general de recorte de horas extra: en cinco áreas no hay nada que recortar.

### Límite de la evidencia
**No es un ahorro capturable, y presentarlo como tal sería el error más caro del informe.** El
recargo efectivo de la hora extra en estos datos es **1,343x** el costo de la hora normal, mientras
que el costo cargado de un empleado nuevo —cargas patronales, ART, aguinaldo, vacaciones— supera
**1,40x**. El punto de equilibrio está en cargas del 34,3%: por debajo conviene contratar, por
encima conviene la hora extra. En Argentina la condición no se cumple. Los $987,6M son el costo de
operar así, no una oportunidad de ahorro (DEC-009).

Tampoco se sostienen los argumentos de respaldo: los sobrecargados crónicos rotan igual que el
resto (19,7% vs 19,0%), su exceso de ausentismo es real pero marginal (+11,1%, unos $4,75M
anuales), y el vínculo con accidentes no es concluyente.

**Verificado y descartado para esta presentación:** el turno noche tiene 15,4% de sobrecargados
crónicos contra 11,5% de mañana y 9,0% de tarde. Parece una conexión con el bloque de seguridad,
pero **no se distingue del azar** (z = 1,48; los intervalos se solapan). Se deja registrado para
que nadie lo "descubra" más adelante como si fuera un hallazgo.

### Métrica de seguimiento
Mediana de horas extra por empleado-mes en las seis áreas cargadas, mensual. **Línea de base:
11,2 a 12,2 h.** Y el indicador que importa de verdad: **cantidad de personas con sobrecarga
crónica. Línea de base: 49 activos.** Es la métrica de riesgo humano; las horas totales son la
métrica de costo, y esa no se promete bajar.

---

## B.4 — Sucesión: una tarjeta de alerta, no un gráfico (reemplaza G13)

### Pregunta
¿Cuántos puestos críticos están en riesgo?

### Por qué esto no es un gráfico
El scatter `G13_riesgo_sucesion_por_puesto.png` grafica un fenómeno que tiene **un solo caso
verificable**. Un gráfico de dispersión con un punto no comunica: sugiere una distribución que no
existe y obliga a la audiencia a buscar un patrón donde hay un hecho puntual. Se reemplaza por una
tarjeta.

> ### ⚠ Punto de falla unipersonal — Supervisor de Logística
>
> | | |
> |---|---|
> | **Dotación del puesto** | **1 persona** |
> | **En riesgo a 24 meses** | **1** |
> | **Sucesores potenciales identificados** | **0** |
> | **Cobertura** | **Ninguna** |
>
> Si esa persona sale, no hay nadie en el puesto y no hay nadie preparándose para ocuparlo.

### Evidencia
`tablas_soporte/P1_riesgo_sucesion_por_puesto.csv`. Es el único registro persistido de riesgo de
sucesión, y contiene exactamente esta fila.

### Decisión habilitada
Documentar en 90 días las decisiones, contactos, rutinas y excepciones operativas que hoy dependen
de esa persona. Asignar formación cruzada con acompañamiento en el puesto. Es barato, es acotado y
no requiere ningún dato nuevo para empezar.

### Límite de la evidencia — y una corrección al informe anterior
**No debe repetirse la afirmación "cuatro de las cinco posiciones críticas se jubilan en 12
meses".** Esa frase, publicada en la versión previa del informe ejecutivo, está construida sobre el
campo `es_posicion_critica` del sistema del cliente, que el propio proyecto descartó como insumo
analítico (DEC-006): marca 10 empleados de 694 (**1,4%**) y **nunca cambia** a lo largo de los 17
meses, lo que indica que se cargó una vez y no se mantuvo. Con cinco posiciones críticas activas,
la respuesta literal a "cuántos puestos críticos están en riesgo" sería "cuatro" — cierto e inútil.

El índice propio de criticidad construido por el proyecto —dotación del puesto ≤ 3, span de control
o nivel jerárquico alto, antigüedad ≥ 10 años, top performer— identifica **47 activos (8,4%)** con
criticidad estimada. Sobre esa base sí se puede planificar. Pero cruzada con proximidad a
jubilación, la tabla persistida devuelve **un solo puesto**.

Con un caso no hay patrón. Lo honesto es presentarlo como lo que es: una alerta concreta y
accionable, más una brecha de calidad de dato para devolverle al cliente.

### Métrica de seguimiento
| Métrica | Línea de base | Objetivo a 90 días |
|---|---:|---|
| Puestos unipersonales sin sucesor identificado | **1** | 0 |
| Rutinas críticas del puesto documentadas | 0 | 100% |
| Cobertura del flag `es_posicion_critica` en el sistema origen | 1,4%, sin actualizar en 17 meses | Revisado y mantenido por RR.HH. |

---

---

# BLOQUE C · Anexo financiero y selección visual

Este bloque va **después** de los dos anteriores, y esa posición es deliberada. La conversación de
negocio se gana con días de operación y con un área que rota al doble; el número en pesos es
soporte, no titular. Un rango de amplitud 8x presentado primero contamina todo lo que viene atrás.

---

## C.1 — La única cifra de rotación de la compañía es 16,7%

Antes de cualquier número en pesos, hay que fijar el denominador. Con los mismos 113 casos
conviven **tres tasas defendibles**, y publicar dos sin distinguirlas es lo que hace que un
directorio descarte un informe entero.

| Definición | Cálculo | Valor |
|---|---|---:|
| **A — Acumulada del período (oficial)** | 113 salidas ÷ 675 personas expuestas | **16,7%** |
| B — Anualizada sobre dotación activa promedio | 113 ÷ 16 meses × 12 ÷ 563 activos | 15,0% |
| C — Del período, anualizada | — | 12,6% |

**Se adopta la A** (DEC-019). No porque sea la más alta, sino porque es la que **ya sostiene todo
el trabajo fino del proyecto**: las diez áreas, los intervalos de confianza de Wilson, el 34,8% de
Mantenimiento Eléctrico y el gráfico G9. La anualizada se calculaba una sola vez, aparte, solo para
el titular.

Esto importa en la sala: comparar el 34,8% de Mantenimiento Eléctrico —calculado con la fórmula
acumulada— contra un titular de 15,0% inflaba la brecha de **2,08x a 2,32x**. Misma empresa, mismos
casos, dos tasas en la misma slide.

**Regla para la presentación: 16,7% en todas partes.** Si RR.HH. necesita una cifra anualizada para
compararse contra un benchmark de industria, se calcula aparte y se etiqueta explícitamente como
proyección. Nunca reemplaza la base de comparación entre áreas.

---

## C.2 — Business case de retención: un rango, no un número (visual G14)

### Titular
> **Reducir las renuncias voluntarias vale entre $23M y $195M al año. Esa amplitud no es
> imprecisión nuestra: es lo que la empresa todavía no mide.**

### Evidencia
`visualizaciones/G14_business_case_escenarios.png` · `tablas_soporte/BC_rango_retencion.csv` ·
`tablas_soporte/BC_supuestos.json`

Base: **≈55 renuncias voluntarias anualizadas** en el período limpio.

| Escenario | Costo por salida | Reducir 15% | Reducir 25% | Reducir 40% |
|---|---:|---:|---:|---:|
| Conservador | $2.836.933 | **$23.298.312** | $38.830.520 | $62.128.831 |
| Central | $6.044.356 | $49.639.275 | **$82.732.125** | $132.371.400 |
| Agresivo | $8.896.808 | $73.065.033 | $121.775.055 | **$194.840.088** |

- **Piso del rango:** $23,3M/año — conservador, reducción del 15%
- **Punto central:** $82,7M/año — escenario central, reducción del 25%
- **Techo del rango:** $194,8M/año — agresivo, reducción del 40%
- **Amplitud: 8,4 veces**

### El piso verificable: $1,64M/año

Esta es la cifra que sobrevive si se le quita **todo** supuesto propio.

Desarmando el costo por salida del escenario central ($6,04M):

| Componente | Monto | Origen |
|---|---:|---|
| Reclutamiento + onboarding | **$200.000** | **Dato que TechnoStamp mide** |
| Sueldo perdido durante la vacancia | **$2.991.905** | **Supuesto nuestro** (47,2 dias de time-to-fill x $1.901.634 de salario medio del saliente) |
| Rampa del ingresante hasta rendimiento pleno | **$2.852.451** | **Supuesto nuestro** (3 meses al 50% de rendimiento) |

**El 97% del costo por salida es juicio, no medición.** Usando únicamente los $200.000 que la
empresa registra, con la reducción más conservadora, el ahorro anual es de **$1.642.500**. Ese
número no depende de ningún supuesto nuestro y se puede defender frente a cualquier pregunta.

### Los dos supuestos, explícitos

| Escenario | Fracción de sueldo perdida en la vacancia | Rampa | Rendimiento durante la rampa |
|---|---:|---:|---:|
| Conservador | 50% — el equipo absorbe parte del trabajo | 2 meses | 70% |
| Central | 100% — el puesto queda descubierto | 3 meses | 50% |
| Agresivo | 100% — puesto descubierto | 6 meses | 50% |

Solo mover la rampa de 3 a 6 meses mueve el ahorro entre **$49,6M y $132,4M**. Una cifra única
escondería eso y lo presentaría como una precisión que no existe.

### Los dos datos que cierran el rango

| # | Dato | Fuente probable | Qué desbloquea |
|---|---|---|---|
| **N1** | Producción promedio mensual de un operario ya formado, por puesto | Sistema de producción / MES de planta. El proyecto ya observa `unidades_producidas` en las tres áreas de producción | Convierte la rampa de supuesto a medición |
| **N2** | Meses desde el ingreso hasta alcanzar ese nivel | Derivable de N1 cruzado con la fecha de ingreso del panel | Cierra el segundo supuesto |

Con N1 y N2, el 97% que hoy es juicio pasa a ser medición y el rango de 8,4x se comprime a una
estimación con incertidumbre acotada.

### Límite de la evidencia
Esto es una **oportunidad estimada**, no un ahorro. Tres advertencias que van en la slide:

1. **Nadie garantiza la reducción.** Los porcentajes de 15/25/40% son objetivos de gestión, no
   resultados proyectados de una intervención concreta.
2. **No hay diagnóstico de causa.** Sin entrevistas de salida no se sabe por qué se van, y sin eso
   ningún programa de retención tiene un objetivo al que apuntar.
3. **`BC_resumen_oportunidades.csv` está superado.** Ese archivo todavía publica "$92,4M esperado"
   para rotación voluntaria: es exactamente la cifra única que DEC-015 descartó. La fuente vigente
   es `BC_supuestos.json`. No usar ese CSV en la presentación.

### Métrica de seguimiento
| Métrica | Línea de base | Objetivo |
|---|---:|---|
| Renuncias voluntarias anualizadas | **≈55/año** | Definir objetivo recién con N3 (entrevistas de salida) en marcha |
| % del costo por salida sostenido en datos del cliente | **3%** | 100%, con N1 y N2 |
| Amplitud del rango | **8,4x** | Reducirla es el entregable, antes que capturar el ahorro |

---

## C.3 — Selección visual: qué se muestra, qué se reformula, qué se reemplaza

Un gráfico entra a la presentación si prueba el titular que ilustra y está normalizado por la
exposición de cada grupo. Los dos criterios, no uno.

### ✅ Mostrar

| Visual | Titular que sostiene | Por qué entra |
|---|---|---|
| **G11** `G11_incidentes_por_turno.png` | El turno noche concentra el riesgo | Tasa por empleado-mes, no conteo; grafica turno, que es la variable del titular (DEC-007, DEC-021) |
| **G9** `G9_rotacion_area_ic95.png` | Una sola área rota distinto del promedio | Lleva el intervalo de confianza a la vista: se ve por qué Mantenimiento Eléctrico sí y Estampado no |
| **G8** `G8_rotacion_original_vs_limpia.png` | La rotación es plana, no descendente | Muestra las dos series juntas: el hallazgo *es* la comparación |
| **G10** `G10_distribucion_horas_extra_area.png` | Seis áreas viven sobre 11 h extra; cinco no llegan a 6 | El boxplot muestra la distribución, no solo el promedio: es lo que hace visible que el corte es limpio |
| **G14** `G14_business_case_escenarios.png` | El ahorro es un rango, no una cifra | Muestra los tres escenarios juntos; ver la amplitud *es* el mensaje |

**Orden sugerido en el deck:** G11 → G9 → G8 → G10 → G14. Sigue la prioridad del caso: primero el
riesgo operativo, después el diagnóstico, el dinero al final.

### ✏️ Reformular — G12

**`G12_capacitacion_seguridad_vs_incidentes.png`**

**Título actual:** *"Más capacitación coincide con más incidentes (se entrena después del
accidente, no antes)"*.

**Ese título no se sostiene, por dos motivos independientes:**

1. **La relación no existe estadísticamente.** La correlación área a área entre horas de
   capacitación en seguridad por empleado y tasa de incidentes es **r = 0,394 con p = 0,260**
   (n = 10 áreas). No se distingue de cero. Quitando Logística —que con 35,2 h por empleado es un
   caso aparte— baja a r = 0,279. Presentar "coincide con" ya es afirmar de más.
2. **La temporalidad no está medida.** El código agrega totales de todo el período por área.
   **No hay ninguna comparación entre la fecha de una capacitación y la fecha de un incidente.**
   Decir "se entrena después del accidente" es una hipótesis narrativa, no un cálculo del proyecto.

**Titular de reemplazo:**

> **No sabemos si la capacitación en seguridad previene incidentes, porque nadie lo mide.**

**Qué sí sostiene la evidencia, y es un hallazgo real:**

| Hecho verificado | Cifra |
|---|---|
| Incidentes sin ninguna acción correctiva registrada | **30 de 45** |
| Incidentes con acción correctiva | 15, **todos con la misma frase**: "Capacitación refuerzo seguridad" |
| Campo de causa raíz en el sistema | **No existe** |
| Acciones correctivas específicas del hecho | **0 de 45** |

Eso no es un programa de capacitación evaluado: es un campo de formulario que se completa siempre
igual. La brecha es de **medición preventiva**, y esa sí es una conclusión defendible.

**Cómo mostrarlo.** Si se conserva el scatter, va con el título nuevo y con una etiqueta visible:
*"comparación descriptiva de totales del período; no mide temporalidad ni causalidad"*.
La alternativa más honesta es reemplazarlo por la tabla de arriba, que comunica la brecha sin
sugerir una relación que los datos no muestran.

### 🔄 Reemplazar — G13

**`G13_riesgo_sucesion_por_puesto.png`** → **tarjeta de alerta de sucesión** (ya escrita en B.4).

El scatter dibuja una distribución que no existe: el único output persistido de riesgo de sucesión
tiene **una sola fila**. Un gráfico de dispersión con un punto obliga a la audiencia a buscar un
patrón donde hay un hecho puntual, y lo peor es que invita a llenar el vacío con la tabla de "4 de
5 posiciones críticas" — que está construida sobre `es_posicion_critica`, el flag que DEC-006
descartó por marcar solo el 1,4% del universo y no actualizarse en 17 meses.

Una tarjeta con cuatro números —dotación 1, en riesgo 1, sucesores 0, cobertura ninguna— comunica
el riesgo completo sin insinuar un patrón. Si más adelante el índice propio de criticidad devuelve
varios puestos, el gráfico vuelve a tener sentido; hoy no.

### ❌ Fuera de la presentación

| Elemento | Motivo |
|---|---|
| "Estampado rota mal" | Su IC 14,9–26,3% contiene al promedio de 16,7% (DEC-016) |
| "Los top performers rotan un 35% más" | Intervalos solapados: 14,7–36,0% vs 13,4–19,2%, sobre 59 personas (DEC-016) |
| "$988M de ahorro en horas extra" | No es capturable: recargo de la hora extra 1,343x vs costo cargado del ingresante >1,40x (DEC-009). Se reporta en negativo, como costo de operar |
| "$92,4M esperado" de `BC_resumen_oportunidades.csv` | Cifra única descartada por DEC-015; el archivo está superado |
| G1–G7 (pirámide etaria, género, brecha salarial, etc.) | Son visuales de exploración, no de decisión. Van al anexo técnico si alguien pregunta |

---

## C.4 — Las cuatro brechas de dato que se le devuelven al cliente

No son un pedido genérico de "mejores datos". Cada una desbloquea una decisión concreta que hoy no
puede tomarse.

| # | Dato faltante | Decisión que desbloquea | Costo de conseguirlo |
|---|---|---|---|
| **N5** | Ficha de investigación con causa raíz obligatoria, y hora real del hecho | Vuelve defendible cualquier conclusión de seguridad. Es el habilitador de la auditoría nocturna | Control de proceso en el sistema actual, no analítica |
| **N3** | Entrevistas de salida estructuradas | Separa "sabemos quién se va y cuánto cuesta" de "sabemos por qué". Sin esto, retención en Mantenimiento Eléctrico es una apuesta | Proceso nuevo de RR.HH.; experimento de 3 meses sin prerrequisitos |
| **N1 + N2** | Producción de un operario formado y meses hasta rendimiento pleno | Cierra el 97% de supuesto del business case y comprime el rango de 8,4x | Cruce del sistema de producción con la fecha de ingreso |
| **N6** | Auditoría del campo `meses_desde_ultimo_aumento` en las bajas | Define si el patrón contraintuitivo (1,0 mes en renuncias vs 4,5 en activos) es señal de fuga temprana o artefacto de registro | Una sola auditoría. Es la validación más barata del proyecto |

**Prioridad: N5 primero.** Es la única que bloquea la recomendación principal de la presentación.

---

**Siguiente:** Subentregable 5 — lista formal de insights nuevos (`03_insights_nuevos.md`).

