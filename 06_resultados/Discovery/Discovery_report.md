# Discovery de RRHH — TechnoStamp Industries

**Fecha:** 3 de septiembre de 2026
**Período analizado:** enero 2024 – mayo 2025 (17 meses)
**Universo:** 694 empleados observados · 562 activos al cierre · 9.733 registros empleado-mes

---

## 1. Resumen ejecutivo

Analizamos tres fuentes (panel mensual de empleados, eventos de RRHH y capacitaciones) para responder cinco preguntas de negocio. **Tres de las cuatro preocupaciones que trajo Martina no se sostienen con los datos**, y el problema más caro de la compañía no estaba en la lista.

| # | Pregunta | Veredicto | Valor anual en juego |
|---|---|---|---|
| P1 | ¿Cuántos puestos críticos en riesgo por jubilación a 12 meses? | **4 personas.** No es el riesgo que se cree | Bajo — pero hay un riesgo distinto y mayor |
| P2 | ¿Hay desbalance de género? | **Sí en representación, no en salario** | Reputacional / pipeline |
| P3 | ¿Hay equipos sobrecargados con horas extra? | **Sí, pero sustituirlas destruye valor** | $988M en HE — sin ahorro capturable |
| P4 | ¿Cómo mejorar la prevención de accidentes? | **Turno noche: 5,4x el riesgo** | ~14 incidentes/año evitables |
| P5 | *(fuera del radar)* ¿Qué nos cuesta la rotación? | **16,7% en el período limpio, plana, 55 renuncias/año** | **$23M – $195M/año** (central: $83M) |

**La conclusión de una línea:** TechnoStamp no tiene un problema de jubilaciones ni de equidad salarial. Tiene un problema de **retención** que cuesta un orden de magnitud más que los accidentes, y un problema de **gobierno del dato** que impide gestionar la seguridad.

> **Cómo leer las cifras de este informe.** Donde hay un rango, el rango es la respuesta — no un promedio con incertidumbre decorativa. El caso económico de la retención va de $23M a $195M anuales porque el 97% del costo por salida son supuestos nuestros, no mediciones de TechnoStamp (sección 9). Cerrar ese rango depende de dos datos que la empresa puede aportar, y esa es la primera pregunta que le haríamos al directorio.

---

## 2. Calidad de los datos — leer antes que cualquier número

Se aplicó el principio de raw inmutable: los CSV originales no fueron modificados. Todas las transformaciones están en `04_scripts/` y las copias derivadas en `datos_transformados/` con linaje en `_linaje.json`.

### Hallazgos de calidad que condicionan las conclusiones

| Hallazgo | Magnitud | Impacto en el análisis |
|---|---|---|
| **Encoding UTF-8 mal interpretado** | Todo el dataset | Verificado por hexdump (`c3 a9` = UTF-8). Un primer intento con `latin-1` producía mojibake. Corregido en origen. |
| **Dos fuentes de incidentes que no cierran** | 100 en panel vs 45 en eventos | **55% de los incidentes no tienen causa raíz, parte del cuerpo ni acción correctiva registrada.** Se adopta `eventos_rrhh` como fuente canónica por ser auditable. |
| **`es_posicion_critica` sin mantener** | 10 de 694 empleados (1,4%) | Inservible para planificación de sucesión. Se construyó un índice alternativo. |
| **Antigüedad declarada vs calculada** | 483 filas (5,0%) | Marcado con `flag_antig_inconsistente`. No se borró ninguna fila. |
| **Snapshots previos a la fecha de ingreso** | 71 filas (0,7%) | Marcado con `flag_snapshot_pre_ingreso`. |
| **Edad declarada vs fecha de nacimiento** | 51 filas (0,5%) | Marcado con `flag_edad_inconsistente`. |
| **Categorías duplicadas** | `Técnica`/`Técnico`, `Mixta`/`Mixto`, `high`/`Grave` | Normalizadas. |
| **Dotación informada vs observada** | Brief dice 450, los datos muestran 562 activos | A confirmar con el cliente: puede excluir contratistas o una planta. |
| **Acción correctiva sin variación** | 15 de 45 incidentes la registran, y las 15 dicen lo mismo | Ver sección 6: no hay análisis de causa raíz real. |

### Dos políticas que se declararon en vez de aplicarse a ciegas

**Vacíos.** No todo dato ausente es un dato perdido. Se clasificó cada columna con vacíos en tres motivos, y solo el tercero admite imputación:

| Motivo | Qué significa | Ejemplo |
|---|---|---|
| **No aplica** | La métrica no existe para ese grupo | `tasa_scrap_porcentaje`: 0,1% vacío en producción, 99,7% fuera de ella |
| **Estructural** | Falta por diseño del registro | `bonus_anual`: es anual dentro de un panel mensual (94,7% vacío) |
| **Real** | Vacío genuino, sin patrón de grupo | `ultimo_aumento_porcentaje` (5,3%) |

Consecuencia práctica: las métricas de producción se promedian **solo** dentro de su universo válido — 5.932 de 9.733 registros (60,9%). Promediarlas sobre toda la empresa mezcla poblaciones distintas. Detalle completo en `datos_transformados/politica_vacios.csv`.

**Valores extremos.** La regla estadística estándar marca 1.388 registros (14,3%) de salario como atípicos. **No se recortó ninguno**, y la razón está en los datos: la mediana salarial sube de forma estricta con cada nivel jerárquico — $1,54M → $2,22M → $3,16M → $5,33M → $8,20M. Los valores altos no son errores: son la estructura jerárquica de la compañía. Recortarlos habría aplastado los niveles de conducción contra el resto y roto la regresión de brecha salarial, que justamente controla por nivel.

> **Advertencia metodológica.** La discrepancia entre fuentes de incidentes no es un detalle técnico: cambió conclusiones. Usando el panel, los empleados con sobrecarga crónica mostraban 3,71x más accidentes. Usando la fuente auditable, muestran 0,47x — es decir, menos (z = −1,09, no significativo). **Cualquier decisión sobre seguridad basada en la columna del panel es una decisión basada en un dato que no se puede auditar.**

---

## 3. P1 — Riesgo de sucesión y jubilación

### La pregunta de Martina

> *"Varios de nuestros empleados más senior están cerca de jubilarse. ¿Cuántos puestos críticos están en riesgo en los próximos 12 meses?"*

### La respuesta: cuatro personas

De 562 empleados activos, **4 se jubilan en los próximos 12 meses** (0,7%). No hay más: la edad implícita de jubilación en los datos es 65 años y solo 4 personas superan los 60.

| Área | Puesto | Personas | Edad | Meses restantes | Dotación del puesto | Sucesores |
|---|---|---|---|---|---|---|
| Logística | Team Leader Logística | 2 | 62,5 | 9 | 5 | 3 |
| Logística | Supervisor de Logística | 1 | 64 | 6 | **1** | **0** |
| Estampado | Técnico Setup | 1 | 64 | 6 | 25 | 24 |

**Un solo caso merece acción inmediata:** el Supervisor de Logística es un puesto unipersonal — un *single point of failure* real que se va en 6 meses y no tiene backup. Los otros tres tienen cobertura natural.

### El riesgo que sí existe, y que nadie mencionó

La pirámide etaria tiene un **hueco estructural**: solo 20 personas (3,6%) tienen entre 50 y 59 años, frente a 243 (43%) entre 30 y 39.

```
60+      ████ 4
50-59    ███████████████ 20          ← el hueco
40-49    ███████████████████████████████████████████████████████ 164
30-39    ██████████████████████████████████████████████████████████████████████████████████ 243
<30      ████████████████████████████████████████████ 131
```

El problema no es que se jubile gente en 2026. Es que **en 10 años no va a haber una capa de seniors formados para tomar los puestos de conducción**, porque esa cohorte no existe hoy. Eso no se arregla con un plan de sucesión: se arregla con un plan de desarrollo a 5 años.

**Nivel de evidencia:** impacto estimado (descriptivo sobre censo completo).

---

## 4. P2 — Género: representación sí, salario no

### La pregunta de Martina

> *"¿Tendremos problemas de desbalance de género en algunas áreas?"*

### Lo que está sano: la equidad salarial

| Medición | Brecha F vs M | Interpretación |
|---|---|---|
| Cruda (media simple) | 0,9% | No usar sola — no controla por puesto ni nivel |
| Dentro del nivel 1 (n=464) | −0,6% | Mujeres cobran levemente más |
| Dentro del nivel 2 (n=76) | +0,8% | Dentro del ruido |
| Dentro del nivel 3 (n=17) | +0,5% | Dentro del ruido |
| **Regresión OLS ajustada** | **0,02%** | **t = −0,03 · no significativo · R² = 0,865 · n = 562** |

Controlando por nivel jerárquico, área, antigüedad, edad y performance, **el género no explica nada del salario**. Esto es un activo defendible: si mañana llega una auditoría de equidad, TechnoStamp pasa.

### Lo que no está sano: representación y promoción

- **Dotación global:** 37,0% mujeres (208 de 562).
- **Áreas por debajo del promedio:** Ensamble 26,8%, Ingeniería 28,6%, Mantenimiento Mecánico y RRHH 33,3%.
- **Embudo de promoción:** 37,5% en nivel 1 → 35,5% en nivel 2 → **29,4% en nivel 3**.

El embudo se angosta justo en el salto a jefaturas. Con n=17 en el nivel 3, la señal es débil estadísticamente, pero la dirección es consistente y el costo de monitorearla es cero.

**Nivel de evidencia:** la ausencia de brecha salarial es *impacto estimado* con control multivariado sólido. El embudo de promoción es *exploratorio* (n chico en niveles altos).

---

## 5. P3 — Horas extra: el hallazgo incómodo

### La pregunta de Martina

> *"Siento que ciertos equipos están sobrecargados con horas extra."*

### Martina tiene razón en el diagnóstico

- **$988M anuales** en horas extra = **8,3% de la nómina base**.
- Es **estructural, no un pico**: 17 meses sostenidos entre 9,9 y 10,5 h/mes, con tendencia creciente (+0,28 h/año).
- Equivale al trabajo de **34,8 personas a tiempo completo**.
- Producción duplica a soporte: Mantenimiento Eléctrico 12,1 h/mes, Pintura 11,9, Estampado 11,3 vs Administración 4,1, Ingeniería 3,6.
- **61 empleados (8,8%) están en sobrecarga crónica** (>70% de sus meses por encima del percentil 80, con ~17 h/mes).

### Pero la solución obvia destruye valor

La recomendación instintiva es "contratá gente en vez de pagar horas extra". **Los números dicen que no.**

| Concepto | Valor |
|---|---|
| Costo por hora extra | $14.474 |
| Costo por hora normal (blue collar) | $10.778 |
| **Recargo efectivo** | **1,34x** |
| Punto de equilibrio (cargas sociales) | **34,3%** |
| Cargas patronales reales en Argentina | ~24-27% + ART + aguinaldo + vacaciones → **>34%** |

**Regla:** conviene contratar solo si `(1 + cargas sociales) < 1,343`. Con el costo cargado real de un empleado argentino, esa condición no se cumple. Sustituir horas extra por dotación **aumenta el costo laboral**, no lo reduce.

| Escenario | FTE convertidos | Ahorro en HE | Costo de nuevos | **Neto** |
|---|---|---|---|---|
| Mínimo (20%) | 7,0 | $197,5M | $213,3M | **−$15,7M** |
| Esperado (35%) | 12,2 | $345,7M | $373,2M | **−$27,6M** |
| Máximo (50%) | 17,4 | $493,8M | $533,2M | **−$39,4M** |

### ¿Y el argumento de fatiga y seguridad?

Se testeó. Los sobrecargados crónicos:

- Se ausentan **+11,1% más por mes** (t = 2,73, significativo). Costo: **$4,75M/año** — real pero marginal.
- Rotan **19,7%** contra **16,4%** del resto, pero los márgenes de error se solapan ampliamente (11,6–31,3% contra 13,7–19,6%; z = 0,64). Con 61 personas no hay diferencia demostrable.
- **No se puede afirmar que se accidenten más.** Las dos fuentes se contradicen (3,71x vs 0,47x; z = −1,09).

**Conclusión honesta:** las horas extra son un tema de **capacidad y flexibilidad operativa**, no una bolsa de ahorro. El caso para actuar existe pero es de riesgo humano y de dependencia operativa, no financiero. No recomendamos un programa de reducción de horas extra justificado por ahorro, porque ese ahorro no existe.

**Nivel de evidencia:** el cálculo de costo es *impacto estimado* con supuesto explícito de cargas sociales (sensibilidad provista). El vínculo con accidentes es *no concluyente*.

---

## 6. P4 — Seguridad: un hallazgo sólido y un problema de gobierno

### La pregunta de Martina

> *"Los accidentes en planta nos preocupan. ¿Qué podemos hacer para mejorar la prevención?"*

### Hallazgo sólido: el turno noche

| Turno | Empleado-mes | Incidentes | Tasa ×1.000 |
|---|---|---|---|
| **Noche** | 2.124 | **25** | **11,8** |
| Administrativo | 2.099 | 8 | 3,8 |
| Rotativo | 868 | 2 | 2,3 |
| Mañana | 2.254 | 5 | 2,2 |
| Tarde | 2.256 | 5 | 2,2 |

*Tabla persistida en `tablas_soporte/P4_incidentes_por_turno.csv` y graficada en `visualizaciones/G11_incidentes_por_turno.png` (DEC-021).*

**El turno noche concentra el 56% de los incidentes y el 74% de los días perdidos, con 5,4x la tasa de mañana o tarde**, sobre exposiciones comparables (2.124 empleado-mes contra 2.254 y 2.256).

> **Límite del dato, a declarar junto con el hallazgo (business case, entrega 7).** El campo `turno_evento` coincide con el turno asignado a esa persona en el panel en **45 de 45 casos**: es el turno de la persona, no un dato levantado del accidente. Y `hora_evento` de los 25 casos rotulados "Noche" va de las **06:53 a las 22:00** — en todo el dataset no hay un solo incidente entre las 23:00 y las 06:00. **Sigue siendo cierto** que la población asignada al turno noche se accidenta 5,4 veces más; **no puede decirse** que los accidentes ocurran de madrugada, ni atribuirlos a la oscuridad, el horario o el sueño. Si la noche igualara la tasa de mañana o tarde, la brecha sería de **~14 incidentes por año**; contra el promedio de compañía (4,7 ×1.000), de **~10,6 por año**. Son **aritmética de brecha** —la distancia entre lo observado y una referencia elegida—, no un resultado esperado de ninguna intervención.

### Los ingresantes no son el problema — pero tampoco hay gradiente por antigüedad

| Antigüedad | Empleado-mes | Incidentes | Tasa ×1.000 |
|---|---|---|---|
| 0-6 meses | 449 | **0** | 0,0 |
| 6-12 meses | 188 | **0** | 0,0 |
| 1-2 años | 387 | 2 | 5,2 |
| 2-5 años | 2.943 | 11 | 3,7 |
| 5-10 años | 3.921 | 20 | 5,1 |
| **10+ años** | 1.713 | 12 | **7,0** |

**Cero accidentes en los primeros 12 meses.** La antigüedad mínima de un accidentado es de 14 meses según `antiguedad_meses_evento` de la ficha del evento; la mediana, 6,6 años.

> **Corrección (business case, entrega 9).** Una versión previa de esta sección leía en esta tabla que *el riesgo sube con la experiencia* y lo atribuía a la **complacencia del personal experimentado**. **Eso no se sostiene.** Un chi-cuadrado de homogeneidad sobre las seis bandas da **5,68 con 5 grados de libertad, p = 0,339**: las tasas no se distinguen entre sí. Y la serie ni siquiera es monótona — cae de 5,2 a 3,7 antes de volver a subir. Los ceros de las dos primeras bandas tampoco prueban nada: con 449 y 188 empleado-mes de exposición, lo esperable bajo tasa pareja son ~2 y ~1 incidentes, así que observar cero es compatible con el azar.
>
> **Lo que sí vale de este hallazgo es negativo, y sigue siendo valioso:** refuta que los ingresantes sean el problema. No alcanza para afirmar un gradiente, ni para atribuirle una causa. Si existe un efecto de antigüedad, la hipótesis razonable es que a los veteranos se les asignan las tareas de riesgo — y esa es una variable del evento que no está registrada.

> Este es el hallazgo que más cambió durante el análisis. La columna del panel sugería 78 incidentes ×1.000 en los primeros 6 meses (10x el promedio). La fuente auditable dice cero. De haber usado la primera, la recomendación habría sido reforzar el onboarding — plata dirigida a un problema inexistente.

### Dónde duele: concentración de la gravedad

- **6 incidentes graves (13%) causan 109 de 138 días perdidos (79%)** y $600.000 de $975.000 en costo.
- **Caídas y sobreesfuerzo = 63% de los días perdidos** (51 y 36 días respectivamente).
- Manos, dedos y brazos: 24 de 45 incidentes.

### El problema de fondo: la investigación de accidentes no existe

Hay dos brechas encadenadas, y la segunda es peor que la primera.

**Primera: más de la mitad de los incidentes no se investiga.** De ~100 incidentes registrados en nómina, solo 45 tienen ficha en `eventos_rrhh`. Sobre los otros 55 no se sabe qué pasó.

**Segunda: de los 45 que sí tienen ficha, solo 15 registran una acción correctiva — y las 15 dicen exactamente lo mismo.**

| Severidad | Incidentes | Con acción correctiva registrada |
|---|---|---|
| Grave | 6 | 6 |
| Moderado | 9 | 9 |
| Leve | 30 | **0** |

La única acción correctiva que aparece en toda la base, en los 15 casos, es la frase *"Capacitación refuerzo seguridad"*.

El proceso distingue bien por gravedad — todo lo grave y moderado se documenta, lo leve no. Pero **la respuesta es siempre idéntica, sin importar si fue una caída, una quemadura o un atrapamiento.** Eso no es análisis de causa raíz: es una respuesta refleja. Y explica por qué la capacitación en seguridad llega siempre tarde y siempre igual.

Ningún programa de prevención puede funcionar así: no se puede prevenir lo que no se investiga, y no se corrige lo que siempre se responde de la misma forma.

### La capacitación en seguridad no llega a quien se accidenta

Con la fuente auditable, cruzando fechas de capacitación contra fechas de incidente:

| De los 45 incidentes | n | % |
|---|---:|---:|
| Con capacitación de seguridad **previa** al hecho | 5 | 11% |
| Con capacitación de seguridad **posterior** al hecho | 4 | 9% |
| **Sin ninguna capacitación de seguridad** | **36** | **80%** |

Y a nivel persona: los accidentados tienen capacitación de seguridad en el **22,0%** de los casos (9 de 41) contra el **19,1%** de los no accidentados (121 de 634) — Fisher exacto bilateral, **p = 0,683**. Es la proporción de toda la empresa (**19,3%**, 130 de 675).

**La capacitación de seguridad cubre al 19,3% de la gente y se asigna sin ninguna relación con quién se lastima**, ni antes ni después del hecho.

> **Corrección (business case, entrega 8).** Una versión previa de esta sección afirmaba que las áreas con más horas de training tienen más incidentes, y concluía que **se capacita después del accidente**. Las dos partes caen. La correlación área a área es **r = 0,394 con p = 0,260** sobre 10 áreas: no se distingue de cero. Y la temporalidad nunca se había calculado — el código agregaba totales del período. Corrido el cruce, *se entrena después del accidente* describe **4 casos de 45**, y esos cuatro recibieron el curso a una mediana de **108 días** del hecho (máximo 344): es el calendario normal, no una reacción.
>
> La cifra de **$34M anuales** que citaba esa versión es el costo de **todo** el training de la compañía ($48,2M en 17 meses). El training de seguridad son **$3,8M** en el período, unos $2,7M anualizados.
>
> **Lo que no puede afirmarse en ninguna dirección** es si la capacitación previene: la asignación no fue aleatoria ni está documentada, así que capacitados y no capacitados no son comparables. Lo que corresponde es registrar el criterio de asignación y hacer una **evaluación de impacto**, no inferir un efecto de estos datos.

**Nivel de evidencia:** el efecto turno noche es *impacto estimado* (consistente en dos fuentes, magnitud grande). La curva de antigüedad y el resto son *exploratorios* (n=45 total).

---

## 7. P5 — Rotación: el problema que nadie puso sobre la mesa

Esta pregunta no estaba en la lista de Martina. **Es la más cara de todas.**

### Magnitud

**Antes de los números, una corrección del período.** El archivo arranca en enero de 2024 y ese primer mes registra 19 salidas, el triple de un mes normal. Los 19 aparecen **una sola vez** en el panel, contra 9,5 meses del resto: son personas que ya estaban saliendo cuando se hizo el corte del archivo. No son rotación generada en el período — son arrastre. Se excluyen.

- **113 salidas** sobre 675 personas expuestas en 16 meses (febrero 2024 – mayo 2025) = **16,7% acumulado del período**, no 19,0% (la cifra con el arrastre de enero incluido).
- **65% son renuncias voluntarias** (73 de 113) — la porción sobre la que se puede actuar.
- Renuncias voluntarias anualizadas: **55 por año**.
- **La rotación no sube ni baja.** La tendencia del período limpio es de +0,05 puntos por año (t = 0,08): es una línea plana con ruido, no una curva. No es un incendio que se agrava, pero tampoco cede solo.

### Dos patrones que se sostienen, y uno que no

**1. Mantenimiento Eléctrico se está desangrando. Esto sí se sostiene.**
34,8% de rotación sobre 46 personas. Con esa cantidad de gente el número exacto no es confiable, pero el rango real va de **22,7% a 49,2%** — y el piso de ese rango ya está muy por encima del promedio de la compañía (16,7%). Es la única área que se distingue estadísticamente. Nadie la mencionó.

| Área | Personas | Salidas | Rotación | Rango real | ¿Se distingue? |
|---|---|---|---|---|---|
| **Mantenimiento Eléctrico** | 46 | 16 | **34,8%** | **22,7 – 49,2%** | **Sí, peor** |
| Estampado | 185 | 37 | 20,0% | 14,9 – 26,3% | No |
| Ensamble | 151 | 24 | 15,9% | 10,9 – 22,6% | No |
| Pintura | 80 | 12 | 15,0% | 8,8 – 24,4% | No |
| Calidad | 71 | 9 | 12,7% | 6,8 – 22,4% | No |
| *Promedio compañía* | 675 | 113 | *16,7%* | — | — |

> **Por qué importa el rango.** Una versión anterior de este informe marcaba también a Estampado como área problemática por su 20,0%. Su rango real va de 14,9% a 26,3% y **contiene al promedio**: con los datos disponibles no se puede afirmar que Estampado rote distinto del resto de la empresa. Dirigir recursos ahí no tendría sustento.

> **El hallazgo sobrevive incluso corrigiendo por haber testeado diez áreas.** Testear diez áreas contra el promedio de la empresa acumula la probabilidad de una falsa alarma: con el umbral habitual del 5%, alguna de las diez puede salir "significativa" por puro azar. La corrección de Bonferroni baja ese umbral a 0,5% (0,05 ÷ 10) para compensarlo. Mantenimiento Eléctrico lo pasa con margen: p = 0,00105 contra un umbral de 0,0050. Es la diferencia entre "la única área que se distingue, aunque no corregimos por múltiples pruebas" y "se distingue incluso corrigiendo por haber testeado las diez" — ver `tablas_soporte/P5_rotacion_por_area_con_IC.csv`, columnas `p_valor` y `sig_bonferroni`.

**2. Se van cuando ya están formados. Esto también se sostiene.**
La antigüedad mediana al salir es **5,2 años**. No es rotación temprana de gente que no encajó: es fuga de personal con conocimiento acumulado, justo cuando la inversión en formación empezaba a rendir.

**3. "Se van los buenos" — esto NO se sostiene.**
Una versión anterior afirmaba que los top performers rotan un 35% más. Corregido el período y calculado el margen de error, los rangos se solapan:

| Grupo | Personas | Rotación | Rango real |
|---|---|---|---|
| Top performers | 59 | 23,7% | 14,7 – 36,0% |
| Resto | 616 | 16,1% | 13,4 – 19,2% |

La diferencia aparente puede ser azar (z = 1,51). Con 59 top performers no hay suficiente evidencia. **La afirmación se retira**, y con ella cualquier iniciativa que se justifique solo por retener top performers. Vale la pena volver a medirlo con más datos: la dirección del efecto es la esperable, pero hoy no se puede afirmar.

> **Señal a investigar, no a concluir:** los que renuncian voluntariamente tuvieron su último aumento hace **1,0 mes** en promedio, frente a **4,5 meses** de los que se quedan. Esto es contra-intuitivo y probablemente refleja contraofertas fallidas o un artefacto en cómo se registra el campo al momento de la baja. **No usar como evidencia sin validar con RRHH.**

**Nivel de evidencia:** magnitud y costo son *impacto estimado* (supuestos de vacancia y rampa explícitos). Las causas de la renuncia son *exploratorias* — los datos no contienen entrevistas de salida.

---

## 8. Matriz de oportunidades

| Oportunidad | Impacto | Factibilidad | Datos | Evidencia | Esfuerzo | **Prioridad** |
|---|---|---|---|---|---|---|
| **A. Retención, con foco en Mantenimiento Eléctrico** | Alto ($23M – $195M/año) | Alta | Buenos, salvo el costo por salida | Impacto estimado | Medio | **1** |
| **B. Trazabilidad de incidentes** | Habilitador | Alta | Deficientes | Causal (es una brecha de proceso) | Bajo | **2** |
| **C. Rediseño del turno noche** | Medio (14 incidentes/año) | Media | Suficientes | Impacto estimado | Medio | **3** |
| **D. Backup del Supervisor de Logística** | Alto y puntual | Alta | Buenos | Descriptivo | Bajo | **4** |
| **E. Reciclaje de seguridad para 10+ años** | Medio | Alta | Débiles (n=45) | Exploratorio | Bajo | **5** |
| ~~F. Sustituir horas extra por dotación~~ | **Negativo** | — | Buenos | Impacto estimado | — | **Descartada** |
| **G. Plan de desarrollo para el hueco 50-59** | Alto a 5 años | Media | Buenos | Descriptivo | Alto | Estratégica |

---

## 9. Business case

### Primero: cuánto de este número es dato y cuánto es supuesto

Todo el caso económico depende de cuánto cuesta una salida. Ese número está hecho de esto:

| Componente | Monto | Peso | Origen |
|---|---|---|---|
| Reclutamiento | $150.000 | 2,5% | **Registrado por TechnoStamp** |
| Onboarding | $50.000 | 0,8% | **Registrado por TechnoStamp** |
| Vacancia del puesto | ~$1,5M – $3,0M | ~50% | *Supuesto nuestro* |
| Rampa del ingresante | ~$1,1M – $5,7M | ~47% | *Supuesto nuestro* |

**El 97% del costo por salida son supuestos nuestros, no mediciones del cliente.** Los insumos son reales — el salario medio del que se va ($1,90M/mes) y los 47 días que tarda cubrir el puesto salen de los datos. Lo que suponemos es *cuánto de ese salario se pierde efectivamente* mientras el puesto está vacío, y *cuánto tarda un ingresante en rendir como el que se fue*.

Por eso el caso se presenta como rango, con cada supuesto a la vista.

### El rango

| Escenario | Supuesto | Costo por salida |
|---|---|---|
| **Conservador** | El equipo absorbe la mitad del trabajo; el ingresante rinde al 70% desde el primer mes | $2,84M |
| **Central** | El puesto queda descubierto; el ingresante rinde al 50% durante 3 meses | $6,04M |
| **Agresivo** | Puesto descubierto y rampa de 6 meses, típica de perfiles técnicos | $8,90M |

Sobre **55 renuncias voluntarias por año**, el ahorro anual según cuánto se reduzca:

| Escenario | Reducir 15% | Reducir 25% | Reducir 40% |
|---|---|---|---|
| Conservador | $23,3M | $38,8M | $62,1M |
| **Central** | $49,6M | **$82,7M** | $132,4M |
| Agresivo | $73,1M | $121,8M | $194,8M |

**Rango completo: $23M a $195M por año. Punto central: $83M.** Es un rango de 8,4 veces, y se reporta así a propósito: esconderlo detrás de una cifra única sería presentar como precisión algo que no la tiene.

**Piso verificable: $1,6M por año.** Es lo que da el cálculo usando *solo* los dos datos que TechnoStamp mide, sin ningún supuesto nuestro. No es el caso económico — es el suelo debajo del cual la afirmación no puede caer.

### Cómo cerrar el rango

Dos datos que la empresa casi seguro tiene y que convertirían el 97% de supuesto en medición:

1. **Producción promedio de un operario formado** (unidades por mes, por puesto).
2. **Cuántos meses tarda un ingresante en alcanzar ese nivel.**

Con eso, la vacancia y la rampa se calculan en vez de suponerse, y el rango de 8,4x se comprime a algo defendible ante el directorio.

### Horizonte 1-3 años (escenario central, reducción del 25%)

| | Año 1 | Año 2 | Año 3 |
|---|---|---|---|
| Beneficios | $85,4M | $85,4M | $85,4M |
| Costo de setup | $18,0M | — | — |
| Costo de operación | $12,0M | $12,0M | $12,0M |
| **Flujo neto** | **$55,4M** | **$73,4M** | **$73,4M** |
| Acumulado | $55,4M | $128,8M | $202,2M |

*Beneficios = $82,7M de retención + $2,7M de seguridad. Setup y operación son estimaciones de orden de magnitud; deben validarse con presupuesto real.*

- **ROI año 1 (escenario central):** 185%
- **En el escenario conservador**, el beneficio anual ($38,8M) sigue superando el costo de operación — el caso no se cae, se achica.

**Advertencia:** el caso económico descansa casi enteramente en la oportunidad A. Si la retención no se mueve, no cierra. Las oportunidades B, C y D se justifican por gestión de riesgo, no por retorno financiero — y hay que presentarlas así al directorio, no maquilladas de ahorro.

---

## 10. Fichas de transición

### Ficha A — Retención de talento crítico

- **Problema:** 55 renuncias voluntarias por año, con un costo estimado entre $23M y $195M anuales. Concentradas en Mantenimiento Eléctrico, la única área que se distingue estadísticamente del promedio.
- **Decisión a automatizar:** identificar mensualmente qué empleados tienen alto riesgo de renuncia y alto valor, para intervención proactiva del manager.
- **Palanca / KPI / baseline:** costo de rotación · % rotación (acumulada del período) · **16,7%**, plana durante los 16 meses limpios.
- **Datos disponibles:** panel mensual completo con performance, salario, antigüedad, aumentos, ausentismo y horas extra.
- **Brechas:** tres, en orden de urgencia. (1) **El costo por salida es 97% supuesto** — faltan la producción de un operario formado y los meses de rampa. (2) No hay entrevistas de salida ni encuestas de clima: se sabe *quién* se va, no *por qué*. (3) El campo `meses_desde_ultimo_aumento` tiene un comportamiento anómalo en las bajas que hay que auditar.
- **Plan de remediación:** instrumentar entrevistas de salida estructuradas (3 meses) antes de invertir en modelos predictivos.
- **Solución propuesta:** tablero mensual de riesgo de fuga por área y persona, alimentado por el panel existente. Regla de negocio simple primero; modelo predictivo solo después de tener 12 meses de entrevistas de salida.
- **Validación pendiente:** por qué Mantenimiento Eléctrico duplica al resto. Hipótesis a testear: competencia salarial externa por perfiles eléctricos, carga de guardias, o un problema de liderazgo local.
- **Próximo paso:** diagnóstico cualitativo en Mantenimiento Eléctrico — 46 personas, es abordable en dos semanas.

### Ficha B — Trazabilidad de incidentes de seguridad

- **Problema:** 55% de los incidentes no tienen causa raíz registrada.
- **Decisión a automatizar:** garantizar que todo incidente que impacta la nómina genere una ficha de investigación obligatoria.
- **Palanca / KPI / baseline:** calidad del dato de seguridad · % incidentes con causa raíz · **45%**.
- **Meta:** 95% en 6 meses.
- **Solución propuesta:** validación en el sistema de carga — no se cierra el mes de nómina con incidentes sin ficha asociada. Es control de proceso, no analítica.
- **Por qué es la #2 pese a no tener ROI:** sin esto, ninguna conclusión sobre seguridad es defendible. Es el habilitador de la ficha C.
- **Próximo paso:** auditar los 55 incidentes sin ficha para entender por qué se perdieron.

### Ficha C — Rediseño de seguridad del turno noche

- **Problema:** 5,4x la tasa de incidentes de mañana/tarde; 74% de los días perdidos.
- **Palanca / KPI / baseline:** días perdidos por accidente · tasa de incidentes en noche · **11,8 ×1.000 empleado-mes**.
- **Meta:** converger a la tasa diurna (2,2) en 18 meses → ~14 incidentes evitados/año.
- **Datos disponibles:** suficientes para dimensionar, insuficientes para diagnosticar la causa (n=25 incidentes en noche).
- **Validación pendiente:** ¿es iluminación, dotación de supervisión, fatiga circadiana o menor presencia de mantenimiento? Los datos no lo dicen.
- **Próximo paso:** walkthrough nocturno con seguridad e higiene antes de comprometer inversión. **No invertir sobre la base de este análisis solo.**

---

## 11. Qué NO se puede afirmar con estos datos

Lo que sigue es tan importante como los hallazgos:

1. **Nada causal.** No hay experimentos ni variación exógena. Todo es asociación con controles.
2. **Que las horas extra causen accidentes.** Las fuentes se contradicen; n insuficiente.
3. **Por qué se va la gente.** No hay entrevistas de salida. Se sabe quién y cuánto cuesta, no por qué.
4. **Que exista discriminación en promoción.** El embudo de género es consistente en dirección pero n=17 en nivel 3 no permite concluir.
5. **La causa del exceso de incidentes en el turno noche.** Se sabe que existe y es grande; no se sabe por qué.
6. **Cualquier conclusión sobre seguridad basada en el 55% de incidentes sin ficha.**
7. **Que los top performers roten más que el resto.** Los márgenes de error se solapan (23,7% contra 16,1%, z = 1,51). Con 59 top performers no alcanza. *Afirmación retirada de una versión anterior.*
8. **Que Estampado rote más que el promedio.** Su rango real (14,9 – 26,3%) contiene al promedio de la compañía. *Afirmación retirada de una versión anterior.*
9. **Cuánto cuesta realmente una salida.** El 97% de la cifra son supuestos nuestros. Se reporta como rango y se pide al cliente los dos datos que lo cerrarían.

### Afirmaciones retiradas durante la revisión

Tres afirmaciones de versiones anteriores no sobrevivieron a un control más estricto. Se listan porque el directorio merece saber qué se corrigió y por qué:

| Afirmación retirada | Por qué se cayó |
|---|---|
| "Los accidentes se concentran en los primeros 6 meses" | Venía de una fuente no auditable. La fuente con causa raíz muestra cero incidentes en los primeros 12 meses. |
| "Los top performers rotan un 35% más" | Los márgenes de error se solapan; la diferencia puede ser azar. |
| "La rotación viene bajando" | La caída aparente la producía el arrastre de enero 2024. Corregido el período, la tendencia es plana. |

---

## 12. Próximos experimentos recomendados

| Experimento | Objetivo | Duración | Prerrequisito |
|---|---|---|---|
| Entrevistas de salida estructuradas | Convertir la rotación de "cuánto cuesta" a "por qué pasa" | 3 meses | Ninguno |
| Diagnóstico en Mantenimiento Eléctrico | Explicar el 34,8% | 2 semanas | Ninguno |
| Ficha obligatoria de incidentes | Cerrar la brecha del 55% | 1 mes | Cambio en el sistema |
| Walkthrough del turno noche | Explicar el 5,4x | 2 semanas | Ninguno |
| Piloto de reciclaje de seguridad para 10+ años | Testear la hipótesis de complacencia | 6 meses | Ficha de incidentes operativa |

---

## 13. Reproducibilidad

| Artefacto | Ubicación |
|---|---|
| Datos crudos (inmutables) | `02_datos/01_Originales/` |
| Scripts del pipeline | `04_scripts/` (18 scripts; `01`…`18`, ver orden de ejecución abajo) |
| Datos transformados | `06_resultados/Discovery/datos_transformados/` |
| **Receta de limpieza reejecutable** | `datos_transformados/transformaciones.json` (31 pasos) |
| **Política de vacíos por columna** | `datos_transformados/politica_vacios.csv` (13 columnas) |
| **Revisión sistemática de variables** | `06_resultados/EDA/EDA_report.md` (54 alertas) |
| Visualizaciones | `06_resultados/Discovery/visualizaciones/` (14 PNG: G1–G14) |
| Tablas de soporte | `06_resultados/Discovery/tablas_soporte/` (17 CSV + `BC_supuestos.json`) |
| Registro de decisiones | `decisions.md` (DEC-001 a DEC-021) |
| Entorno | conda `nivii_ai` (Python 3.12) |

**Orden de ejecución real.** Dos scripts quedaron superados y no se ejecutan: `03_limpieza.py` (reemplazado por `13_limpieza_v2.py`) y `09_business_case.py` (reemplazado por `17_business_case_v2.py`). El orden vigente, tal como corre el notebook orquestador:

`01_perfilado` → `02_calidad` → **`13_limpieza_v2`** → `04_p1_p2` → `05_verif_critica` → `06_p3_p4_p5` → `07_verif_incidentes_p5` → `08_visualizaciones` → `10_sensibilidad_he` → `11_verif_cronicos_seguridad` → `12_diagnostico_gaps` → `14_eda_sistematico` → `15_diagnostico_fragilidad` → `16_rotacion_temporal` → **`17_business_case_v2`** → `18_visualizaciones_decision`

> **Nota de trazabilidad (2026-09-06).** `tablas_soporte/BC_resumen_oportunidades.csv`, salida del script superado `09_business_case.py`, sigue en la carpeta y contradice el rango vigente de `BC_rango_retencion.csv` (`17_business_case_v2.py`). Su retiro está pendiente como decisión abierta en `decisions.md`.

**Cómo reprocesar datos nuevos.** Cuando TechnoStamp envíe los próximos meses, `transformaciones.json` contiene los 31 pasos de limpieza con sus parámetros ya calculados — renombres, conversiones de tipo, unificación de categorías, política de vacíos y reglas de coherencia. Se reaplican en orden para obtener exactamente el mismo tratamiento, sin depender de que alguien recuerde qué se hizo.
