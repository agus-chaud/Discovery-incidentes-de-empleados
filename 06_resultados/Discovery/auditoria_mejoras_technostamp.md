# Auditoría integral TechnoStamp — informe consolidado

**Fecha del diagnóstico:** 5 de septiembre de 2026 · **Última actualización:** 6 de septiembre de 2026 (ver §1.1)
**Alcance original:** diagnóstico y recomendación. A partir del §1.1, este informe también registra qué recomendaciones ya se implementaron.
**Objetivo:** que el proyecto sea más simple de entender y mantener, más visual y fácil de comunicar, y más útil, riguroso y accionable para el negocio.

**Detalle completo por capítulo:** `06_resultados/Discovery/auditoria_mejoras_technostamp/` (seis subentregables).

---

## 1. Veredicto general

**El análisis es sólido. El empaquetado es lo que falla.**

Se recalcularon todas las cifras del documento ejecutivo contra los parquet y las tablas de soporte. **Ninguna está mal calculada.** Las decisiones metodológicas están bien argumentadas y, en cinco casos, corrigieron conclusiones contra la intuición y contra lo que el cliente esperaba escuchar.

Los problemas encontrados son de tres tipos, y ninguno invalida el análisis:

| Tipo | Ejemplo | Efecto |
|---|---|---|
| **Definición** | Tres tasas de rotación defendibles, dos publicadas sin distinguir denominador | El directorio no sabe cuál creer |
| **Consistencia** | Un archivo de linaje que apunta al script superado; un business case obsoleto junto al vigente | Un auditor encuentra dos versiones del mismo hecho |
| **Comunicación** | Títulos de gráfico que describen el eje en vez de enunciar la conclusión | La audiencia hace el trabajo que el analista ya hizo |

De los 32 ítems del backlog, **20 eran implementables de inmediato** sin cambiar conclusiones ni pedir definiciones de negocio. Solo **4 tocan el mensaje ejecutivo** y necesitan firma humana.

### 1.1 · Estado de implementación (actualizado 6-sep-2026)

Seis de los hallazgos del §3 ya se resolvieron. El detalle de cada uno está documentado en `decisions.md` (DEC-019 a DEC-021) y en el subentregable `06_backlog_priorizado.md`, que conserva el estado original de cada ítem.

| # | Hallazgo | Estado | Decisión |
|---|---|---|---|
| 3.1 | El notebook se cortaba en la etapa 11/16 | ✅ **Resuelto** | Columna alineada en `12_diagnostico_gaps.py`; el notebook corre de punta a punta |
| 3.2 | Tres tasas de rotación conviviendo sin distinguirse | ✅ **Resuelto** | **DEC-019** — se unificó en 16,7% (acumulada del período), la misma base que ya usaban las diez áreas |
| 3.4 | Títulos de G8–G14 describían el eje, no concluían | ✅ **Resuelto** | Los 7 títulos reescritos como conclusión, con acentos |
| 3.5 (G11) | G11 no probaba el hallazgo de turno noche y usaba conteo bruto | ✅ **Resuelto** | **DEC-021** — G11 rehecho por tasa ×1.000 empleado-mes y turno; se persiste `tablas_soporte/P4_incidentes_por_turno.csv` |
| 3.6 | Bonferroni declarado como hueco abierto | ✅ **Resuelto** | **DEC-020** — corrido; Mantenimiento Eléctrico sobrevive (p = 0,00105 vs umbral 0,005) |
| — | G10 titulaba "producción vs soporte", una categoría que el gráfico no muestra | ✅ **Resuelto** | Título reemplazado por lo que el gráfico efectivamente grafica (11 áreas ordenadas, extremos nombrados) |

**Sigue pendiente**, sin cambios desde el diagnóstico original: los dos artefactos obsoletos de 3.3 (`_linaje.json` y `BC_resumen_oportunidades.csv`), G13 dentro de 3.5, la reformulación del insight de sucesión, el rediseño de G14, el README, los paths absolutos de 17 scripts, y el resto del backlog de la sección 4.

---

## 2. Mapa del proyecto

```
02_datos/01_Originales/  (RAW inmutable, 3 CSV)
        ▼  01_perfilado · 02_calidad · 13_limpieza_v2   ← única etapa que escribe datos
datos_transformados/  4 parquet + transformaciones.json (31 pasos) + politica_vacios.csv
        ▼  11 scripts de análisis
tablas_soporte/ (17 CSV + BC_supuestos.json)   ·   EDA_report.md (54 alertas)
        ▼  08_visualizaciones → G1–G7 (exploratorios)
           18_visualizaciones_decision → G8–G14 (de decisión)
        ▼
Discovery_report.md · conclusiones_ejecutivas_technostamp.md · decisions.md · ESTUDIO
```

**Orquestador:** `03_notebooks/Technostamp_Completo.ipynb` corre cada script como proceso independiente y renderiza los PNG inline. No duplica lógica.

---

## 3. Los seis hallazgos que más importan

### 3.1 · El notebook no corre de punta a punta — ✅ Resuelto

`12_diagnostico_gaps.py` usa la columna `scrap_prom`; `13_limpieza_v2.py` la renombró a `scrap_prom_produccion`. Es un contrato roto en la migración v1 → v2: el script quedó escrito contra la salida de `03_limpieza.py`.

Como `ejecutar_etapa` lanza excepción ante un fallo, **el lector que sigue la instrucción del propio notebook se detiene en la etapa 11 de 16** y nunca ve el EDA sistemático, el diagnóstico de fragilidad, la rotación corregida, el business case vigente ni los siete gráficos de decisión.

Revisé las 102 columnas de los cuatro parquet contra las referencias de los 18 scripts: **es el único contrato roto.** No hay problema sistémico, y arreglarlo no cambia ninguna cifra publicada.

### 3.2 · Conviven tres tasas de rotación y se publican dos sin distinguirlas — ✅ Resuelto

Con los mismos 113 casos:

| Definición | Resultado |
|---|---:|
| Salidas anualizadas / dotación activa promedio (563,4) | **15,04%** |
| Tasa acumulada del período limpio (113 / 675) | **16,74%** |
| Tasa del período anualizada | 12,56% |

El insight ejecutivo 1 titula con **15,0%** y su tabla de evidencia, dos párrafos abajo, compara **16,7%** contra el 34,8% de Mantenimiento Eléctrico. Y como ese 34,8% está calculado en base 16,74%, compararlo contra el titular **infla la brecha de 2,08x a 2,32x**.

Se resuelve con una línea de texto, pero requiere decidir cuál es la definición oficial. **Actualización:** se adoptó la definición acumulada (16,7%) — DEC-019. `Discovery_report.md`, `conclusiones_ejecutivas_technostamp.md` y `16_rotacion_temporal.py` ya están consistentes.

### 3.3 · Dos artefactos obsoletos contradicen a los vigentes — abierto

| Artefacto obsoleto | Qué dice | Qué dice el vigente |
|---|---|---|
| `tablas_soporte/BC_resumen_oportunidades.csv` (4-sep) | Retención: $55,4M / **$92,4M** / $147,8M | `BC_rango_retencion.csv`: $23,3M / **$82,7M** / $194,8M |
| `datos_transformados/_linaje.json` (3-sep) | Datos generados por `03_limpieza.py` | `transformaciones.json`: generados por `13_limpieza_v2.py` |

El segundo es el más grave: **DEC-001 y el informe §2 se apoyan textualmente en `_linaje.json`**, y es uno de los dos únicos archivos de la capa de datos versionados en git. Un auditor externo ve dos scripts declarados como origen del mismo dataset.

### 3.4 · Los gráficos de decisión abandonaron el principio que el proyecto mismo enseña — ✅ Resuelto

| | G1–G7 (exploratorios) | G8–G14 (de decisión) |
|---|---|---|
| Títulos | **Conclusiones**: *"Turno NOCHE: 5,4x el riesgo"*, *"NO se sostiene: los márgenes se solapan"* | **Descriptivos**: *"Rotacion por area: diferencias con margen de error"* |
| Paneles | 18 paneles en 7 imágenes | 1 panel por imagen ✅ |

Los siete títulos de decisión describen el eje. Ninguno dice qué concluir — que es exactamente el contraejemplo que `ESTUDIO` §9 usa. **El texto del titular ya está escrito en las conclusiones ejecutivas: solo hay que moverlo al gráfico.** Además los siete están sin acentos, conviviendo dentro de la misma imagen con etiquetas de eje acentuadas.

### 3.5 · Dos gráficos no sostienen el hallazgo que ilustran — G11 resuelto, G13 abierto

- **G11** se citaba como evidencia de *"el turno noche concentra el riesgo"* pero mostraba **área y severidad, no turno**. Y usaba **conteos absolutos** — lo que DEC-007 prohíbe explícitamente: dibujaba Ensamble 14 vs Calidad 3 (4,7x) cuando la tasa real publicada es 19,6 vs 15,5 ×1.000 (26%). **El gráfico dibujaba la conclusión que el propio análisis descartó.** ✅ **Resuelto (DEC-021):** G11 ahora grafica la tasa ×1.000 por turno, con la noche destacada, leyendo `tablas_soporte/P4_incidentes_por_turno.csv` — tabla que también se persistió por primera vez.
- **G13** sigue sin codificar cobertura ni sucesores — la variable que sostiene el caso del puesto unipersonal. Sigue siendo un scatter de tres puntos con el 85% del lienzo vacío y un eje que dice "24 meses" contra los 12 publicados. **Abierto.**

El hallazgo de seguridad más robusto del proyecto —el 5,4x del turno noche— ya **tiene tabla de soporte persistida** (`P4_incidentes_por_turno.csv`, resuelto junto con G11).

### 3.6 · Una debilidad autodeclarada que ya está resuelta — ✅ Resuelto

`ESTUDIO` §7 declara como hueco abierto que no se corrigió por comparaciones múltiples. **Se corrió y el hallazgo sobrevive:** Mantenimiento Eléctrico, z = 3,28 → p = 0,00104 contra un umbral Bonferroni de 0,005 sobre diez áreas.

Convierte *"la única área que se distingue, aunque no corregimos"* en *"se distingue incluso corrigiendo por haber testeado las diez"*. Es la diferencia entre una afirmación con asterisco y una sin él, delante de quien asigna presupuesto.

---

## 4. Backlog: resumen por bloque

El backlog completo, con problema, impacto de negocio, evidencia y archivos afectados por ítem, está en `auditoria_mejoras_technostamp/06_backlog_priorizado.md`.

| Bloque | Ítems | Contenido |
|---|---:|---|
| **1 · Alto impacto / bajo esfuerzo** | 15 | Arreglo del notebook · regeneración del linaje · retiro del business case obsoleto · celdas de conclusión · títulos como conclusión · README · tabla de incidentes por turno · Bonferroni · corrección de encoding |
| **2 · Alto impacto / esfuerzo medio** | 5 | Paths relativos en 17 scripts · rehacer G11 por turno y en tasa · módulo común de definiciones · marcar scripts superados · declarar y versionar la capa de evidencia |
| **3 · Requiere validación humana** | 4 | Definición de rotación · reformulación del insight de sucesión · rediseño de G14 como rango · jerarquía de las cuatro oportunidades |
| **4 · Secundarias** | 8 | Universo y período en cada gráfico · n por área en G9 · nota de no-causalidad legible · G10 · logs · limpieza de raíz · censura por la derecha · tablas más cortas |

**Distribución por estado:** 20 ítems *lista para implementar ahora* · 12 *requieren criterio o validación humana*.

---

## 5. Nuevos datos y métricas propuestos

Solo los que resuelven una brecha ya documentada por el propio proyecto.

| # | Métrica | Decisión que habilita | Por qué hoy no puede afirmarse |
|---|---|---|---|
| **N1** | Producción promedio de un operario formado (unidades/mes por puesto) | Convierte la rampa del costo por salida de supuesto a medición | El 97% del costo por salida son supuestos propios; el informe §9 ya identifica este dato |
| **N2** | Meses hasta rendimiento pleno de un ingresante | Cierra el segundo supuesto; comprime el rango de 8,4x | "50% durante 3 meses" es juicio: mueve el ahorro entre $49,6M y $132,4M |
| **N3** | Entrevistas de salida estructuradas | Separa "sabemos quién se va" de "sabemos por qué" | El informe §11 lo declara: no hay entrevistas ni encuestas de clima |
| **N4** | Turno del incidente en la ficha de `eventos_rrhh` | Vuelve auditable el hallazgo que sostiene toda la recomendación de seguridad | Hoy se infiere cruzando contra el panel del mes; la cadena no está persistida |
| **N5** | Ficha de investigación obligatoria con causa raíz | Habilita cualquier conclusión defendible sobre seguridad | 55 de ~100 incidentes sin ficha; de los 45 con ficha, 15 con acción correctiva y las 15 con la misma frase |
| **N6** | Auditoría de `meses_desde_ultimo_aumento` en las bajas | Determina si la señal (1,0 vs 4,5 meses) es real o artefacto de registro | Ya marcado en el informe §7 como "señal a investigar, no a concluir" |

---

## 6. Las 5 mejoras con mayor retorno

1. ✅ **Arreglar el corte del notebook.** Una línea de código. Hoy impide que nadie llegue a ver el business case vigente ni los siete gráficos de decisión. — *Resuelto.*
2. **Agregar celdas de conclusión después de cada etapa.** El notebook tiene 1.222 líneas de salida cruda contra 107 de narrativa (11,4:1) y cero celdas de conclusión. El lector infiere lo que el analista ya sabe. — *Pendiente.*
3. ✅ **Reescribir los siete títulos de los gráficos de decisión como conclusión.** El texto ya estaba escrito en las conclusiones ejecutivas. — *Resuelto.*
4. **Eliminar las dos contradicciones de trazabilidad** (`_linaje.json` y `BC_resumen_oportunidades.csv`). Son lo primero que encuentra un auditor. — *Pendiente.*
5. **Crear el README.** Convierte siete carpetas vacías de "trabajo pendiente" en "decisión argumentada de no modelar" — que es lo que realmente son. — *Pendiente.*

---

## 7. Las 3 validaciones humanas más importantes

| # | Decisión que falta | Quién valida | Riesgo que evita |
|---|---|---|---|
| **1** | Cuál es la definición oficial de tasa de rotación de TechnoStamp | **Martina Rosales** | Que el directorio vea 15,0% y 16,7% en la misma slide y descarte el informe entero; y que se dimensione mal la brecha del área priorizada |
| **2** | Si el insight de sucesión se reformula sobre el caso unipersonal observable en vez de sobre `es_posicion_critica` | **Martina Rosales + CEO** | Presentar como cobertura completa del riesgo de sucesión un análisis apoyado en un registro que el propio proyecto documentó como no mantenido (5 personas, 1,4% del padrón, constante en 17 meses) |
| **3** | Qué escenario del business case se presenta como referencia al directorio | **CEO + Directorio** | Que el directorio ancle en $194,8M —la cifra más grande y más especulativa— y luego descubra que el 97% es supuesto propio |

Las tres están registradas como decisiones pendientes en `decisions.md`.

---

## 8. Qué debe preservarse porque ya es sólido

- **La arquitectura notebook-orquestador / scripts-lógica.** Sin duplicación, sin estado oculto entre celdas, con fallo visible en vez de silencioso. Es la mejor decisión estructural del proyecto.
- **`transformaciones.json`**: 31 pasos con parámetros ya calculados, más `regla_general`, `codificacion` y `areas_produccion` como campos explícitos. Es el activo de reproducibilidad.
- **La estructura de `decisions.md`**: decisión · alternativa descartada · por qué se descartó · conclusión · bug evitado. Artefacto poco común y muy defendible.
- **La sección "Qué NO se puede afirmar"** (9 ítems) y la **tabla de afirmaciones retiradas** con el motivo de cada caída, más el **nivel de evidencia declarado por hallazgo**.
- **El business case como rango con piso verificable** (DEC-015) y la cuantificación explícita de que el 97% es supuesto propio.
- **G9** (foco en la única área que se distingue, con margen de error y línea de referencia rotulada), **G8** (hace visible la corrección de DEC-017) y la **nota de no-causalidad de G12**.
- **Los títulos-conclusión de G1–G7** y la **conclusión integradora** del documento ejecutivo: *"no hay un problema generalizado de personas, hay cuatro riesgos focalizados"*.
- **DEC-004, DEC-009, DEC-015, DEC-016 y DEC-017**: cinco decisiones que corrigieron conclusiones contra la intuición.

---

## 9. Conclusión ejecutiva

El análisis de TechnoStamp es riguroso y sus conclusiones se sostienen: la aritmética verifica. Lo que falla es el empaquetado — un notebook que se corta, títulos que no concluyen, dos artefactos obsoletos que contradicen a los vigentes. Arreglos de bajo esfuerzo, alto retorno en credibilidad.

---

## Anexo · Índice de subentregables

| Archivo | Contenido |
|---|---|
| `auditoria_mejoras_technostamp/01_contexto_y_mapa.md` | Contexto recuperado, mapa del flujo, inventario de artefactos, estructura |
| `auditoria_mejoras_technostamp/02_datos_y_rigor.md` | Verificación de cifras, denominadores, incertidumbre, consistencia entre documentos |
| `auditoria_mejoras_technostamp/03_notebook_y_scripts.md` | Legibilidad, duplicación, contratos entre etapas, portabilidad |
| `auditoria_mejoras_technostamp/04_visualizaciones_y_narrativa.md` | Los 14 gráficos, carga cognitiva, foco, tablas, narrativa ejecutiva |
| `auditoria_mejoras_technostamp/05_documentacion_y_trazabilidad.md` | Linaje, versionado, coherencia entre documentos, supuestos declarados |
| `auditoria_mejoras_technostamp/06_backlog_priorizado.md` | Backlog único de 32 ítems, validaciones humanas, nuevos datos y métricas |
