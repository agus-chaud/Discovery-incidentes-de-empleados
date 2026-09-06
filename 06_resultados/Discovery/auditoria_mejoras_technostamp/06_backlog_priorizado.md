# 06 · Backlog priorizado

**Auditoría integral TechnoStamp — subentregable 6 de 6**
**Orden:** (1) alto impacto / bajo esfuerzo · (2) alto impacto / esfuerzo medio · (3) alto impacto / requiere validación humana · (4) mejoras secundarias.

**Estados:**
- **Lista para implementar ahora** — no cambia conclusiones ni requiere definición de negocio.
- **Requiere validación humana** — puede cambiar interpretación, supuestos, prioridades, métricas, datos fuente o mensaje ejecutivo.

---

## Bloque 1 · Alto impacto / bajo esfuerzo

| # | Prioridad | Área | Mejora propuesta | Problema actual | Impacto de negocio | Esfuerzo | Estado | Evidencia | Archivos afectados |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Crítica | Notebook y experiencia de lectura | Alinear el nombre de columna `scrap_prom` → `scrap_prom_produccion` | El notebook lanza `CalledProcessError` en la celda 24 y, como `ejecutar_etapa` hace `raise`, el lector se detiene en la etapa 11 de 16 | El artefacto que prueba reproducibilidad no reproduce. Nadie que siga la instrucción del notebook llega al business case vigente ni a G8–G14 | Muy bajo | **Lista para implementar ahora** | Traceback en la salida guardada de la celda 24; `13_limpieza_v2.py` renombró la columna, `12_diagnostico_gaps.py` quedó en la versión v1 | `04_scripts/12_diagnostico_gaps.py` |
| 2 | Crítica | Documentación y trazabilidad | Regenerar `_linaje.json` desde `13_limpieza_v2.py` o consolidarlo con `transformaciones.json` | `_linaje.json` (3-sep 21:29) declara `script: 04_scripts/03_limpieza.py`; los parquet que describe los generó `13_limpieza_v2.py` el 5-sep 12:09 | DEC-001 y el informe §2 se apoyan textualmente en este archivo, y es uno de los 2 únicos archivos de la capa de datos versionados. Un auditor ve dos orígenes para el mismo dataset | Muy bajo | **Lista para implementar ahora** | Subentregable 05 §1; comparación de campo `script` y `mtime` | `06_resultados/Discovery/datos_transformados/_linaje.json` |
| 3 | Alta | Documentación y trazabilidad | Retirar `BC_resumen_oportunidades.csv` a `tablas_soporte/_superado/` | Salida de `09_business_case.py` (4-sep) contradice el rango vigente: $92,4M central y rango $55,4M–$147,8M contra $82,7M y $23,3M–$194,8M | Es la contradicción de datos más visible del proyecto. Si el directorio abre la carpeta de soporte, encuentra dos casos económicos distintos | Muy bajo | **Lista para implementar ahora** | Subentregable 02 §3; comparación directa de ambos CSV | `06_resultados/Discovery/tablas_soporte/BC_resumen_oportunidades.csv` |
| 4 | Alta | Documentación y trazabilidad | Reescribir DEC-018 y `ESTUDIO` §9 con escritura UTF-8 verificada | 34 tokens con `?` literal en `decisions.md` y 48 en `ESTUDIO_conceptos_technostamp.md` (`?rea`, `Decisi?n`, `Log?stica`, `n?mina`) | Los bytes son UTF-8 válido y no hay caracteres de reemplazo: el texto se escribió ya degradado. Visible para cualquiera que abra el archivo, y contradice el estándar de encoding que el propio proyecto fijó | Bajo | **Lista para implementar ahora** | Subentregable 01 §5.1; conteo de tokens con `?` literal | `decisions.md`, `ESTUDIO_conceptos_technostamp.md` |
| 5 | Alta | Notebook y experiencia de lectura | Agregar una celda markdown de 2–3 líneas **después** de cada etapa con el titular de lo que demostró | 1.222 líneas de `stdout` contra 107 de narrativa (11,4:1) y **cero** celdas de conclusión. El lector infiere solo | Convierte el notebook de registro de ejecución en documento leíble. Es la mejora de mayor retorno por esfuerzo de todo el proyecto | Bajo | **Lista para implementar ahora** | Subentregable 03 §3; conteo de líneas por celda | `03_notebooks/Technostamp_Completo.ipynb` |
| 6 | Alta | Visualizaciones y narrativa | Reescribir los 7 títulos de G8–G14 como conclusión, y con acentos | Los 7 títulos son descriptivos (*"Rotacion por area: diferencias con margen de error"*) y sin acentos, conviviendo con etiquetas de eje acentuadas | El texto del titular ya existe en `conclusiones_ejecutivas_technostamp.md`: solo hay que moverlo al gráfico. Los exploratorios G1–G7 ya lo hacen bien | Bajo | **Lista para implementar ahora** | Subentregable 04 §1; títulos extraídos del código | `04_scripts/18_visualizaciones_decision.py` |
| 7 | Alta | Documentación y trazabilidad | Crear `README.md` de una pantalla: qué es, para quién, dónde empezar según el rol, orden real de ejecución, qué está superado y por qué hay carpetas vacías | No hay punto de entrada. Las carpetas vacías `05_modelos/` y `07_despliegue/` comunican "trabajo pendiente" cuando reflejan la decisión —bien argumentada— de no modelar | Es lo primero que ve el cliente, el auditor o un entrevistador. Hoy tienen que adivinar el orden y el estado | Bajo | **Lista para implementar ahora** | Subentregable 05 §4 | `README.md` (nuevo) |
| 8 | Alta | Análisis y rigor | Persistir `P4_incidentes_por_turno.csv` (incidentes, empleado-mes de exposición, tasa ×1.000, días perdidos) | El 5,4x del turno noche es el hallazgo de seguridad más robusto, sostiene la Ficha C y el insight ejecutivo 3 — y **no tiene tabla de soporte**. `eventos_limpio.parquet` no tiene columna de turno | Sin reejecutar el pipeline, nadie puede verificar el número que sostiene la recomendación de seguridad | Bajo | **Lista para implementar ahora** | Subentregable 02 §7; inventario de `tablas_soporte/` | `04_scripts/06_p3_p4_p5.py` o `07_verif_incidentes_p5.py` |
| 9 | Alta | Análisis y rigor | Agregar columna `p_bonferroni` a `P5_rotacion_por_area_con_IC.csv` y una línea al informe | `ESTUDIO` §7 declara como hueco abierto que no se corrigió por comparaciones múltiples | El hallazgo **sobrevive**: z = 3,28 → p = 0,00104 contra umbral 0,005 (α/10). Convierte "la única área que se distingue, aunque no corregimos" en "se distingue incluso corrigiendo por haber testeado las diez". Refuerza la prioridad #1 delante de quien asigna presupuesto | Bajo | **Lista para implementar ahora** | Subentregable 02 §6; cálculo verificado | `04_scripts/17_business_case_v2.py`, `Discovery_report.md`, `ESTUDIO_conceptos_technostamp.md` |
| 10 | Media | Documentación y trazabilidad | Actualizar `Discovery_report.md` §13 (Reproducibilidad) al estado real | Declara "scripts 01…14", "G1–G7", "12 CSV" y un orden que omite 12, 15, 16, 17 y 18. En disco hay 18 scripts, 14 PNG y 17 CSV | La sección que existe para dar trazabilidad es la que peor describe el proyecto | Bajo | **Lista para implementar ahora** | Subentregable 01 §5.4; inventario de archivos | `06_resultados/Discovery/Discovery_report.md` |
| 11 | Media | Visualizaciones y narrativa | Reemplazar G13 por una tabla de tres filas: puesto · personas en riesgo · dotación · sucesores · meses restantes | Scatter de 3 puntos, barra de color continua para una variable de 2 valores, 85% del lienzo vacío, eje Y dice "24 meses" contra los 12 publicados, y **no codifica cobertura** — la variable que sostiene el hallazgo | El caso accionable es "dotación 1, cero sucesores, 6 meses" y hoy el gráfico no lo muestra. Las propias conclusiones piden mostrar cobertura | Bajo | **Lista para implementar ahora** | Subentregable 04 §2; inspección del PNG y del código | `04_scripts/18_visualizaciones_decision.py`, `conclusiones_ejecutivas_technostamp.md` |
| 12 | Media | Notebook y experiencia de lectura | Rotular G1–G7 como anexo exploratorio y G8–G14 como set de decisión | El notebook los presenta con el mismo peso: 18 paneles de exploración antes de los 7 de decisión | Cambio de rótulo, no de contenido. Reduce la carga cognitiva del lector ejecutivo | Muy bajo | **Lista para implementar ahora** | Subentregable 04 §3 | `03_notebooks/Technostamp_Completo.ipynb`, `Discovery_report.md` |
| 13 | Media | Análisis y rigor | Aplicar el período limpio dentro de `10_sensibilidad_he.py` y actualizar la cifra de DEC-009 | El informe publica "crónicos 19,7% vs resto 16,4%" pero el script imprime 19,0% porque usa los 17 meses sin DEC-017. **El 16,4% no lo produce ninguna salida persistida** | Número correcto sin fuente reproducible. La conclusión de DEC-009 no cambia (z = 0,64, sigue sin ser demostrable) | Bajo | **Lista para implementar ahora** | Subentregable 03 §5.4; ambos valores reproducidos | `04_scripts/10_sensibilidad_he.py`, `decisions.md` (DEC-009) |
| 14 | Media | Documentación y trazabilidad | Versionar `conclusiones_ejecutivas_technostamp.md` | El documento que va al directorio es el único entregable sin historial en git | Sin trazabilidad de versiones en el artefacto de mayor exposición externa | Muy bajo | **Lista para implementar ahora** | `git status` | repositorio |
| 15 | Media | Notebook y experiencia de lectura | Corregir el texto de cierre: "15 etapas" → 16 | `ETAPAS_EJECUTADAS` lista 16 y el markdown dice 15 | Detalle, pero es la última línea que lee quien recorre el notebook | Muy bajo | **Lista para implementar ahora** | Subentregable 03 §6 | `03_notebooks/Technostamp_Completo.ipynb` |

---

## Bloque 2 · Alto impacto / esfuerzo medio

| # | Prioridad | Área | Mejora propuesta | Problema actual | Impacto de negocio | Esfuerzo | Estado | Evidencia | Archivos afectados |
|---|---|---|---|---|---|---|---|---|---|
| 16 | Alta | Documentación y trazabilidad | Propagar `ROOT = Path(__file__).resolve().parents[1]` a los 17 scripts que hoy usan path absoluto | 17 de 18 scripts tienen `C:\Users\Dell\Agus\Nivii AI` escrito a mano. Solo `18_visualizaciones_decision.py` hace lo correcto | El proyecto declara reproducibilidad como principio (DEC-001, DEC-014, informe §13) y el pipeline solo arranca en una máquina. Es la objeción más obvia que puede hacer un cliente o un entrevistador | Medio (mecánico, 17 archivos) | **Lista para implementar ahora** | Subentregable 03 §4; conteo por script | `04_scripts/*.py` (17) |
| 17 | Alta | Visualizaciones y narrativa | Reemplazar G11 por incidentes **por turno**, en **tasa ×1.000 empleado-mes**, con la noche destacada | G11 muestra área y severidad cuando el insight 3 titula sobre turno, y usa **conteos absolutos** — lo que DEC-007 prohíbe explícitamente. Dibuja Ensamble 14 vs Calidad 3 (4,7x) cuando la tasa real publicada es 19,6 vs 15,5 ×1.000 (26%) | El gráfico dibuja la conclusión que el propio análisis descartó, y no sostiene el titular que ilustra. Es el defecto de evidencia más serio del set visual | Medio | **Lista para implementar ahora** | Subentregable 04 §2; DEC-007; inspección del PNG | `04_scripts/18_visualizaciones_decision.py`, `conclusiones_ejecutivas_technostamp.md` |
| 18 | Media | Notebook y experiencia de lectura | Crear `04_scripts/_comun.py` con raíz del proyecto, carga de parquet y definiciones de negocio compartidas | La regla "sobrecarga crónica" (p80 · ≥70% de meses · ≥6 meses) está escrita en 3 scripts. Hoy coinciden en 61 personas, pero cambiarla en 2 de 3 produce divergencia silenciosa | Una sola definición por concepto de negocio. Elimina ~110 líneas de repetición | Medio | Requiere criterio de refactor (no cambia conclusiones) | Subentregable 03 §5.3 | `04_scripts/06_p3_p4_p5.py`, `10_sensibilidad_he.py`, `11_verif_cronicos_seguridad.py` |
| 19 | Media | Documentación y trazabilidad | Marcar `03_limpieza.py` y `09_business_case.py` como superados (sufijo, encabezado o carpeta `_superado/`) y documentar el orden real | La numeración promete `01 → 02 → 03…`; el orden real es `01 → 02 → 13 → 04 → …`. Nada en el nombre del archivo indica cuál manda | Un lector nuevo usa el script equivocado. Ya pasó con la salida de `09` (ítem 3) | Medio (renombrar afecta documentación) | Requiere criterio | Subentregable 03 §5.1 y §5.2 | `04_scripts/`, `Discovery_report.md`, `README.md` |
| 20 | Media | Documentación y trazabilidad | Declarar la exclusión de datos como decisión y versionar las tablas de soporte agregadas | `.gitignore` excluye `*.csv` y `*.parquet`: de 41 archivos versionados, ninguno es dato. La capa de evidencia auditable no viaja con el proyecto, y la exclusión no está declarada | Combinado con los paths absolutos, nadie fuera de esta máquina puede verificar una sola cifra. Versionar las agregadas (todas menos `P3_cronicos_detalle.csv` y `P3_sobrecargados_cronicos.csv`) vuelve el informe verificable sin exponer nóminas | Medio | Requiere criterio (decisión de privacidad) | Subentregable 05 §3; `git ls-files` | `.gitignore`, `decisions.md` |

---

## Bloque 3 · Alto impacto / requiere validación humana

### 21 · Unificar la definición de tasa de rotación en todo el material

| Campo | Detalle |
|---|---|
| **Área** | Análisis y rigor · Visualizaciones y narrativa |
| **Problema actual** | Con los mismos 113 casos existen tres tasas anuales defendibles: **15,04%** (salidas anualizadas / dotación activa promedio 563,4), **16,74%** (acumulada del período limpio sobre 675 personas) y **12,56%** (tasa del período anualizada). El insight ejecutivo 1 titula con 15,0% y su tabla de evidencia, dos párrafos abajo, compara 16,7% contra 34,8% |
| **Impacto de negocio** | El directorio lee dos tasas de rotación de la misma empresa en la misma slide. Además, el 34,8% de Mantenimiento Eléctrico está calculado en base 16,74%: contra el titular de 15,0% la brecha parece 2,32x cuando la correcta es 2,08x |
| **Esfuerzo** | Bajo una vez decidida la definición |
| **Estado** | **Requiere validación humana** |
| **Qué decisión humana falta** | Cuál de las tres definiciones es la oficial de TechnoStamp para reportar rotación |
| **Quién debería validarla** | Martina Rosales (Head de RR.HH.), porque debe ser consistente con cómo RR.HH. reporta rotación internamente y ante el directorio |
| **Qué riesgo evita** | Que el directorio detecte dos cifras y descarte el informe entero; y que se dimensione mal la brecha del área priorizada |
| **Qué evidencia adicional lo resuelve** | Saber si RR.HH. ya reporta una tasa de rotación y con qué denominador. Si no existe, adoptar la definición A (anualizada sobre dotación activa promedio) y escribirla una vez debajo del titular |
| **Evidencia** | Subentregable 02 §2; los tres cálculos reproducidos |
| **Archivos afectados** | `conclusiones_ejecutivas_technostamp.md`, `Discovery_report.md`, `04_scripts/17_business_case_v2.py`, `18_visualizaciones_decision.py` |

### 22 · Reformular el insight ejecutivo de sucesión

| Campo | Detalle |
|---|---|
| **Área** | Análisis y rigor · Visualizaciones y narrativa |
| **Problema actual** | El insight 4 titula *"Cuatro de las cinco posiciones críticas activas llegan a jubilación"* usando `es_posicion_critica` — el flag que DEC-006 declaró no utilizable como insumo analítico, exigiendo declarar la limitación siempre que se use. El dato es correcto (verificado: los 4 que se jubilan ≤12 meses tienen el flag), pero el universo de 5 personas es un registro no mantenido (1,4% del padrón, constante en 17 meses) |
| **Impacto de negocio** | *"Cuatro de cinco críticos se jubilan"* suena a que se va el 80% del riesgo crítico. Lo que el dato realmente dice es que el registro de posiciones críticas tiene 5 personas y no sirve para planificar. El hallazgo accionable y honesto ya está en el informe pero no en el titular: **un puesto unipersonal, sin backup, se va en 6 meses** |
| **Esfuerzo** | Bajo |
| **Estado** | **Requiere validación humana** |
| **Qué decisión humana falta** | Si el titular ejecutivo se reformula sobre el caso unipersonal observable, dejando "4 de 5 críticos" como evidencia con la salvedad de cobertura del flag |
| **Quién debería validarla** | Martina Rosales, y el CEO si el mensaje al directorio ya fue comunicado |
| **Qué riesgo evita** | Presentar como cobertura completa del riesgo de sucesión un análisis apoyado en un registro que el propio proyecto documentó como no mantenido. Si el directorio pregunta "¿y las otras posiciones críticas?", la respuesta hoy es "el sistema solo tiene cinco cargadas" |
| **Qué evidencia adicional lo resuelve** | Que RR.HH. confirme o actualice el padrón de posiciones críticas, o que se adopte formalmente el índice de criticidad de DEC-006 (47 empleados, 8,4%) — que es la decisión pendiente que ya figura en `decisions.md` |
| **Evidencia** | Subentregable 02 §4; DEC-006; verificación de los 4 casos |
| **Archivos afectados** | `conclusiones_ejecutivas_technostamp.md`, `decisions.md`, `04_scripts/18_visualizaciones_decision.py` |

### 23 · Rehacer G14 como visual de rango, no de nueve cifras puntuales

| Campo | Detalle |
|---|---|
| **Área** | Business case · Visualizaciones y narrativa |
| **Problema actual** | Nueve barras agrupadas rotuladas al peso (`$194.840.088`, en vertical), sin rango, sin el piso verificable de $1,6M, sin distinguir dato medido de supuesto, con verde para el escenario "Agresivo" y sin usar la paleta que el propio script declara |
| **Impacto de negocio** | Contradice a DEC-015, que es la decisión que le da credibilidad al caso económico. Rotular al peso una cifra que es **97% supuesto** publica precisión inexistente: exactamente el error que DEC-015 se propuso evitar |
| **Esfuerzo** | Medio |
| **Estado** | **Requiere validación humana** |
| **Qué decisión humana falta** | Qué escenario y qué porcentaje de reducción se presentan como referencia al directorio, y si se muestran los tres escenarios o solo el rango con el punto central |
| **Quién debería validarla** | CEO y Directorio, porque define sobre qué cifra se conversa la inversión en retención |
| **Qué riesgo evita** | Que el directorio ancle en $194,8M —el número más grande y más especulativo de la imagen— y luego descubra que el 97% es supuesto propio. Eso destruye la credibilidad de todo el informe, incluido lo que sí está bien fundado |
| **Qué evidencia adicional lo resuelve** | Los dos datos que el informe §9 ya identifica: producción promedio de un operario formado (unidades/mes por puesto) y meses hasta alcanzar ese nivel. Con eso el rango de 8,4x se comprime |
| **Evidencia** | Subentregable 04 §2; DEC-015; `BC_supuestos.json` |
| **Archivos afectados** | `04_scripts/18_visualizaciones_decision.py`, `conclusiones_ejecutivas_technostamp.md` |

### 24 · Explicitar la jerarquía de las cuatro oportunidades en el documento ejecutivo

| Campo | Detalle |
|---|---|
| **Área** | Business case · Visualizaciones y narrativa |
| **Problema actual** | Los cuatro insights se presentan con igual peso. El informe técnico dice que el caso económico *"descansa casi enteramente en la oportunidad A"* (retención) y que B, C y D se justifican por gestión de riesgo, no por retorno. Esa jerarquía no está en el documento ejecutivo |
| **Impacto de negocio** | Es la información más útil para asignar presupuesto, y hoy está solo en el documento que el directorio no lee |
| **Esfuerzo** | Bajo |
| **Estado** | **Requiere validación humana** |
| **Qué decisión humana falta** | Confirmar el orden de prioridad para la conversación con el directorio, y si seguridad y sucesión se presentan explícitamente como gestión de riesgo sin retorno financiero prometido |
| **Quién debería validarla** | Martina Rosales y el CEO |
| **Qué riesgo evita** | Que las cuatro iniciativas compitan por presupuesto como si tuvieran el mismo sustento económico, cuando solo una lo tiene |
| **Qué evidencia adicional lo resuelve** | Ninguna adicional: la evidencia ya está en el informe §8 y §9. Es una decisión de comunicación |
| **Evidencia** | Subentregable 04 §4; `Discovery_report.md` §8 y §9 |
| **Archivos afectados** | `conclusiones_ejecutivas_technostamp.md` |

---

## Bloque 4 · Mejoras secundarias

| # | Prioridad | Área | Mejora propuesta | Problema actual | Impacto de negocio | Esfuerzo | Estado | Evidencia | Archivos afectados |
|---|---|---|---|---|---|---|---|---|---|
| 25 | Baja | Visualizaciones y narrativa | Declarar universo (n) y período dentro de cada gráfico | Ninguno de los 14 PNG lo hace, pese a que `ESTUDIO` §9 lo exige | El lector no sabe si mira 694 personas o 562, 17 meses o 16 | Bajo | **Lista para implementar ahora** | Subentregable 04 §1 | `04_scripts/08_visualizaciones.py`, `18_visualizaciones_decision.py` |
| 26 | Baja | Visualizaciones y narrativa | Anotar el n por área en G9 | RRHH (n=16) y Estampado (n=185) tienen el mismo peso visual; el IC de RRHH va de 1% a 28% | Refuerza el mensaje de "no sobrerreaccionar con las otras nueve áreas" | Muy bajo | **Lista para implementar ahora** | Subentregable 04 §2 | `04_scripts/18_visualizaciones_decision.py` |
| 27 | Baja | Visualizaciones y narrativa | Hacer legible la nota de no-causalidad de G12 y replicarla en todo gráfico asociativo | Está en gris claro y tamaño mínimo; a tamaño de slide desaparece | Es la mejor práctica del set visual y hoy es invisible justo cuando más se la necesita | Muy bajo | **Lista para implementar ahora** | Subentregable 04 §2 | `04_scripts/18_visualizaciones_decision.py` |
| 28 | Baja | Visualizaciones y narrativa | Reformular G10 según la pregunta que deba responder | Muestra horas por empleado-mes cuando el insight 2 habla de volumen y costo; ordena por mediana entre seis áreas indistinguibles (11,2–12,2 h); el umbral p80 y los 61 crónicos no aparecen | Hoy responde una tercera pregunta que nadie hizo | Medio | Requiere criterio | Subentregable 04 §2 | `04_scripts/18_visualizaciones_decision.py` |
| 29 | Baja | Notebook y experiencia de lectura | Mover el detalle de las 3 etapas más ruidosas a un archivo de log y dejar solo el resumen | `06_p3_p4_p5` imprime 205 líneas, `07_verif_incidentes_p5` 169, `01_perfilado` 94 | Complementa el ítem 5. No urgente | Medio | Requiere criterio | Subentregable 03 §3 | `04_scripts/`, `03_notebooks/` |
| 30 | Baja | Documentación y trazabilidad | Eliminar los 3 CSV duplicados de la raíz y documentar por qué existen las 7 carpetas vacías | Sugieren dos fuentes de datos posibles y trabajo pendiente | Reduce el ruido para un lector nuevo. Se resuelve junto con el README (ítem 7) | Muy bajo | **Lista para implementar ahora** | Subentregable 01 §3 | raíz del repositorio |
| 31 | Baja | Análisis y rigor | Nombrar la censura por la derecha en el informe técnico, no solo en el material de estudio | `ESTUDIO` §7 la declara; el `Discovery_report.md` §11 ("Qué NO se puede afirmar") no la incluye | Con 16 meses el efecto es acotado, pero nombrar la debilidad propia antes de que la señalen es lo que sostiene la credibilidad del resto | Muy bajo | **Lista para implementar ahora** | Subentregable 02 §8 | `Discovery_report.md` §11 |
| 32 | Baja | Visualizaciones y narrativa | Reducir a tres filas la tabla de evidencia del insight 2 y agregar el n al pie de cada tabla | Seis filas donde tres alcanzan; "9,86 h en enero" y "10,21 h en mayo" ocupan dos filas para decir "no cambió"; los insights 2, 3 y 4 no muestran denominador | Menos carga cognitiva, más contexto donde hace falta | Muy bajo | **Lista para implementar ahora** | Subentregable 04 §5 | `conclusiones_ejecutivas_technostamp.md` |

---

## Nuevos datos y métricas propuestos

Solo se proponen los que resuelven una brecha ya documentada por el propio proyecto. Ninguno se propone "porque sí".

### N1 · Producción promedio de un operario formado

| Campo | Detalle |
|---|---|
| **Definición** | Unidades producidas por mes por un empleado que ya alcanzó rendimiento pleno, desagregado por puesto |
| **Fuente potencial** | Sistema de producción / MES de planta. El proyecto ya observa `unidades_producidas` y `tasa_scrap_porcentaje` en las tres áreas de producción |
| **Granularidad y frecuencia** | Puesto × mes; carga mensual |
| **Decisión que habilita** | Convierte el componente "rampa del ingresante" del costo por salida de supuesto a medición. Junto con N2, comprime el rango de $23M–$195M a algo defendible ante el directorio |
| **Por qué hoy no puede afirmarse** | El 97% del costo por salida ($5,68M de $5,88M) son dos supuestos propios: vacancia y rampa. El informe §9 identifica este dato explícitamente como uno de los dos que cerrarían el rango |

### N2 · Meses hasta rendimiento pleno de un ingresante

| Campo | Detalle |
|---|---|
| **Definición** | Cantidad de meses desde el ingreso hasta alcanzar la producción media del puesto (N1) |
| **Fuente potencial** | Cruce del sistema de producción con la fecha de ingreso del panel de RR.HH. Es derivable si N1 existe |
| **Granularidad y frecuencia** | Puesto; recalculable trimestralmente |
| **Decisión que habilita** | Cierra el segundo supuesto del costo por salida. Con N1 y N2, el caso económico de retención pasa de rango de 8,4x a estimación con incertidumbre acotada |
| **Por qué hoy no puede afirmarse** | El escenario central asume "rinde 50% durante 3 meses" y el agresivo "6 meses". Ambos son juicio, no medición, y mueven el ahorro anual entre $49,6M y $132,4M solo con esa variable |

### N3 · Entrevistas de salida estructuradas

| Campo | Detalle |
|---|---|
| **Definición** | Cuestionario cerrado al momento de la baja: motivo principal, destino, factores de decisión, satisfacción con jefatura y con compensación |
| **Fuente potencial** | Proceso nuevo de RR.HH.; el informe §12 ya lo propone como experimento de 3 meses sin prerrequisitos |
| **Granularidad y frecuencia** | Una por baja; continuo |
| **Decisión que habilita** | Es lo que separa "sabemos quién se va y cuánto cuesta" de "sabemos por qué". Sin esto, cualquier programa de retención en Mantenimiento Eléctrico es una apuesta |
| **Por qué hoy no puede afirmarse** | El informe §11 lo declara textualmente: no hay entrevistas de salida ni encuestas de clima. La hipótesis del área (competencia salarial externa, carga de guardias, liderazgo local) está sin testear |

### N4 · Turno del incidente en la ficha de `eventos_rrhh`

| Campo | Detalle |
|---|---|
| **Definición** | Turno en que ocurrió el incidente, cargado en la ficha del evento y no inferido por cruce con el panel del mes |
| **Fuente potencial** | Formulario de carga de incidentes existente; es un campo, no un sistema nuevo |
| **Granularidad y frecuencia** | Por incidente; continuo |
| **Decisión que habilita** | Vuelve auditable el hallazgo que sostiene toda la recomendación de seguridad. Hoy el 5,4x se obtiene cruzando eventos contra el panel del mes, lo que asume que la persona no cambió de turno |
| **Por qué hoy no puede afirmarse** | `eventos_limpio.parquet` no tiene columna de turno. El número es correcto pero su cadena de derivación no está persistida ni es verificable sin reejecutar el pipeline |

### N5 · Ficha de investigación obligatoria con causa raíz

| Campo | Detalle |
|---|---|
| **Definición** | Validación en el sistema de nómina: no se cierra el mes con incidentes registrados sin ficha asociada, y la acción correctiva es campo obligatorio de texto libre distinto del valor por defecto |
| **Fuente potencial** | Control de proceso en el sistema actual, no analítica |
| **Granularidad y frecuencia** | Por incidente; continuo. KPI mensual: % de incidentes con causa raíz (baseline 45%) |
| **Decisión que habilita** | Sin esto ninguna conclusión de seguridad es defendible. Es el habilitador de la Ficha C, y el propio informe lo prioriza como oportunidad #2 pese a no tener ROI |
| **Por qué hoy no puede afirmarse** | 55 de ~100 incidentes no tienen ficha, y de los 45 que la tienen, solo 15 registran acción correctiva — las 15 con la misma frase. No hay análisis de causa raíz que analizar |

### N6 · Auditoría del campo `meses_desde_ultimo_aumento` en las bajas

| Campo | Detalle |
|---|---|
| **Definición** | No es una métrica nueva: es verificar cómo se escribe el campo existente al momento de registrar una baja |
| **Fuente potencial** | RR.HH. y el sistema de nómina |
| **Granularidad y frecuencia** | Una sola auditoría |
| **Decisión que habilita** | Determina si el patrón contra-intuitivo (1,0 mes en renuncias vs 4,5 en activos) es una señal real —contraofertas fallidas— o un artefacto de registro. Si es real, es una señal de fuga temprana valiosa para el tablero de retención |
| **Por qué hoy no puede afirmarse** | Ya está correctamente marcado en el informe §7 como "señal a investigar, no a concluir" y figura como decisión pendiente en `decisions.md`. Es la validación de menor costo del proyecto |

---

## Cierre

### Las 5 mejoras con mayor retorno para claridad y utilidad de negocio

1. **Arreglar el corte del notebook** (ítem 1). Es una línea de código y hoy impide que cualquiera llegue a ver el business case vigente ni los siete gráficos de decisión.
2. **Agregar celdas de conclusión después de cada etapa** (ítem 5). 1.222 líneas de salida cruda contra 107 de narrativa: hoy el lector hace el trabajo de inferir que el analista ya hizo.
3. **Reescribir los siete títulos de los gráficos de decisión como conclusión** (ítem 6). El texto ya está escrito en las conclusiones ejecutivas; hay que moverlo al gráfico.
4. **Eliminar las dos contradicciones de trazabilidad** (ítems 2 y 3): un archivo de linaje que apunta al script equivocado y un business case obsoleto conviviendo con el vigente. Son las dos cosas que un auditor encuentra primero.
5. **Crear el README** (ítem 7). Convierte siete carpetas vacías de "trabajo pendiente" en "decisión argumentada de no modelar", que es lo que realmente son.

### Las 3 validaciones humanas más importantes

1. **Cuál es la definición oficial de tasa de rotación** (ítem 21) — Martina Rosales. Hoy conviven 15,0% y 16,7% en la misma slide.
2. **Si el insight de sucesión se reformula sobre el caso unipersonal** (ítem 22) — Martina Rosales y CEO. El titular actual se apoya en el flag que el propio proyecto declaró no mantenido.
3. **Qué escenario del business case se presenta como referencia** (ítem 23) — CEO y Directorio. Evita que se ancle en $194,8M, la cifra más grande y más especulativa de la imagen.

### Qué debe preservarse porque ya es sólido

- **La arquitectura notebook-orquestador / scripts-lógica.** Sin duplicación, sin estado oculto entre celdas, con fallo visible en vez de silencioso.
- **`transformaciones.json`**: 31 pasos con parámetros ya calculados, más `regla_general`, `codificacion` y `areas_produccion` como campos explícitos. Es el activo de reproducibilidad del proyecto.
- **La estructura de `decisions.md`**: decisión · alternativa descartada · por qué se descartó · conclusión · bug evitado. Es un artefacto poco común y muy defendible.
- **La sección "Qué NO se puede afirmar" y la tabla de "afirmaciones retiradas"** del informe técnico, con el nivel de evidencia declarado por hallazgo.
- **El tratamiento del business case como rango con piso verificable** (DEC-015), y la cuantificación explícita de que el 97% es supuesto propio.
- **G9** (foco en la única área que se distingue, con margen de error y línea de referencia), **G8** (hace visible la corrección de DEC-017) y la nota de no-causalidad de **G12**.
- **Los títulos-conclusión de G1–G7** y la conclusión integradora del documento ejecutivo.
- **DEC-004, DEC-009, DEC-015, DEC-016 y DEC-017**: cinco decisiones que corrigieron conclusiones contra la intuición y contra lo que el cliente esperaba escuchar.

### Conclusión ejecutiva

El análisis de TechnoStamp es riguroso y sus conclusiones se sostienen: la aritmética verifica. Lo que falla es el empaquetado — un notebook que se corta, títulos que no concluyen, dos artefactos obsoletos que contradicen a los vigentes. Arreglos de bajo esfuerzo, alto retorno en credibilidad.
