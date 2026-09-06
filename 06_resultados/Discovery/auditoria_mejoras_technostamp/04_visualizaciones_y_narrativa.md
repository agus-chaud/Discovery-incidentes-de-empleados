# 04 · Visualizaciones y narrativa

**Auditoría integral TechnoStamp — subentregable 4 de 6**
**Criterio aplicado a cada gráfico:** ¿qué está pasando? · ¿cómo afecta al negocio? · ¿qué evidencia lo sostiene? · ¿qué acción concreta sugiere? Un visual que no responde las cuatro es exploración, no comunicación ejecutiva (`ESTUDIO` §9).

Se inspeccionaron los 14 PNG y el código que los produce.

---

## 1. El proyecto ya tiene dos familias de gráficos, y la evolución fue en la dirección correcta

| | **G1–G7** (`08_visualizaciones.py`) | **G8–G14** (`18_visualizaciones_decision.py`) |
|---|---|---|
| Paneles | 18 paneles en 7 imágenes (G4, G5, G6 son grillas 2×2) | **1 panel por imagen** |
| Títulos | **Conclusiones**: *"Turno NOCHE: 5,4x el riesgo de mañana/tarde"*, *"NO se sostiene: los márgenes de error se solapan"* | **Descriptivos**: *"Rotacion por area: diferencias con margen de error"* |
| Rol | Exploración | Decisión |

**Acá está la ironía central del proyecto:** los gráficos exploratorios (G1–G7) aplican el principio de `ESTUDIO` §9 —el título enuncia la conclusión, no la variable— y los gráficos de decisión (G8–G14) lo abandonaron. Los siete títulos de decisión, textual del código:

```
"Rotacion mensual: original versus periodo limpio"
"Rotacion por area: diferencias con margen de error"
"Distribucion de horas extra por area"
"Incidentes por area y severidad"
"Capacitacion en seguridad versus incidentes"
"Riesgo de sucesion por puesto"
"Business case por escenario y reduccion de rotacion"
```

Los siete describen el eje. Ninguno dice qué concluir. Es exactamente el ejemplo que el propio `ESTUDIO` §9 usa como contraejemplo: *"«Rotación por área» solo describe un gráfico; obliga a la audiencia a hacer el trabajo de inferir la conclusión."*

**Recomendación transversal (lista para implementar):** reescribir los siete títulos como conclusión, tomando el titular que ya existe en `conclusiones_ejecutivas_technostamp.md`. El texto ya está escrito — solo hay que moverlo al gráfico. No cambia ningún dato.

**Segundo defecto transversal:** los siete títulos están sin acentos (*Rotacion*, *Distribucion*, *Capacitacion*, *sucesion*, *reduccion*) mientras las etiquetas de eje y de categoría sí los llevan (*Logística*, *Ingeniería*, *Mantenimiento Eléctrico*). Dentro de la misma imagen conviven las dos ortografías. Es la misma clase de descuido de codificación que afecta a `decisions.md` y al `ESTUDIO` (subentregable 01, §5.1), y en una slide de directorio se lee como falta de terminación.

**Tercer defecto transversal:** ninguno de los 14 gráficos declara **universo (n) ni período**. `ESTUDIO` §9 lo pide explícitamente ("universo y período visibles"). Hoy el lector no sabe si el gráfico mira 694 personas o 562, 17 meses o 16.

---

## 2. Evaluación gráfico por gráfico — familia de decisión (G8–G14)

### G9 · Rotación por área con IC 95% — **el mejor del conjunto. Preservar.**

Un solo mensaje, una sola barra roja, el resto en gris, línea de referencia rotulada con el valor. Hace visible exactamente lo que el proyecto quiere defender: **por qué se prioriza un área y no se sobrerreacciona con las otras nueve**. Responde 1, 3 y parcialmente 2.

**Mejoras menores:** título como conclusión; anotar el n de cada área (hoy RRHH con 16 personas y Estampado con 185 tienen el mismo peso visual, y el intervalo de RRHH va de 1% a 28%, que es casi ninguna información); declarar universo y período.

### G14 · Business case por escenario — **el más riesgoso para el directorio.**

Nueve barras agrupadas, cada una rotulada al peso: `$194.840.088`, `$132.371.400`, `$121.775.055`… en vertical.

El problema no es estético. **Contradice a DEC-015**, que es la decisión que le da credibilidad al caso económico:

- DEC-015 exige publicar **un rango con los supuestos a la vista**. El gráfico publica nueve cifras puntuales y ningún supuesto.
- DEC-015 exige acompañar siempre el **piso verificable de $1,6M** (lo único que se sostiene sin supuestos propios). No aparece.
- Rotular al peso una cifra que es **97% supuesto** es publicar precisión inexistente — el error exacto que DEC-015 se propuso evitar.
- El eje Y está en `$M` y las etiquetas en pesos completos: dos unidades en la misma imagen.
- **Verde para "Agresivo"**: el escenario más especulativo se pinta con el color que el ojo lee como "seguro". La semántica de color está invertida.
- No usa la paleta que el propio script declara arriba (`AZUL, ROJO, GRIS, VERDE, NARANJA`): sale con los colores por defecto de matplotlib.

**Recomendación (requiere validación humana, porque cambia cómo el directorio lee la plata):** reemplazar por un único visual de rango — una barra o banda de $23M a $195M, con el punto central $83M marcado, el piso verificable de $1,6M como línea, y la distinción visual entre *dato medido* y *supuesto nuestro*. Es el gráfico que DEC-015 describe en palabras y que todavía no existe en imagen.

### G13 · Riesgo de sucesión por puesto — **el más débil. Rehacer o eliminar.**

Un scatter de burbujas con **tres puntos**, una barra de color continua para una variable que toma dos valores (1 y 2), y aproximadamente el 85% del lienzo vacío.

Pero el defecto grave es otro: **el gráfico no muestra la variable que sostiene el hallazgo.** El caso accionable es que el Supervisor de Logística tiene **dotación 1 y cero sucesores**. La cobertura no está codificada en ningún eje, tamaño ni color. Las propias conclusiones ejecutivas piden *"mostrar los puestos y su cobertura, no solo las edades"* — y el gráfico que citan no muestra cobertura.

Además el eje Y dice **"a 24 meses"** mientras el horizonte publicado en todo el informe es **12 meses** (coincide con la columna `en_riesgo_24m` señalada en el subentregable 02).

**Recomendación (lista para implementar):** una tabla de tres filas con puesto · personas en riesgo · dotación · sucesores · meses restantes comunica más y mejor que cualquier gráfico con tres puntos. Tres datos no necesitan un scatter.

### G11 · Incidentes por área y severidad — **contradice DEC-007 y no sostiene el insight que ilustra.**

Dos problemas independientes, ambos serios:

**(a) Es la evidencia equivocada.** El insight ejecutivo 3 se titula *"El turno noche concentra el riesgo de seguridad"* y cita este gráfico. El gráfico muestra **área y severidad — no turno**. El propio documento lo admite al pedir *"complementar con una tabla breve de turno y severidad"*. El titular más robusto del bloque de seguridad no tiene visual que lo respalde. Y como se documentó en el subentregable 02 §7, tampoco tiene tabla de soporte persistida.

**(b) Usa conteos absolutos, que es lo que DEC-007 prohíbe.** DEC-007 dice textualmente: *"Nunca comparar conteos de eventos entre grupos de tamaño distinto."* El gráfico muestra Ensamble con 14 incidentes y Calidad con 3 — sugiere 4,7 veces peor. Normalizado por empleado-mes, la brecha real que el propio informe publica es **19,6 vs 15,5 ×1.000: 26%, no 366%.** El gráfico dibuja la conclusión que el análisis descartó.

**(c)** Rojo/verde es la peor combinación posible para daltonismo, y el verde de "Leve" transmite "está bien" sobre 30 incidentes reales.

**Recomendación (lista para implementar):** reemplazar por incidentes **por turno**, en **tasa ×1.000 empleado-mes**, con la noche destacada — que es el hallazgo robusto, el que aparece en ambas fuentes y el que sostiene la Ficha C.

### G10 · Distribución de horas extra por área — **mide algo distinto de lo que el insight afirma.**

El insight ejecutivo 2 pide *"destacar Estampado, Ensamble y Mantenimiento Eléctrico por volumen/costo"*. El gráfico muestra **horas por empleado-mes**, no volumen ni costo. Y ordenado por mediana crea un ranking entre seis áreas de producción cuyas medianas van de 11,2 a 12,2 — diferencias que el propio informe no considera distinguibles.

Lo que el gráfico sí muestra bien es un corte binario: producción ~11–12 h/mes contra soporte ~4–6 h/mes. Ese es su mensaje real.

Falta lo accionable: el **umbral p80** que define sobrecarga crónica no aparece, y las **61 personas crónicas** —la población sobre la que se puede actuar— son invisibles.

**Recomendación (requiere criterio):** decidir qué pregunta responde. Si es "dónde está el costo", corresponde un gráfico de costo anualizado de HE por área. Si es "dónde está el riesgo humano", corresponde mostrar los 61 crónicos por área con el umbral marcado. Hoy responde una tercera pregunta que nadie hizo.

### G12 · Capacitación vs incidentes — **buena práctica adentro, ejecución mejorable.**

**Lo que hay que preservar:** la nota *"Comparacion descriptiva: no prueba causalidad"* impresa dentro del gráfico. Es la práctica más madura de todo el set visual y debería replicarse en cada gráfico asociativo.

**Lo que falla:** la nota está en gris claro y tamaño mínimo — a tamaño de slide desaparece, justo cuando más se la necesita. Logística en x=35 comprime los otros diez puntos en el tercio izquierdo. Y Dirección (12 empleado-mes, 0 incidentes, 0 horas) ancla la esquina inferior izquierda con el mismo peso visual que un área de 185 personas, sugiriendo visualmente una tendencia que el análisis no afirma.

### G8 · Rotación mensual original vs período limpio — **cumple su función. Preservar.**

Es el gráfico que hace visible DEC-017: muestra el pico artificial de enero y la serie corregida. Es honestidad metodológica hecha imagen y es de los pocos que un directorio agradece. **Debería ser anexo, no slide principal:** documenta una corrección del analista, no una decisión del negocio.

---

## 3. Familia exploratoria (G1–G7): buena calidad, ubicación equivocada

G4, G5 y G6 son grillas 2×2 con cuatro conclusiones en negrita cada una. Cada panel es correcto; el problema es la densidad: **cuatro insights simultáneos en una imagen obligan al lector a elegir por su cuenta cuál importa**, y un directorio no hace ese trabajo.

Sus títulos, en cambio, son el modelo a seguir:

> *"Pareto plano → el problema es SISTÉMICO, no de unos pocos abusadores"*
> *"CONTRA-INTUITIVO: el riesgo sube con la experiencia. Cero incidentes en los primeros 12 meses"*
> *"NO se sostiene: los márgenes de error se solapan (zona gris) — la diferencia puede ser azar"*

**Recomendación (lista para implementar):** declarar G1–G7 explícitamente como **anexo exploratorio** en el notebook y en el informe, y G8–G14 como el set de decisión. Hoy el notebook los presenta con el mismo peso, en la misma secuencia, y el lector recibe 18 paneles de exploración antes de llegar a los siete de decisión. Es un cambio de rótulo, no de contenido.

---

## 4. Narrativa: el documento ejecutivo está bien construido, con tres grietas

`conclusiones_ejecutivas_technostamp.md` respeta la estructura correcta —titular · impacto · evidencia · acción— y tiene una conclusión integradora que ordena todo: *"no hay un problema generalizado de personas, hay cuatro riesgos focalizados"*. Eso funciona y hay que preservarlo.

Las tres grietas, todas ya documentadas en subentregables anteriores:

| # | Grieta | Efecto en la audiencia |
|---|---|---|
| 1 | Titular con 15,0% y tabla de evidencia con 16,7% en el mismo insight | El directorio ve dos tasas de rotación de la misma empresa y no sabe cuál creer |
| 2 | Insight 3 titula sobre turno y muestra un gráfico de área | La evidencia no prueba el titular |
| 3 | Insight 4 titula sobre "4 de 5 posiciones críticas" usando el flag que DEC-006 declaró inutilizable | Suena a que se va el 80% del riesgo crítico; el dato honesto es un puesto unipersonal sin backup |

**Y una omisión de foco:** los cuatro insights se presentan con igual peso. El propio informe técnico dice que el caso económico *"descansa casi enteramente en la oportunidad A"* (retención), y que las oportunidades B, C y D se justifican por gestión de riesgo, no por retorno. Esa jerarquía —que es la información más útil para asignar presupuesto— está en el informe técnico y no en el documento ejecutivo.

---

## 5. Tablas: universo, denominador e incertidumbre

Revisadas las tablas de evidencia del documento ejecutivo:

| Aspecto | Estado |
|---|---|
| Denominador visible | Parcial. Insight 1 muestra "113 / 675"; insights 2, 3 y 4 no muestran denominador. |
| Período declarado | Sí, en el encabezado del documento. **Bien.** |
| Incertidumbre | Solo en insight 1 (IC 95%). Los insights 3 y 4 publican cifras sobre n=45 y n=5 sin ningún margen. |
| Exceso de detalle | La tabla del insight 2 tiene seis filas donde tres alcanzan; "Horas extra promedio enero 2024: 9,86" y "mayo 2025: 10,21" ocupan dos filas para decir "no cambió". |
| Precisión falsa | `$1.399,1M` y `$987,6M` con un decimal sobre una base de supuestos de cargas sociales. |

**Recomendación (lista para implementar):** agregar el n al pie de cada tabla de evidencia, y bajar a tres filas la tabla del insight 2 (peso sobre nómina, costo anualizado, personas con sobrecarga crónica).

---

## 6. Resumen de este subentregable

| # | Hallazgo | Estado propuesto |
|---|---|---|
| 1 | Los 7 títulos de decisión son descriptivos; los exploratorios sí concluyen | Lista para implementar |
| 2 | Los 7 títulos de decisión sin acentos, conviviendo con etiquetas acentuadas | Lista para implementar |
| 3 | Ningún gráfico declara universo ni período | Lista para implementar |
| 4 | G11 usa conteos absolutos contra DEC-007 y no muestra turno, que es el titular | Lista para implementar |
| 5 | G13 no codifica cobertura —la variable que sostiene el hallazgo— y dice 24 meses | Lista para implementar |
| 6 | G14 contradice DEC-015: nueve cifras al peso, sin rango, sin piso, sin supuestos | **Requiere validación humana** |
| 7 | G10 mide horas por persona cuando el insight habla de volumen y costo | Requiere criterio |
| 8 | G1–G7 no están rotulados como anexo exploratorio | Lista para implementar |
| 9 | Los cuatro insights ejecutivos no llevan la jerarquía que el informe técnico sí declara | **Requiere validación humana** |

**Preservar sin cambios:** G9 (foco y margen de error), G8 (honestidad metodológica visible), la nota de no-causalidad de G12, los títulos-conclusión de G1–G7 y la conclusión integradora del documento ejecutivo.

---

## Próximo subentregable

`05_documentacion_y_trazabilidad.md` — coherencia entre documentos, linaje, supuestos declarados y capacidad de auditoría externa.
