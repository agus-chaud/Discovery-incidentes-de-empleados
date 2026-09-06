# 05 · Documentación y trazabilidad

**Auditoría integral TechnoStamp — subentregable 5 de 6**
**Pregunta que guía esta sección:** si mañana un auditor externo, el cliente o un entrevistador abre este repositorio sin hablar con nadie, ¿puede entender qué se hizo, verificarlo y reejecutarlo?

---

## 1. Hallazgo principal: el archivo de linaje describe un pipeline que ya no existe

Dentro de `06_resultados/Discovery/datos_transformados/` conviven dos archivos de procedencia:

| Archivo | Generado | Script que declara | Estado |
|---|---|---|---|
| `_linaje.json` | **2026-09-03 21:29** | **`04_scripts/03_limpieza.py`** | **Obsoleto** |
| `transformaciones.json` | 2026-09-05 12:09 | `04_scripts/13_limpieza_v2.py` | Vigente |

Los cuatro parquet que están en esa misma carpeta tienen fecha **2026-09-05 12:09**: los produjo `13_limpieza_v2.py`.

**`_linaje.json` atribuye esos datos a un script que no los generó.** Su contenido no es falso —los conteos que reporta (694 empleados, 132 salidas, 562 activos) coinciden con la realidad—, pero su **procedencia sí lo es**: apunta al script superado, con una fecha 39 horas anterior a los datos que dice describir.

Por qué esto es más grave que los otros hallazgos de documentación:

- DEC-001 —la primera decisión del proyecto— se sostiene textualmente sobre este archivo: *"Toda transformación se persiste aparte […] con un `_linaje.json` que registra origen, encoding, lista de transformaciones y propósito."*
- El `Discovery_report.md` §2 lo cita como la prueba del principio de raw inmutable.
- Es uno de los **dos únicos archivos de la capa de datos que están versionados en git** (ver §3), es decir, es literalmente lo que un tercero ve del linaje del proyecto.

Un auditor que compare ambos archivos encuentra dos scripts distintos declarados como origen del mismo dataset. En un proyecto cuyo argumento central es la trazabilidad, es la contradicción que más caro sale.

**Recomendación (lista para implementar):** regenerar `_linaje.json` desde `13_limpieza_v2.py` o consolidar ambos en un solo archivo. No cambia ningún dato ni conclusión.

---

## 2. `transformaciones.json` es el mejor artefacto de trazabilidad del proyecto. Preservar.

31 pasos con sus parámetros ya calculados, no la instrucción que los calcula:

| Operación | Pasos |
|---|---:|
| `politica_vacios` | 13 |
| `a_fecha` | 8 |
| `unificar_categorias` | 3 |
| `regla_coherencia` | 3 |
| `renombrar_columna` | 2 |
| `a_entero_con_vacios` | 1 |
| `politica_outliers` | 1 |

Además declara `regla_general`, `codificacion` y `areas_produccion` como campos explícitos — es decir, las decisiones de universo y política están **en el dato**, no solo en la prosa del informe.

Esto es exactamente lo que DEC-014 se propuso y funciona. Cuando TechnoStamp mande los próximos seis meses, esto es reejecutable. **Es el activo de reproducibilidad del proyecto y no hay que tocarlo.**

---

## 3. El repositorio no permite verificar nada: contiene la receta, no los ingredientes

`.gitignore` excluye `*.csv`, `*.parquet`, `*.xlsx` y `datos/`. Resultado, sobre 41 archivos versionados:

| Capa | Versionado |
|---|---|
| Scripts (18) | ✅ |
| Notebook | ✅ |
| Informes, `decisions.md`, `ESTUDIO`, 14 PNG | ✅ |
| `_linaje.json` + `transformaciones.json` | ✅ |
| **CSV originales (3)** | ❌ |
| **Parquet limpios (4)** | ❌ |
| **17 tablas de soporte + `BC_supuestos.json`** | ❌ |
| **`politica_vacios.csv`** | ❌ |

Excluir datos de personal identificable es una decisión defendible y probablemente correcta. **El problema es que no está declarada en ningún lado**, y su consecuencia sí importa: la capa de evidencia auditable —las 17 tablas que sostienen cada cifra del informe— no viaja con el proyecto.

Combinado con los paths absolutos de 17 de 18 scripts (subentregable 03 §4), el resultado neto es que **nadie fuera de esta máquina puede reproducir ni verificar una sola cifra**. Para un entregable cuya sección 13 se titula "Reproducibilidad", es la brecha más grande entre lo declarado y lo verificable.

**Recomendación (requiere criterio):** documentar la exclusión como decisión (`DEC-0xx: los datos de personal no se versionan`) y versionar las tablas de soporte agregadas, que no contienen datos identificables salvo `P3_cronicos_detalle.csv` y `P3_sobrecargados_cronicos.csv`. Con eso el informe pasa a ser verificable sin exponer nóminas.

---

## 4. No hay puerta de entrada al proyecto

En la raíz del repositorio hay dos archivos Markdown: `decisions.md` y `ESTUDIO_conceptos_technostamp.md`. **No hay README.**

Quien abra el repositorio hoy tiene que adivinar:

- que el punto de partida es `03_notebooks/Technostamp_Completo.ipynb`;
- que el entregable de negocio es `06_resultados/Discovery/conclusiones_ejecutivas_technostamp.md`;
- que el informe técnico es `06_resultados/Discovery/Discovery_report.md`;
- que `03_limpieza.py` y `09_business_case.py` están superados;
- que las carpetas `05_modelos/` y `07_despliegue/` están vacías **a propósito**, porque el proyecto decidió no construir un modelo (`ESTUDIO` §1) — hoy parecen trabajo pendiente.

Ese último punto es el más costoso: la decisión de **no** modelar es una de las mejores del proyecto y está bien argumentada en el `ESTUDIO`, pero la estructura de carpetas comunica exactamente lo contrario.

**Recomendación (lista para implementar):** un `README.md` de una pantalla con: qué es el proyecto, para quién, dónde empezar a leer según el rol (directorio / RR.HH. / técnico), cuál es el orden de ejecución real, qué está superado y por qué hay carpetas vacías. Es la mejora de menor esfuerzo y mayor impacto en "simple de entender".

---

## 5. Coherencia entre documentos

Se cruzaron los cuatro documentos narrativos. Estado:

| Par de documentos | Coherencia | Excepciones |
|---|---|---|
| `Discovery_report.md` ↔ `conclusiones_ejecutivas_technostamp.md` | Alta | Rotación 15,0% vs 16,7% (subentregable 02 §2); jerarquía de oportunidades presente en el técnico y ausente en el ejecutivo (subentregable 04 §4) |
| `Discovery_report.md` ↔ `decisions.md` | Alta | DEC-009 con 19,0% vs 16,4% del informe (subentregable 02 §5) |
| `decisions.md` ↔ `ESTUDIO_conceptos_technostamp.md` | Alta | El `ESTUDIO` declara Bonferroni como hueco abierto cuando el hallazgo lo sobrevive (subentregable 02 §6) |
| `decisions.md` (DEC-006) ↔ insight ejecutivo 4 | **Contradicción** | El insight usa como universo el flag que DEC-006 declaró no utilizable como insumo analítico, sin declarar la limitación (subentregable 02 §4) |
| `Discovery_report.md` §13 ↔ estado real del repo | **Desactualizado** | 18 scripts vs "01…14"; 14 PNG vs "G1–G7"; 17 CSV vs "12 CSV"; orden de ejecución omite 12, 15, 16, 17, 18 |

**Lectura de conjunto:** la coherencia narrativa es buena. Lo que falla es el **mantenimiento**: la documentación describe el estado del proyecto al 3 de septiembre, y el proyecto siguió avanzando hasta el 5. Cada mejora (limpieza v2, business case v2, gráficos de decisión, conclusiones ejecutivas) sumó artefactos sin actualizar los documentos que los indexan.

---

## 6. Calidad de la documentación de supuestos

Este es el punto más fuerte del proyecto y conviene decirlo con precisión, porque es lo que lo diferencia de un análisis promedio.

| Práctica | Dónde | Estado |
|---|---|---|
| Alternativa descartada + por qué, en cada decisión | `decisions.md`, 17 entradas | **Excelente. Preservar.** |
| "Bug evitado" nombrado explícitamente | DEC-001, DEC-004, DEC-005, DEC-009 | **Excelente. Preservar.** |
| Supuestos del business case con su razón en la misma estructura de datos | `BC_supuestos.json` + `17_business_case_v2.py` | **Excelente. Preservar.** |
| Separación dato duro / supuesto propio, cuantificada (97%) | DEC-015, informe §9 | **Excelente. Preservar.** |
| Sección "Qué NO se puede afirmar" (9 ítems) | informe §11 | **Excelente. Preservar.** |
| Tabla de "afirmaciones retiradas" con el motivo de cada caída | informe §11 | **Poco común y muy defendible. Preservar.** |
| Nivel de evidencia declarado por hallazgo (descriptivo / estimado / exploratorio / no concluyente) | informe, cada sección | **Excelente. Preservar.** |
| Decisiones pendientes de validación del cliente | `decisions.md`, ahora 6 entradas | **Bien. Mantener actualizado.** |

**Ninguna de estas prácticas debe tocarse en el marco de "simplificar el proyecto".** Son lo que hace que el informe resista una lectura crítica.

---

## 7. Riesgo de mantenimiento de los propios documentos

Dos señales de que el sistema documental empezó a degradarse:

1. **Corrupción de acentos en las dos secciones escritas más recientemente** (`decisions.md` DEC-018 y `ESTUDIO` §9): 34 y 48 tokens con `?` literal. No es un problema de visualización — los bytes son UTF-8 válido y no hay ningún carácter de reemplazo: el texto se escribió ya degradado y la información se perdió. Es especialmente visible porque el resto de ambos archivos está impecable. **Recomendación: reescribir esas dos secciones asegurando escritura UTF-8.**
2. **El entregable ejecutivo no está versionado.** `conclusiones_ejecutivas_technostamp.md` figura como archivo sin seguimiento en git, junto con el notebook modificado y siete PNG modificados. El documento que va al directorio es el único que no tiene historial.

---

## 8. Resumen de este subentregable

| # | Hallazgo | Estado propuesto |
|---|---|---|
| 1 | `_linaje.json` atribuye los datos al script superado `03_limpieza.py` | Lista para implementar |
| 2 | La capa de evidencia (17 tablas + parquet + CSV) no está versionada, y la exclusión no está declarada | Requiere criterio |
| 3 | No hay README: ni punto de entrada, ni orden real, ni explicación de las carpetas vacías | Lista para implementar |
| 4 | `Discovery_report.md` §13 describe el repositorio al 3 de septiembre | Lista para implementar |
| 5 | Contradicción DEC-006 ↔ insight ejecutivo 4 | **Requiere validación humana** |
| 6 | Corrupción de acentos en DEC-018 y `ESTUDIO` §9 | Lista para implementar |
| 7 | El entregable ejecutivo sin versionar | Lista para implementar |

**Preservar sin cambios:** `transformaciones.json` (31 pasos reejecutables), la estructura de `decisions.md` con alternativa descartada y bug evitado, `BC_supuestos.json`, la sección "Qué NO se puede afirmar", la tabla de afirmaciones retiradas y el nivel de evidencia declarado por hallazgo.

---

## Próximo subentregable

`06_backlog_priorizado.md` — backlog único ordenado por impacto/esfuerzo, con validaciones humanas y propuestas de nuevos datos y métricas.
