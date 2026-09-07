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
| **N6 — auditoría de `meses_desde_ultimo_aumento`** | Es la señal más discriminante que hoy se ve en los datos (1,0 mes en renuncias vs 4,5 en activos, I12) y **no se sabe si significa lo que parece**. Entrenar sobre ella sin auditarla es construir sobre un artefacto de registro posible |
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

Prioridad de captura, en orden: **N3** (entrevistas de salida) y **N6** (auditoría del campo de
último aumento).

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
