# 04 · Puente Discovery → Automation

**Subentregables 6 en adelante.** Uno o dos insights por entrega. Para cada uno: tipo de proyecto
posible, datos faltantes reales, veredicto explícito y mapa `ds-*` solo si se justifica.

## El criterio, antes de aplicarlo

De `ESTUDIO_conceptos_technostamp.md` §1. Un modelo se justifica cuando la decisión que alimenta
cumple **las tres** condiciones, no una:

| Condición | Pregunta concreta |
|---|---|
| **Frecuencia** | ¿La decisión se toma muchas veces? ¿Cada cuánto? |
| **Escala** | ¿Es una escala que una persona no puede revisar caso por caso? |
| **Cuello de botella** | ¿El problema es la **velocidad de scorear**, o la **calidad de la inferencia**? |

Si el cuello de botella es entender *por qué* pasa algo, eso es inferencia, y un modelo predictivo
no lo resuelve: lo esconde detrás de una probabilidad.

**Regla de honestidad que gobierna este documento:** no recomendar ML porque sea técnicamente
posible. Y cuando el veredicto es negativo, dejar escrito **el umbral** — qué tendría que cambiar
para que fuera sí. Un "no" sin umbral es una opinión, no un veredicto.

---

# Entrega 6 · I2 y I10 — el candidato obvio a modelo de churn

Se tratan juntos porque son las dos mitades de la misma pregunta de negocio: **quién se va**
(I2) y **cuánto cuesta** (I10). Es el lugar donde la tentación de modelar es más fuerte, y por eso
merece la respuesta más trabajada del documento.

---

## I2 — Rotación concentrada en Mantenimiento Eléctrico

> **Insight.** De diez áreas, una sola rota distinto del promedio de la compañía, y rota al doble:
> Mantenimiento Eléctrico, 34,8% (16 de 46), IC95 22,7–49,2%, p = 0,00105 contra un umbral
> Bonferroni de 0,005.

### 1. Tipo de proyecto posible

**El candidato natural es `supervisado`:** un modelo de riesgo de fuga que asigne a cada empleado
una probabilidad de renunciar en los próximos N meses.

Si se hiciera, se definiría así:

| Elemento | Definición |
|---|---|
| **Variable objetivo** | `renuncia voluntaria en los próximos 6 meses` — binaria, por empleado-mes. Solo renuncia voluntaria: despido, jubilación, fin de contrato y reestructuración no son lo que una acción de retención puede evitar |
| **Anticipación necesaria** | Al menos 3 meses. Menos que eso no deja margen para conversar, revisar compensación o mover a la persona de puesto. Una alerta a 30 días llega tarde para todo salvo la contraoferta |
| **Unidad de análisis** | Empleado-mes, con censura a derecha tratada explícitamente |

**Alternativa `no supervisado`:** segmentar perfiles de riesgo sin etiqueta. Se descarta antes de
evaluarla, porque la etiqueta existe y es de buena calidad — el problema no es la falta de
etiqueta, es la cantidad.

### 2. Datos faltantes

Conectados con brechas ya identificadas, ninguna inventada:

| Brecha | Por qué bloquea este proyecto |
|---|---|
| **N3 — entrevistas de salida estructuradas** | No existe ninguna. El modelo podría aprender *quién* se parece a los que se fueron, pero nadie sabría *qué hacer* con esa alerta. Una lista de nombres sin un motivo accionable no es un producto |
| ~~N6~~ **Corregido en la entrega 8** | Este campo parecía la señal más discriminante del dataset (1,0 mes en renuncias vs 4,5 en activos). **Es un artefacto de registro**, confirmado: ninguna de las 132 bajas supera el valor 3, y los jubilados muestran el mismo perfil que los renunciantes. No es una brecha que bloquee el proyecto — es una **variable prohibida**: entrenar sobre ella sería predecir el acto de registrar la baja, no la decisión de irse |
| Ausencia de encuesta de clima o satisfacción | Las variables que la literatura y el sentido común señalan como motoras de la renuncia —relación con la jefatura, percepción de equidad, carga— no están medidas |

### 3. Veredicto explícito

**`ninguno — sigue siendo Discovery recurrente`.**

Las tres condiciones, una por una:

| Condición | Qué muestra el caso |
|---|---|
| **Frecuencia** | **No cumple.** La decisión real es "¿invertimos en retención en Mantenimiento Eléctrico?". La toma un directorio una o dos veces al año, no todos los días |
| **Escala** | **No cumple, y no está cerca.** El área tiene **46 personas**. Un jefe puede sentarse con las 46 en dos semanas. Toda la empresa son 694, revisables una por una si hiciera falta |
| **Cuello de botella** | **Es calidad de inferencia, no velocidad de scoring.** La pregunta abierta no es *quién* se va: es *por qué*. Y eso no lo contesta un modelo predictivo — lo contesta la entrevista de salida que todavía no existe |

**Y hay una razón adicional, puramente técnica, que sella el veredicto.**

| Cantidad | Valor |
|---|---:|
| Personas en el universo | 694 |
| Salidas totales | 132 |
| **Renuncias voluntarias — la clase positiva real** | **89** |
| Renuncias voluntarias en Mantenimiento Eléctrico | **11** |
| Columnas candidatas a variable en el panel | **60** |

**89 casos positivos contra 60 variables candidatas.** Con esa proporción, un modelo no aprende el
fenómeno: aprende el ruido de esta muestra en particular. Y si se acota a la pregunta que de verdad
importa —el área que rota distinto— la clase positiva son **11 personas**. No hay técnica de
balanceo, regularización ni validación cruzada que arregle eso, porque el problema no es el
algoritmo: es que el fenómeno ocurrió once veces.

A eso se suma que la propia etiqueta está mal definida por la **censura a derecha**: quien figura
como activo no es un "no se va", es un "todavía no se fue". Entrenar un clasificador binario sobre
esa etiqueta le enseña al modelo que la gente que lleva poco tiempo se queda.

**Lo que sí corresponde hacer, y es más barato y más útil:** rotación por área con intervalo de
confianza, recalculada cada trimestre con la misma fórmula, y una entrevista de salida
estructurada en cada baja. Eso responde la pregunta del negocio con la evidencia que ya existe.

#### El umbral — qué cambiaría el veredicto

No es una respuesta permanente. Se revisa si pasan **las tres** cosas a la vez:

1. **Volumen:** que el universo pase de cientos a **decenas de miles** de personas, o que el
   horizonte de datos crezca a varios años, de modo que la clase positiva llegue al orden de miles
   y no de decenas.
2. **Frecuencia de decisión:** que exista una acción de retención **individual, presupuestada y
   recurrente** —no una decisión anual de directorio— que un manager deba asignar mes a mes sobre
   más gente de la que puede revisar.
3. **Cuello de botella:** que ya se sepa *por qué* se va la gente (N3 en régimen, con al menos un
   par de años de motivos estructurados) y que lo que falte sea *a quién priorizar primero*.

Mientras el negocio siga sin saber por qué se van, cualquier modelo estaría automatizando una
decisión que todavía nadie sabe tomar.

### 4. Mapa ds-*

> **No pasar a ds-06 todavía; sostener como análisis recurrente de Discovery y mejorar la captura
> de datos.**

Prioridad de captura: **N3** (entrevistas de salida). N6 quedó resuelta en la entrega 8 — el campo
es un artefacto y se retira del análisis, no se audita para poder usarlo.

---

## I10 — El costo de la rotación es un rango de 8,4x, y el 97% es supuesto propio

> **Insight.** El caso económico va de $23,3M a $194,8M anuales. Del costo por salida central
> ($6.044.356), solo **$200.000** —el 3,3%— provienen de algo que TechnoStamp mide.

### 1. Tipo de proyecto posible

**`ninguno — sigue siendo Discovery`**, y en este caso ni siquiera hay un candidato razonable que
descartar.

Vale explicar por qué, porque es un error conceptual frecuente: lo que falta acá **no es un
patrón que aprender, son dos cantidades que medir**.

| Componente | Monto (escenario central) | Naturaleza |
|---|---:|---|
| Reclutamiento + onboarding | $200.000 | **Medido** por el cliente |
| Sueldo perdido durante la vacancia | $2.991.905 | 47,2 días de time-to-fill × $1.901.634 de salario medio del saliente × **fracción supuesta** |
| Rampa del ingresante | $2.852.451 | 3 meses × salario × **rendimiento supuesto** |

La "fracción del sueldo que se pierde mientras el puesto está vacío" y "cuántos meses tarda un
ingresante en rendir como el que se fue" **no son inferencias sobre datos existentes**. Son hechos
del mundo que nadie registró. Ningún modelo los puede recuperar de un dataset que no los contiene:
un algoritmo entrenado sobre estos datos aprendería nuestros propios supuestos y los devolvería con
apariencia de resultado.

Esa es la trampa a nombrar en voz alta. Un número que sale de un modelo no es más verdadero que el
supuesto que lo alimentó — solo es más difícil de auditar.

### 2. Datos faltantes

| Brecha | Qué es exactamente |
|---|---|
| **N1** | Producción promedio mensual de un operario ya formado, por puesto. Derivable del sistema de producción / MES; el proyecto ya observa `unidades_producidas` en las tres áreas de producción |
| **N2** | Meses desde el ingreso hasta alcanzar ese nivel. Derivable de N1 cruzado con la fecha de ingreso del panel |

Ambas son **recolección**, no modelado. Con ellas, el 97% que hoy es juicio pasa a ser medición.

### 3. Veredicto explícito

**`ninguno — sigue siendo Discovery recurrente`.**

| Condición | Qué muestra el caso |
|---|---|
| **Frecuencia** | **No cumple.** El costo por salida se recalcula una o dos veces al año, cuando cambian los salarios o el time-to-fill |
| **Escala** | **No cumple.** Son 52 puestos distintos y 90 contrataciones en 17 meses. Una planilla lo cubre |
| **Cuello de botella** | **Ni scoring ni inferencia: es medición.** Faltan dos números que nadie tomó. No hay nada que inferir todavía |

Una vez que N1 y N2 existan, la curva de rampa por puesto se estima con estadística descriptiva
sobre las ~90 contrataciones del período —promedio de producción por mes desde el ingreso, por
puesto—. Eso es un gráfico, no un modelo. Y con 52 puestos y 90 contrataciones, muchos puestos van
a tener uno o dos ingresantes: el resultado va a ser un rango, otra vez, pero un rango **medido**
en lugar de supuesto. Que es exactamente el objetivo.

#### El umbral — qué cambiaría el veredicto

Prácticamente nada de lo que se ve desde acá. Este insight no se convierte en un proyecto de ML por
crecer: se convierte en un **indicador de gestión** en cuanto N1 y N2 se midan. El único escenario
en que aparecería modelado es si TechnoStamp quisiera **pronosticar** el time-to-fill de una
vacante antes de abrirla, sobre miles de búsquedas históricas. Con 90 contrataciones en 17 meses,
eso está a dos órdenes de magnitud de distancia.

### 4. Mapa ds-*

> **No pasar a ds-06 todavía; sostener como análisis recurrente de Discovery y mejorar la captura
> de datos.**

Prioridad de captura: **N1** y **N2**. El entregable no es un modelo: es un rango más angosto y
defendible ante el directorio.

---

## Cierre de la entrega 6

Los dos insights más "modelables" del proyecto —el que todos esperan que sea un churn model y el
que tiene un número grande en pesos— dan **el mismo veredicto: ninguno**. Y por motivos distintos,
que vale distinguir:

- **I2 no se modela por escala y por cuello de botella.** El fenómeno ocurrió 89 veces en toda la
  empresa y 11 en el área que importa, y lo que falta saber es *por qué*, no *quién*.
- **I10 no se modela porque el problema no es de inferencia.** Faltan dos mediciones. Un modelo
  entrenado sobre estos datos devolvería nuestros propios supuestos disfrazados de resultado.

Es la misma conclusión con la que arrancó el proyecto —§1 del `ESTUDIO`: la primera decisión fue no
construir un modelo— sostenida ahora insight por insight, con el umbral escrito al lado.

---

**Siguiente:** entrega 7 — **I4** (seguridad nocturna) e **I6** (concentración de la gravedad).
El segundo candidato a modelo predictivo, donde n = 45 y n = 6 son buena parte de la respuesta.

---

# Entrega 7 · I4 e I6 — el segundo candidato a modelo predictivo

El primer candidato era predecir **quién se va** (entrega 6). El segundo es predecir **quién se
accidenta**, y de paso **qué tan grave**. Se tratan juntos porque comparten el mismo techo: el
fenómeno completo ocurrió 45 veces, y la parte que importa, 6.

Antes de entrar, dos verificaciones nuevas que cambian el análisis y que conviene tener a mano.

---

## Dos hallazgos previos, verificados en esta entrega

### V1 — `severidad` no es una variable observada: es una recodificación de `dias_perdidos`

Rangos de días perdidos por categoría, sobre los 45 incidentes:

| Severidad | n | Días perdidos observados |
|---|---:|---|
| Leve | 30 | **0** — los treinta, sin excepción |
| Moderado | 9 | 1, 2, 3, 4, 5 |
| Grave | 6 | 8, 9, 21, 22, 24, 25 |

**Cero solapamiento entre las tres categorías.** No hay un solo "Leve" con un día perdido, ni un
"Moderado" con seis. Un corte tan limpio no ocurre cuando dos personas clasifican un hecho a
criterio: ocurre cuando la etiqueta **se deriva** del número.

Esto no es un defecto del dato, pero cambia lo que se puede hacer con él: **"predecir la severidad"
y "predecir los días perdidos" son el mismo problema con distinto nombre.** Un modelo de severidad
no aportaría una dimensión nueva del riesgo — estaría prediciendo un renombre de su propia
variable objetivo.

### V2 — La concentración de gravedad en el turno noche **no se distingue del azar**

Es un ajuste al bloque A del guion ejecutivo, y ya está aplicado ahí.

| Comparación | Noche | Resto | Test |
|---|---:|---:|---|
| Casos graves | 5 | 1 | Fisher exacto bilateral, **p = 0,205** |
| Incidentes con días perdidos | 10 | 5 | Fisher, **p = 0,352** |
| Incidentes leves | **15** | **15** | Idénticos |

El "5 de 6 casos graves ocurrió de noche" es un **conteo real y se puede decir**. Afirmar que *la
gravedad se concentra en la noche* es una generalización, y con seis casos no se sostiene.

**Lo que sí aguanta es el hallazgo principal:** la tasa de incidentes, 5,4x, calculada sobre 45
casos con exposición comparable. Los días perdidos son el **impacto observado** de ese hallazgo, no
un segundo hallazgo con entidad propia.

---

## I4 — El turno noche concentra 5,4x la tasa de incidentes

> **Insight.** 11,8 incidentes cada 1.000 empleado-mes contra 2,2 de mañana y tarde, con exposición
> comparable (2.124 vs 2.254 y 2.256 empleado-mes). 25 de 45 incidentes y 102 de 138 días perdidos.

### 1. Tipo de proyecto posible

Hay dos candidatos, y conviene evaluarlos por separado porque fallan por motivos distintos.

**Candidato A — `supervisado`:** un modelo de riesgo de accidente por empleado-mes.

| Elemento | Definición |
|---|---|
| **Variable objetivo** | `incidente de seguridad en los próximos 3 meses` — binaria, por empleado-mes |
| **Anticipación necesaria** | 1 a 3 meses. Menos no deja margen para cambiar dotación, tarea o cobertura |
| **Unidad de análisis** | Empleado-mes del panel activo |

**Candidato B — `no supervisado`:** agrupar condiciones de trabajo para descubrir perfiles de
riesgo sin usar la etiqueta de incidente.

| Elemento | Definición |
|---|---|
| **Patrón buscado** | Combinaciones de turno, área, tarea, dotación y estado de equipo que se repiten en las condiciones donde ocurren los hechos |
| **Decisión que habilitaría** | Priorizar qué configuraciones auditar primero |

### 2. Datos faltantes

| Brecha | Por qué bloquea |
|---|---|
| **N5 — ficha de investigación con causa raíz** | 30 de 45 incidentes no tienen ninguna acción correctiva; los 15 restantes repiten la misma frase. **No existe campo de causa raíz.** Sin esto no hay ninguna variable explicativa del hecho |
| **Hora real del hecho** | `turno_evento` es el turno asignado a la persona, no el del accidente, y `hora_evento` lo contradice (6 a 22 h) |
| **Variables del evento, no de la persona** | El dataset describe bien al **empleado** —antigüedad, horas extra, área, turno— y casi nada del **hecho**: qué máquina, qué tarea, qué condición del entorno. Para modelar un evento hacen falta variables del evento |

Esa última fila es el problema de fondo del candidato B, y es fácil de pasar por alto: no se pueden
agrupar condiciones de trabajo si las condiciones de trabajo no están registradas.

### 3. Veredicto explícito

**`ninguno — sigue siendo Discovery recurrente`.**

| Condición | Qué muestra el caso |
|---|---|
| **Frecuencia** | **No cumple.** La decisión real es "¿auditamos el turno noche?", y se toma una vez. Las decisiones diarias de seguridad —parar una línea, revisar un equipo— son operativas y las toma un supervisor mirando, no scoreando |
| **Escala** | **No cumple.** 675 personas en el universo, ~125 en el turno noche. Un jefe de turno recorre esa línea en una noche |
| **Cuello de botella** | **Es calidad de inferencia, y ni siquiera está en condiciones de serlo.** No se sabe por qué pasan los accidentes, y no se sabe porque **nadie registra la causa**. El problema no es que falte un modelo: falta el dato de entrada |

**Y el tamaño del fenómeno cierra la discusión:**

| Cantidad | Valor |
|---|---:|
| Empleado-mes en el panel activo | 9.601 |
| Incidentes auditables | **45** |
| **Tasa base de la clase positiva** | **0,47%** |
| Personas distintas accidentadas | 41 de 675 (**6,1%**) |
| **Personas con más de un incidente** | **3** |

Esa última fila es la que decide. **Con 41 personas accidentadas y solo 3 reincidentes, no hay
señal individual persistente que aprender.** Un modelo por persona no tiene a qué agarrarse: el
accidente no le "pertenece" a un perfil de empleado, le pertenece a una situación.

#### El argumento que hay que anticipar: "balanceá las clases"

Es la objeción previsible, y por eso vale contestarla de frente. Con 45 positivos en 9.601
observaciones, alguien va a proponer sobremuestrear la clase minoritaria.

**No arregla nada, y empeora una cosa.** Balancear no crea información: reparte de otro modo la que
ya hay. Interpolar entre 45 casos —muchos de ellos leves, sin días perdidos, en 41 personas
distintas— fabrica ejemplos sintéticos que no corresponden a ningún accidente que haya ocurrido.
El modelo sale más confiado, no más correcto. Es el mismo error que la pseudorreplicación de la
tabla persona-mes: confianza que no se ganó.

#### Y una razón que no es estadística

Aunque el modelo funcionara, **la acción correctiva no es individual.** Lo que este análisis
recomienda —revisar dotación, supervisión, tareas, mantenimiento y relevo del turno noche— se
ejecuta sobre el turno, no sobre personas. Un score de riesgo por empleado no cambiaría ni una de
esas seis decisiones.

Peor: señalaría trabajadores individuales por un riesgo que es de condiciones. Poner un número de
"probabilidad de accidentarse" al lado del nombre de un operario, cuando lo que falla es la
configuración del turno, desplaza la responsabilidad exactamente en la dirección equivocada. Es una
razón suficiente por sí sola para no hacerlo, incluso si los datos alcanzaran.

#### El umbral — qué cambiaría el veredicto

1. **Que exista N5 en régimen**, con causa raíz y condiciones del hecho registradas, durante al
   menos dos años. Sin variables del evento no hay modelo posible, con cualquier volumen.
2. **Que el volumen crezca en dos órdenes de magnitud**: miles de eventos, no decenas. Eso implica
   una operación mucho más grande, o consolidar datos de varias plantas.
3. **Que la decisión se vuelva individual y frecuente** — por ejemplo, asignar diariamente tareas
   de riesgo entre cientos de personas con restricciones que un planificador no puede resolver a
   mano. Hoy no es el caso.

Las tres, no una.

### 4. Mapa ds-*

> **No pasar a ds-06 todavía; sostener como análisis recurrente de Discovery y mejorar la captura
> de datos.**

Prioridad de captura: **N5** (causa raíz + hora real del hecho) y variables del evento. Es la
brecha número uno de todo el proyecto, porque bloquea la recomendación principal.

---

## I6 — Seis casos graves explican 109 de los 138 días perdidos

> **Insight.** El daño está concentrado en poquísimos casos: los 6 graves suman 109 días, los 9
> moderados 29, y los **30 leves suman cero**.

### 1. Tipo de proyecto posible

**El candidato es `supervisado`:** predecir la severidad de un incidente, o directamente los días
perdidos, para priorizar prevención donde duele.

| Elemento | Definición |
|---|---|
| **Variable objetivo** | `días perdidos` (regresión) o `incidente con días perdidos` (binaria) |
| **Anticipación necesaria** | No aplica en el sentido habitual: no se predice antes del hecho, se predice la consecuencia del hecho |

**Y acá aparece el problema antes que cualquier consideración de tamaño.** Por V1, `severidad` es
una recodificación de `dias_perdidos`: Leve = 0 días, Moderado = 1–5, Grave = 8–25, sin un solo
caso que cruce. Predecir severidad **es** predecir días perdidos. No son dos variables, es una.

Un modelo entrenado para clasificar severidad usando días perdidos como variable de entrada tendría
una exactitud perfecta y no diría absolutamente nada. Es fuga de la variable objetivo en su forma
más pura, y es fácil de cometer sin darse cuenta, porque las dos columnas existen por separado en
el archivo y tienen nombres distintos.

### 2. Datos faltantes

| Brecha | Por qué bloquea |
|---|---|
| **N5 — causa raíz y condiciones del hecho** | Es la misma brecha de I4, y acá pesa todavía más. Para predecir la consecuencia de un accidente hacen falta las características **del accidente**: qué energía estaba involucrada, qué protección falló, qué tarea se estaba haciendo. El dataset tiene la parte del cuerpo afectada y el subtipo, y poco más |
| Volumen de eventos con consecuencia | Solo **15 de 45** incidentes tienen algún día perdido. Los otros 30 son ceros |

### 3. Veredicto explícito

**`ninguno — sigue siendo Discovery recurrente`.**

| Condición | Qué muestra el caso |
|---|---|
| **Frecuencia** | **No cumple.** Ocurren ~2,8 incidentes por mes en toda la empresa, con un máximo de 6 en el peor mes. No hay ningún flujo que scorear |
| **Escala** | **No cumple, por mucho.** La clase que importa son **6 casos**. Y la clase "con alguna consecuencia", 15 |
| **Cuello de botella** | **Ni scoring ni inferencia: es registro.** Faltan las variables del hecho. Y la etiqueta que se querría predecir es una recodificación del resultado |

**Lo que sí corresponde hacer, y es más útil:** usar la concentración como criterio de priorización,
que es una decisión de gestión y no necesita ningún modelo. Los 30 incidentes leves suman **cero**
días perdidos; bajar el conteo total de incidentes y bajar los días perdidos **son objetivos
distintos**, y hoy la empresa no los distingue. Eso solo ya cambia dónde se pone el esfuerzo.

#### El umbral — qué cambiaría el veredicto

Este es el más lejano de todos los evaluados. Haría falta:

1. **N5 en régimen**, con variables del hecho —no del empleado— registradas de forma estructurada.
2. **Cientos de eventos con consecuencia**, no quince. Con la tasa actual de la empresa, eso son
   décadas; en la práctica implica datos sectoriales o multiplanta.
3. Que la severidad se registre **de forma independiente** de los días perdidos, o que se abandone
   como objetivo y se modele directamente la consecuencia.

Mientras tanto, el criterio de priorización por concentración se sostiene solo con aritmética.

### 4. Mapa ds-*

> **No pasar a ds-06 todavía; sostener como análisis recurrente de Discovery y mejorar la captura
> de datos.**

Prioridad de captura: **N5**, con foco explícito en variables del evento. Y una recomendación de
registro que no cuesta nada: **dejar de derivar `severidad` de `dias_perdidos`**, o documentar
explícitamente que es una recodificación, para que nadie la use más adelante como si fuera una
observación independiente.

---

## Cierre de la entrega 7

Los cuatro insights evaluados hasta acá —los dos de rotación y los dos de seguridad— son los cuatro
candidatos "obvios" a modelo del proyecto. Los cuatro dan **ninguno**, y el patrón de por qué ya se
puede ver:

| Insight | Falla en |
|---|---|
| **I2** — rotación en un área | Escala (89 positivos en toda la empresa, 11 en el área) y cuello de botella (falta saber *por qué*) |
| **I10** — costo de la rotación | No es inferencia: faltan **dos mediciones** que nadie tomó |
| **I4** — seguridad nocturna | Escala (45 eventos, 3 reincidentes), falta de variables del hecho, y la acción correctiva **no es individual** |
| **I6** — concentración de la gravedad | Seis casos, y una etiqueta que es una **recodificación del resultado** |

Ninguno falla por falta de técnica. Tres fallan porque el fenómeno ocurrió pocas veces, y todos
fallan porque **falta el dato que explicaría el fenómeno**, no el algoritmo que lo predeciría.

Esa es la conclusión que vale llevar a la sala: el próximo paso de TechnoStamp no es un modelo, es
un formulario de carga de incidentes que pida la causa, y una entrevista de salida que pida el
motivo. Los dos son controles de proceso. Ninguno de los dos es analítica.

---

**Siguiente:** entrega 8 — **I12** (señal de fuga temprana) e **I8** (eficacia preventiva de
capacitación). Los dos casos donde el dato existe pero todavía no se sabe qué significa.

---

# Entrega 8 · I12 e I8 — cuando el dato existe pero no se sabe qué significa

Las cuatro entregas anteriores trataron insights que fallaban por **escala** o por **falta de
dato**. Estos dos son otra categoría: **el dato está, y es la interpretación la que falta**.

Y en los dos casos, al ir a verificar la interpretación con los archivos que ya existen, la
respuesta apareció. Ninguno de los dos necesitaba un dato nuevo: necesitaba que alguien corriera el
cruce.

Esta entrega, entonces, no solo emite veredictos. **Cierra dos brechas del backlog** y obliga a
corregir lo que se había escrito sobre ambos insights.

---

## I12 — La "señal de fuga temprana" es un artefacto de registro

> **Insight, tal como estaba enunciado.** Quien renuncia había recibido un aumento hace 1,0 mes;
> quien se queda, hace 4,5. Era la señal más discriminante de todo el dataset, y era
> contraintuitiva. La brecha **N6** proponía auditar cómo se escribe el campo antes de usarlo.

### La verificación que resuelve N6 sin salir de los datos

`meses_desde_ultimo_aumento`, abierto por motivo de salida:

| Grupo | n | Media | Mediana | Mín | **Máx** |
|---|---:|---:|---:|---:|---:|
| Renuncia voluntaria | 89 | 1,03 | 1,0 | 0 | **3** |
| Despido | 27 | 0,96 | 1,0 | 0 | **3** |
| Jubilación | 7 | 1,43 | 1,0 | 0 | **3** |
| Reestructuración | 5 | 1,40 | 1,0 | 0 | **3** |
| Fin de contrato | 4 | 0,50 | 0,5 | 0 | **1** |
| **Activos** | **562** | **4,53** | **2,0** | 0 | **17** |

Y el número que cierra la discusión:

| | |
|---|---:|
| Salidas con valor mayor a 3 | **0 de 132** |
| Activos con valor mayor a 3 | **183 de 562** |

**Ninguna baja, de ningún motivo, supera el valor 3. Un tercio de los activos sí.**

### Por qué esto no es una señal

Si el aumento reciente fuera un predictor de renuncia —la hipótesis de la contraoferta fallida, o
de la frustración salarial— el patrón tendría que ser **específico de las renuncias voluntarias**.

No lo es. Los despedidos tienen media 0,96. Los jubilados, 1,43. Los de fin de contrato, 0,50. Los
cinco motivos comparten el mismo perfil, y los cinco están capados en 3.

El caso de las jubilaciones es la prueba directa: **nadie se jubila porque le dieron un aumento
hace un mes.** Y sin embargo los siete jubilados del período tienen valores de 0, 0, 1, 1, 2, 3 y 3
—incluido uno de 60 años con 4,3 años de antigüedad—. La jubilación es una decisión que se planifica
con años; que ese grupo muestre exactamente el mismo "indicador de fuga" que los renunciantes
demuestra que el campo no está midiendo nada sobre la decisión de irse.

**Qué está pasando, entonces.** El campo se reescribe o se trunca en el momento de registrar la
baja, para todas las bajas por igual. En los activos el contador corre libre hasta 17 —que es
exactamente el largo del panel—; en las salidas nunca pasa de 3. Eso es la firma de un artefacto de
registro, no de un comportamiento humano.

### 1. Tipo de proyecto posible

**`ninguno`**, y por una razón anterior a cualquier consideración de escala: **la variable no
significa lo que su nombre dice**. No hay proyecto de ningún tipo —supervisado, no supervisado o
descriptivo— que se construya sobre un campo cuyo contenido depende del acto administrativo de dar
de baja y no del fenómeno que se quiere estudiar.

### 2. Datos faltantes

**N6 queda resuelta desde el lado analítico.** Ya no hace falta preguntarse *si* el patrón es un
artefacto: los datos lo muestran. Lo que sigue abierto es de otra naturaleza:

| Qué queda | Naturaleza |
|---|---|
| Por qué el sistema reescribe el campo al registrar una baja | Auditoría de **proceso**, para arreglar el sistema origen. Ya no bloquea ningún análisis |
| Un registro histórico real de aumentos, con fecha | **Dato nuevo.** Es lo que permitiría estudiar de verdad la relación entre compensación y renuncia |

### 3. Veredicto explícito

**`ninguno — sigue siendo Discovery recurrente`**, y con una advertencia que vale más que el
veredicto:

> **`meses_desde_ultimo_aumento` no debe usarse como variable en ningún análisis de rotación,
> ni entrar como feature en ningún modelo futuro.**

Es exactamente el tipo de variable que un modelo encontraría "muy predictiva" —separa salidas de
activos casi perfectamente— y que estaría prediciendo el **acto de registrar la baja**, no la
decisión de irse. Fuga de la variable objetivo, disfrazada de hallazgo de negocio.

Vale detenerse un segundo acá, porque es la lección más transferible de todo el documento: **una
variable que separa demasiado bien suele estar contaminada por el desenlace.** Cuando un campo
discrimina así de limpio, la primera pregunta no es "qué buen predictor", es "¿cuándo se escribe
este dato?".

#### El umbral — qué cambiaría el veredicto

Que exista un **registro histórico de aumentos con fecha propia**, independiente del estado del
empleado. Con eso la pregunta original —¿la gente se va después de un aumento que no alcanzó?—
vuelve a ser investigable, y sería un análisis de Discovery legítimo. Seguiría sin justificar un
modelo, por las mismas razones de escala de I2.

### 4. Mapa ds-*

> **No pasar a ds-06 todavía; sostener como análisis recurrente de Discovery y mejorar la captura
> de datos.**

Y agregar el campo a una lista de variables prohibidas para cualquier trabajo futuro de rotación.

---

## I8 — La capacitación en seguridad no llega a quien se accidenta, ni antes ni después

> **Insight, tal como estaba enunciado.** Nadie mide si la capacitación en seguridad previene algo.
> La correlación área a área es r = 0,394 con p = 0,260, y el código del proyecto **no compara
> fechas**. G12 afirmaba "se entrena después del accidente, no antes" sin ningún cálculo detrás.

### El cruce temporal que nunca se había corrido

Se podía hacer con lo que ya existe: `capacitaciones_limpio.parquet` tiene `fecha_inicio` y
`fecha_fin` (145 capacitaciones de Seguridad, 133 empleados distintos, enero 2024 – mayo 2025), y
`eventos_limpio.parquet` tiene `fecha_evento`. Corrido sobre los 45 incidentes:

| De los 45 incidentes | n | % |
|---|---:|---:|
| Con capacitación de seguridad **previa** al hecho | 5 | 11% |
| Con capacitación de seguridad **posterior** al hecho | 4 | 9% |
| **Sin ninguna capacitación de seguridad, en ninguna dirección** | **36** | **80%** |

**El titular de G12 está contradicho por los datos.** "Se entrena después del accidente" describe a
**4 casos de 45**. Y esos cuatro recibieron su capacitación a una mediana de **108 días** del hecho,
con un máximo de **344 días**: eso no es una reacción al accidente, es el calendario normal de
capacitación que en algún momento los alcanzó.

### Y el hallazgo real, que es mejor que el que se creía

A nivel persona, comparando cobertura de capacitación entre quienes se accidentaron y quienes no:

| Grupo | n | Con capacitación de seguridad |
|---|---:|---:|
| Accidentados | 41 | 9 (**22,0%**) |
| No accidentados | 634 | 121 (**19,1%**) |
| **Universo completo** | **675** | **130 (19,3%)** |

Fisher exacto bilateral: **p = 0,683. No se distingue.**

Los accidentados tienen capacitación de seguridad **exactamente en la proporción de la empresa**.
No más, no menos, ni antes ni después. Sumado a la correlación por área (r = 0,394, p = 0,260), son
tres mediciones independientes que apuntan a lo mismo.

**El hallazgo, entonces, no es "no lo medimos": es que la capacitación de seguridad cubre al 19,3%
de la gente y se asigna sin ninguna relación con quién se lastima.** Eso es más fuerte, más
accionable y más incómodo que la brecha de medición que decía el enunciado anterior.

### 1. Tipo de proyecto posible

**El candidato sería `supervisado`:** predecir quién necesita capacitación de seguridad, o estimar
el efecto de la capacitación sobre el riesgo de incidente.

| Elemento | Definición |
|---|---|
| **Variable objetivo** | `incidente en los N meses posteriores a la capacitación`, por empleado |
| **Anticipación necesaria** | La de la planificación del calendario de capacitación: un trimestre |

### 2. Datos faltantes

| Brecha | Por qué bloquea |
|---|---|
| **N5 — causa raíz** | Sin saber qué falló en cada accidente, no se puede saber qué capacitación lo habría prevenido. Un curso genérico de "refuerzo de seguridad" no tiene contra qué evaluarse |
| Criterio de asignación de la capacitación | No está registrado por qué a una persona le tocó un curso y a otra no. Sin eso, cualquier comparación entre capacitados y no capacitados confunde el efecto del curso con el criterio de quien lo asignó |

Esa segunda fila es el problema serio, y no es de volumen: es de **diseño**. Comparar la tasa de
incidentes de capacitados contra no capacitados no mide el efecto de la capacitación si la
asignación no fue aleatoria ni siquiera documentada.

### 3. Veredicto explícito

**`ninguno — sigue siendo Discovery recurrente`.**

| Condición | Qué muestra el caso |
|---|---|
| **Frecuencia** | **No cumple.** El calendario de capacitación se arma por trimestre o por año |
| **Escala** | **No cumple.** 145 capacitaciones de seguridad y 45 incidentes en 17 meses. Una planilla lo cubre |
| **Cuello de botella** | **Es diseño de la medición, no scoring.** La pregunta —¿la capacitación previene?— no se contesta con un modelo predictivo sobre datos observacionales donde la asignación es desconocida |

**Y lo que corresponde hacer es barato y no es analítica.** Con la cobertura al 19,3% y sin relación
con el riesgo, el primer paso es de gestión pura: **cubrir con capacitación de seguridad al turno
noche y a las áreas de producción**, que es donde están los incidentes, y registrar el criterio de
asignación. Recién con eso registrado durante un par de años se podría evaluar el efecto —y aun así
sería una evaluación, no un modelo predictivo.

#### El umbral — qué cambiaría el veredicto

1. **Asignación registrada**, y preferentemente escalonada en el tiempo por algún criterio
   explícito. Eso convierte el despliegue del programa en algo evaluable.
2. **N5 en régimen**, para saber qué falló en cada caso y si el contenido del curso lo cubría.
3. Volumen de eventos en el orden de los cientos.

Con (1) y (2), lo que aparece no es un modelo predictivo: es una **evaluación de impacto**. Que es
una herramienta distinta y la correcta para esta pregunta.

### 4. Mapa ds-*

> **No pasar a ds-06 todavía; sostener como análisis recurrente de Discovery y mejorar la captura
> de datos.**

Prioridad: registrar el criterio de asignación de la capacitación, y **N5**.

---

## Correcciones que esta entrega obliga

Las dos verificaciones cambian lo que se había escrito. Ya están aplicadas.

| Documento | Qué decía | Qué dice ahora |
|---|---|---|
| `03_insights_nuevos.md` I12 | "Señal de fuga temprana sin validar; puede ser contraoferta fallida o artefacto" | **Artefacto de registro confirmado.** Ninguna de las 132 bajas supera el valor 3; los jubilados muestran el mismo perfil que los renunciantes |
| `03_insights_nuevos.md` I8 | "Nadie mide si la capacitación previene algo" | El cruce temporal **sí se corrió**: 80% de los accidentados nunca tuvo capacitación de seguridad, y la cobertura no se distingue del resto de la empresa (p = 0,683) |
| `03_insights_nuevos.md` §3 | N6 en prioridad 3 | **N6 resuelta analíticamente.** Lo que queda es auditoría de proceso del sistema origen, y ya no bloquea ningún análisis |
| `02_guion_ejecutivo.md` §C.3 | G12: "no sabemos si la capacitación previene, porque nadie lo mide" | Se agrega el resultado del cruce temporal, que es un hallazgo más fuerte y accionable |
| `01_matriz_evidencia.md` fila 5 | — | Se incorporan las tres mediciones independientes |
| `04_puente...` entrega 6, I2 | N6 descrita como "la señal más discriminante que hoy se ve en los datos" | Corregido: es un artefacto, y el campo queda **prohibido** como variable de rotación |

---

## Cierre de la entrega 8

Seis insights evaluados, seis veces **ninguno**. Pero estos dos aportan algo que los cuatro
anteriores no:

**Ninguno de los dos necesitaba un dato nuevo.** Necesitaba que alguien corriera el cruce. N6 se
resolvió abriendo el campo por motivo de salida; la temporalidad de G12 se resolvió con dos
archivos que ya estaban en el proyecto y tienen fecha.

Es una advertencia sobre el propio backlog: **antes de pedirle un dato al cliente, conviene agotar
lo que ya está en la mesa.** Dos de las seis brechas que este proyecto iba a solicitar no eran
brechas de dato — eran análisis pendientes.

Y dejan una regla que se lleva a cualquier proyecto: **cuando una variable separa demasiado bien,
la primera pregunta es cuándo se escribe ese dato, no qué buen predictor es.**

---

**Siguiente:** entrega 9 — **I3**, **I11**, **I5**, **I7**, **I9** e **I1**. Los que son
decisiones de gestión o arreglos de captura. Cierre del documento.


