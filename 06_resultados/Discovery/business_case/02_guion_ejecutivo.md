# 02 · Guion ejecutivo — TechnoStamp

**Documento base para el PowerPoint de Martina Rosales, CEO y Directorio.**
Cada bloque corresponde a una slide o a un par de slides. Estructura fija por bloque:
titular · impacto de negocio · evidencia · acción · límite de la evidencia · métrica de seguimiento.

Regla que gobierna todo el documento: **el titular es una conclusión, no la descripción de un
gráfico**. Si una slide no responde qué está pasando, cuánto afecta, qué dato lo sostiene y qué
conviene corregir, es exploración, no comunicación ejecutiva.

Estado: bloque operativo (subentregable 2). El diagnóstico organizacional y el anexo financiero
se agregan en los subentregables 3 y 4.

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

**Siguiente:** Subentregable 3 — diagnóstico organizacional (G8, G9, G10 y la tarjeta de sucesión).
