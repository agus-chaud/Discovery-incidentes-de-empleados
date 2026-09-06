# TechnoStamp explicado 

Aca se explica el por que de cada elección,  para que lo puedas defender en una entrevista sin abrir el código.

## 1. La primera decisión fue no construir un modelo

Te dan tres CSV crudos y una lista de preocupaciones de una gerenta de RRHH. 
Un modelo se justifica cuando la decisión que alimenta pasa muchas veces, rápido, y a una escala que una persona no puede revisar caso por caso: scorear millones de transacciones por fraude, decidir en milisegundos si mostrar un anuncio. Acá las decisiones son otra cosa — "¿invertimos en retención?", "¿Mantenimiento Eléctrico realmente está peor que el resto?" — decisiones que un directorio toma un par de veces al año, donde el cuello de botella no es la velocidad de scorear . Eso es inferencia: estimar con incertidumbre , darle al negocio la respuesta que necesitaba de por qué una sola área pierde el doble de gente que el resto.

**Practicá esto (respondé antes de destapar):** ¿por qué este proyecto no construyó ningún modelo, si había datos de sobra para intentarlo?

## 2. Una fila no es una persona

`empleados_mensual.csv` tiene una fila por persona, por mes: 9.733 filas para 694 personas a lo largo de 17 meses. Si le corrés un `.groupby("genero").mean()` a esa tabla tal cual viene, no estás promediando sobre 694 personas — estás promediando sobre 9.733 observaciones persona-mes, y alguien que se quedó los 17 meses pesa 17 veces más que alguien que se fue en el segundo mes. Eso infla en silencio a quien se queda y le resta peso a quien se va, justo cuando la pregunta es sobre quién se va.

La solución fue crear  una segunda tabla, una fila por persona (su último estado conocido más los agregados de toda su historia), para cualquier cosa que sea sobre personas (cuántas se fueron, la brecha salarial, la rotación por área).

Esta nueva tabla tambien era necesaria por un tema de error estandar. si se calcula la brecha salarial de género sobre la tabla original, cada persona aportaba hasta 17 observaciones de salario casi idénticas entre sí (su sueldo no cambia mucho mes a mes). Un test estadístico que no sepa que esas 17 filas vienen de la misma persona las trata como 17 datos independientes, y eso reduce artificialmente el error estándar. El test se volvería más confiado de lo que debería, sin que nadie haya mentido con ningún número. Esto tiene nombre, pseudorreplicación, y es uno de esos errores que no rompen nada a simple vista pero inflan la confianza de una conclusión que no la merece. Trabajar sobre la tabla de una fila por persona lo evita .  Antes de promediar sobre cualquier tabla, siempre preguntate si cada fila es independiente entre sí o si varias filas pueden venir de la misma entidad.

## 3. Que un dato falte no siempre significa lo mismo

El manual estándar dice que hay tres formas en que un dato puede faltar. MCAR: falta al azar puro, no depende de nada. MAR: falta, pero el motivo está explicado por otra columna que sí tenés. MNAR: falta por culpa del propio valor que falta — por ejemplo, la gente con sueldos muy altos que no contesta la pregunta del sueldo en una encuesta.

Ninguna de las tres explica bien el patrón de faltantes más grande de este proyecto. `tasa_scrap_porcentaje` no le "falta" a alguien de RRHH por azar, ni porque otra columna lo prediga: le falta porque el desperdicio de producción no es un concepto que aplique a un analista de RRHH. No es un dato perdido. Es un dato que no existe para ese grupo , y conviene tenerlo como una cuarta categoría en la cabeza, porque el arreglo es distinto: no se imputa. 
El arreglo correcto es definir bien el universo: promediar el desperdicio solo dentro de donde existe (las tres áreas de producción, 60,9% de las filas) y decirlo explícitamente. El propio patrón de vacíos es el diagnóstico: 0,1% vacío adentro de producción contra 99,7% u 50,8% afuera. Si fuera azar puro, no se concentraría así.

## 4. Un valor raro no siempre es un error

Las tres herramientas típicas para detectar outliers  (el rango intercuartílico, el z-score, los percentiles extremos) hacen lo mismo en el fondo: marcan qué está lejos del centro. Ninguna sabe por qué está lejos, ni si está mal. Eso necesita contexto de negocio.

La regla del rango intercuartílico marcó 1.388 filas de sueldo (14,3%) como atípicas. El instinto de junior es recortarlas o aplicarles winsorización porque están distorsionando el promedio. Antes de tocar nada, conviene revisar si ese patrón raro ya tiene una explicación conocida. Ordenando el sueldo medio por nivel jerárquico sale esto: $1.543.376, $2.215.424, $3.163.732, $5.333.018, $8.199.502 — sube en línea recta en los cinco niveles, sin ninguna excepción. Eso no es ruido. Es el organigrama. Recortarlo habría aplastado justo la estructura que la regresión de brecha salarial necesita para controlar por nivel — se rompería el análisis para arreglar un problema que no existía. 


## 5. Cuando dos fuentes cuentan historias distintas

 Los accidentes de trabajo estaban registrados en dos tablas que no coincidían. El enfoque fácil es confiar en la que tiene más casos, o en la que es más cómoda de cruzar; pero lo correcto es medir cuál puede explicar cómo se midió.

La columna `incidentes_seguridad_count` del panel mensual sumaba 100 incidentes en el período. La tabla `eventos_rrhh` , con causa, parte del cuerpo y acción correctiva  sumaba 45 incidentes. El número del panel es el doble, pero no puede justificarse a sí mismo: no trae causa ni contexto. Esa es la señal de alarma. Usando el número del panel, los datos parecían decir que los ingresantes (primeros 6 meses) se accidentan a 10 veces el promedio — algo dramático. Usando el registro auditable: cero incidentes en los primeros 12 meses; la antigüedad más baja entre cualquier accidentado es 13 meses. Conclusión opuesta. Usé la fuente auditable porque es la única que puedo ir a verificar. 

## 6. Un porcentaje solo es casi una opinión

Un porcentaje describe lo que pasó, una vez, en ese grupo exacto. No dice nada sobre si se repetiría el año que viene. El intervalo de confianza es el correcto a usar, porque es un rango que contendría la tasa real la mayoría de las veces si repitieras la medición.

Mantenimiento Eléctrico mostraba 34,8% de rotación sobre 46 personas. El intervalo de Wilson sobre eso (se usa en vez de la fórmula normal de toda la vida porque esa fórmula se rompe justo con n chico o cerca de 0%/100%, llegando a dar intervalos por debajo de cero o por arriba de cien) da 22,7% a 49,2%. Es ancho, pero todo el rango sigue arriba del promedio de la empresa (16,7%). Comparalo con Estampado: su 20,0% también parecía peor que el promedio, pero su intervalo va de 14,9% a 26,3%, que sí incluye al 16,7%. Con estos datos no se puede distinguir a Estampado de lo normal. Mismo tipo de test, respuesta distinta, porque el tamaño de grupo es distinto — 46 personas contra 185. Los grupos chicos necesitan una diferencia mucho más grande antes de que se les pueda creer. 


## 7. Lo que se quedó sin resolver

**No hubo corrección por comparaciones múltiples.** Testear algo a un umbral del 5% significa aceptar un 5% de probabilidad de una falsa alarma en ESE test, por puro azar, incluso si no está pasando nada real. Testear diez cosas hace que ese "5% de chance de una falsa alarma" se acumule — la probabilidad de que al menos una de las diez parezca "significativa" sin ningún motivo real ronda el 40%. El proyecto testeó diez áreas contra el promedio de rotación de la empresa. Volvió exactamente una significativa (Mantenimiento Eléctrico), con un margen grande y cómodo (z=3,28), probablemente real. Pero "probablemente" está haciendo trabajo en esa frase, y el análisis nunca corrió la corrección (por ejemplo, Bonferroni) que permitiría decirlo con la misma confianza que si se hubiera testeado una sola área desde el principio.

**La censura por la derecha no se trató.** Alguien marcado como activo hoy no es "alguien que se queda para siempre" — es "alguien cuyo final todavía no viste". Cada estadística de rotación de este informe subestima, técnicamente, a la gente que se va a ir eventualmente pero todavía no lo hizo. Esto se llama censura por la derecha, y es la razón entera por la que el análisis de supervivencia (curvas de Kaplan-Meier, modelos de Cox) existe como campo aparte en vez de que todo el mundo calcule porcentajes. Es poco probable que cambie alguna conclusión acá — 16 meses no alcanzan para que pese mucho — pero un Decision Scientist tiene que poder decir, sin que se lo pregunten, "este número subestima técnicamente el riesgo real de fuga por censura". La regla que conecta los dos huecos: nombrar una debilidad de tu propio análisis antes de que te la señalen vale más, en una entrevista, que no tener ninguna debilidad que nombrar.


## 8. En plata: nunca prometas un número, prometé un rango

Cuando armás una estimación de costo, algunos ingredientes son cosas que contaste y otros son cosas que supusiste. 

El costo por salida de este proyecto dio $5,88M. De eso, solo $200.000 — reclutamiento más onboarding — salen de algo que la empresa realmente mide. El otro 97% (cuánto sueldo se pierde mientras el puesto está vacío, cuántos meses necesita un ingresante para rendir como quien reemplazó) es un juicio de valor. Mover ese juicio de valor dentro de un rango razonable hace que el ahorro anual estimado vaya de $23M a $195M — una amplitud de 8 veces.Se debe publicar el rango, mostrar qué ingredientes son medidos y cuáles son supuestos, y nombrar los dos datos concretos que la empresa podría aportar para achicar ese rango a algo defendible.

## Mapa rápido: concepto → pregunta de entrevista

| Concepto | Dónde apareció | Te pueden preguntar |
|---|---|---|
| Inferencia vs predicción | Por qué no hay ningún modelo en todo el proyecto | "¿Por qué no armaron un modelo de churn si tenían los datos?" |
| Unidad de análisis y granularidad | Panel mensual vs tabla de una fila por persona | "¿Por qué armaron una tabla aparte en vez de trabajar sobre el panel directo?" |
| Ausencia estructural (missingness) | El desperdicio de producción vacío fuera de tres áreas | "¿Por qué no imputaron el scrap para el resto de la empresa?" |
| Outliers con estructura | Los sueldos altos siguiendo el organigrama | "¿Por qué no recortaron los sueldos atípicos si distorsionan el promedio?" |
| Fuente auditable vs volumen | `eventos_rrhh` elegida sobre la columna del panel | "¿Cómo decidieron qué tabla de incidentes usar?" |
| Intervalos de confianza | Mantenimiento Eléctrico vs Estampado | "¿Por qué un área sí y la otra no, si las dos tienen más rotación que el promedio?" |
| Comparaciones múltiples | Diez áreas testeadas sin corrección | "¿Corrigieron por múltiples comparaciones?" |
| Censura | Activos marcados como si se quedaran para siempre | "¿Ese 15% de rotación es la tasa real, o le falta algo?" |
| Rango vs punto único | El business case entre $23M y $195M | "¿Por qué no me dan un solo número de ahorro esperado?" |

Para el detalle completo de cada decisión, con las cifras exactas y las alternativas descartadas, `decisions.md` es la fuente. Este archivo es para tenerlo en la cabeza antes de entrar a la sala.

## 9. Un gr?fico no es un insight: la unidad de una presentaci?n ejecutiva es una decisi?n

Un directorio no necesita recorrer todas las columnas ni aprender la metodolog?a antes de entender qu? est? en juego. Necesita poder responder cuatro preguntas: **qu? est? pasando, cu?nto afecta al negocio, qu? dato lo sostiene y qu? conviene corregir**. Si una slide no responde esas cuatro cosas, probablemente es exploraci?n, no comunicaci?n ejecutiva.

Por eso la s?ntesis de TechnoStamp no se ordena por archivos ni por m?tricas de RR.HH.; se ordena por riesgos que cambian una conversaci?n de negocio. Mantenimiento El?ctrico merece prioridad porque su 34,8% de rotaci?n es la ?nica diferencia por ?rea que se sostiene frente al promedio. El turno noche merece una intervenci?n de seguridad porque concentra 25 de los 45 incidentes auditables y los casos graves explican 109 de 138 d?as perdidos. La sucesi?n debe hacerse visible porque existe un puesto de Supervisor de Log?stica ocupado por una sola persona que se jubila en seis meses.

La palabra importante es **focalizado**. No hay evidencia para decir ?toda la empresa rota mal?, ?las horas extra causan accidentes? o ?la capacitaci?n resolver? la seguridad?. Las horas extra s? son estructurales ?8,3% de la n?mina base y 61 personas con sobrecarga cr?nica?, pero eso sostiene una revisi?n de capacidad y cobertura, no un ahorro prometido. De la misma forma, el business case de retenci?n es una oportunidad en rango, no un n?mero garantizado: depende en gran medida de supuestos de vacancia y rampa que el cliente todav?a no mide.

La forma correcta de presentar cada hallazgo es:

1. **Titular:** una conclusi?n que se pueda leer sin explicaci?n adicional.
2. **Impacto:** costo, continuidad, productividad o riesgo que convierte el dato en problema de negocio.
3. **Evidencia:** un gr?fico o tabla con pocos elementos, universo y per?odo visibles, y un ?nico dato destacado.
4. **Acci?n correctiva:** una intervenci?n concreta y proporcional al hallazgo; no un plan gen?rico ni una promesa de resultado.

Ejemplo: ?La rotaci?n requiere una intervenci?n focalizada en Mantenimiento El?ctrico? funciona porque no repite el n?mero como titular, explica qu? debe hacer el negocio y conserva el 34,8% junto con su intervalo de confianza como evidencia. ?Rotaci?n por ?rea? solo describe un gr?fico; obliga a la audiencia a hacer el trabajo de inferir la conclusi?n.

El resultado ejecutivo completo est? en `06_resultados/Discovery/conclusiones_ejecutivas_technostamp.md`. Ese documento propone los cuatro insights y conecta cada uno con los visuales de decisi?n G9, G10, G11, G13 y G14.


## 10. Lo que enseñó auditar el propio proyecto

Auditar un trabajo terminado enseña cosas distintas que hacerlo. Estas cinco son las que valen para defender el proyecto — o cualquier otro — en una sala.

**Un pipeline tiene contratos, y una migración los rompe en silencio.** La limpieza v2 renombró una columna. Un script escrito contra la v1 siguió pidiéndola por el nombre viejo y el notebook entero se corta en la etapa 11 de 16. Nadie escribió mal ese script: lo que cambió fue el contrato, y no había nada que lo verificara. Cuando reemplaces una etapa por una versión mejorada, el trabajo no termina en la etapa nueva: termina cuando revisaste quién consumía la vieja.

**La misma tasa admite varios denominadores, y todos son “correctos”.** Con 113 salidas salen tres tasas de rotación anual defendibles: 15,0% (anualizada sobre dotación activa promedio), 16,7% (acumulada del período) y 12,6% (la del período anualizada). Ninguna está mal calculada. El error no es de aritmética: es publicar dos sin decir cuál es cuál, y comparar contra ellas indistintamente. Antes de publicar cualquier tasa, escribí su denominador y su período al lado, una vez, y usá el mismo en toda comparación entre grupos.

**Corregir por comparaciones múltiples no siempre debilita un hallazgo: a veces lo blinda.** El proyecto declaró como debilidad no haber corrido Bonferroni sobre las diez áreas testeadas. Al correrlo, Mantenimiento Eléctrico sobrevive con holgura (p = 0,00104 contra un umbral de 0,005). La corrección que se evitaba por miedo a perder el hallazgo era la que lo volvía inatacable. Si un efecto es grande y el z es cómodo, correr la corrección es barato y convierte una afirmación con asterisco en una sin él.

**Un artefacto de linaje desactualizado es peor que no tener linaje.** El archivo que registra el origen de los datos apuntaba al script superado, con fecha anterior a los datos que decía describir. Su contenido no era falso; su procedencia sí. Sin linaje, un auditor pregunta. Con linaje contradictorio, deja de creerle al resto. Todo artefacto de trazabilidad se regenera cuando se regenera el dato, o se borra.

**La evidencia tiene que probar el titular que ilustra, y una tasa nunca es un conteo.** Un gráfico citado para sostener “el turno noche concentra el riesgo” mostraba área y severidad — no turno. Y lo mostraba en conteos absolutos, que es justo lo que el propio proyecto había decidido no hacer: Ensamble 14 contra Calidad 3 parece 4,7 veces peor, y normalizado por exposición la brecha real es del 26%. El gráfico dibujaba la conclusión que el análisis había descartado. Antes de mandar un visual a una slide, preguntate dos cosas: ¿muestra la variable de la que habla el título?, ¿y está normalizado por la exposición de cada grupo?

| Concepto | Dónde apareció | Te pueden preguntar |
|---|---|---|
| Contratos entre etapas de un pipeline | Una columna renombrada en la limpieza v2 corta el notebook | ¿Cómo garantizás que una mejora de una etapa no rompe las de abajo? |
| Denominador y unidad de exposición | Tres tasas de rotación anual defendibles | ¿Ese 15% de rotación sobre qué base está calculado? |
| Comparaciones múltiples | Bonferroni sobre diez áreas | ¿Por qué corriste la corrección si ya tenías el hallazgo? |
| Trazabilidad de procedencia | Linaje que apuntaba al script superado | ¿Cómo sé con qué código se generó este dataset? |
| La evidencia debe probar el titular | Gráfico de área citado para un hallazgo de turno | ¿Este gráfico prueba lo que dice el título? |

> **Nota de estado.** La sección 9 de este archivo tiene los acentos degradados por una escritura con codificación incorrecta (48 tokens con `?` literal). Está registrado como ítem 4 del backlog en `06_resultados/Discovery/auditoria_mejoras_technostamp/06_backlog_priorizado.md`. La auditoría completa está en `06_resultados/Discovery/auditoria_mejoras_technostamp.md`.
