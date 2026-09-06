# 03 · Notebook y scripts

**Auditoría integral TechnoStamp — subentregable 3 de 6**
**Foco:** legibilidad, duplicación, complejidad innecesaria y experiencia de lectura. Lo técnico se evalúa solo donde afecta credibilidad, trazabilidad o reproducibilidad.

---

## 1. La arquitectura es correcta y hay que defenderla

El notebook orquesta, no calcula. `ejecutar_etapa()` corre cada script como proceso independiente con `subprocess` + `runpy`, captura `stdout`/`stderr` y `mostrar_graficos()` renderiza los PNG inline porque los scripts usan backend `Agg`.

Esto resuelve bien tres problemas que suelen arruinar un notebook de consultoría:

- **Sin duplicación de lógica.** No hay una versión del cálculo en el notebook y otra en el script.
- **Sin estado oculto entre celdas.** Cada etapa arranca en un proceso limpio; no hay variables que sobrevivan de una celda anterior y cambien un resultado.
- **Sin resultados silenciosamente rotos.** `check=False` + `raise` explícito hace que un fallo se vea, en vez de mostrar la salida parcial y seguir.

`18_visualizaciones_decision.py` además resuelve la raíz del proyecto con `Path(__file__).resolve().parents[1]`. **El patrón correcto ya existe adentro del repositorio.**

---

## 2. Hallazgo principal: el notebook se rompe por un contrato entre scripts, no por un bug suelto

La causa raíz del fallo de la celda 24:

| | |
|---|---|
| `12_diagnostico_gaps.py` línea 23 | usa la columna `scrap_prom` |
| `13_limpieza_v2.py` (limpieza vigente) | la llama `scrap_prom_produccion` |
| `03_limpieza.py` (limpieza superada) | la llamaba `scrap_prom` |

`12_diagnostico_gaps.py` fue escrito contra la salida de la limpieza v1 y **nunca se actualizó cuando v2 la reemplazó**. No es un descuido de tipeo: es un contrato de datos roto entre dos etapas del pipeline, sin ningún mecanismo que lo detecte antes de la ejecución.

**Alcance verificado:** revisé las 102 columnas de los cuatro parquet contra las referencias de los 18 scripts. **Éste es el único contrato roto.** Los demás scripts vigentes leen columnas que existen. No hay un problema sistémico — hay un script huérfano de la migración v1 → v2.

**Consecuencia de negocio:** el lector que sigue la instrucción del propio notebook ("ejecutá las celdas de arriba hacia abajo") se detiene en la etapa 11 de 16. Nunca ve el EDA sistemático, el diagnóstico de fragilidad, la rotación temporal corregida, el business case vigente ni los siete gráficos de decisión G8–G14. Todo lo que sostiene el informe ejecutivo queda del otro lado de la excepción.

**Recomendación (lista para implementar):** alinear el nombre de columna en `12_diagnostico_gaps.py`. Esfuerzo mínimo, no cambia ninguna cifra publicada — el script es de autodiagnóstico y no alimenta ninguna tabla de soporte ni gráfico.

---

## 3. Hallazgo de lectura: el notebook tiene 11 líneas de salida cruda por cada línea de explicación

| Métrica | Valor |
|---|---:|
| Líneas de `stdout` guardadas en el notebook | **1.222** |
| Líneas de markdown (narrativa) | 107 |
| **Ratio salida cruda / narrativa** | **11,4 : 1** |
| Celdas de conclusión después de una etapa | **0** |

Las etapas más pesadas concentran el problema: `06_p3_p4_p5` imprime **205 líneas**, `07_verif_incidentes_p5` imprime **169**, `01_perfilado` imprime **94**.

Y el patrón estructural es siempre el mismo: *markdown de introducción → celda de código → 200 líneas de tablas de consola → markdown de introducción de la etapa siguiente.* **Ninguna etapa cierra con una conclusión.** El lector recibe la evidencia y tiene que inferir por su cuenta qué acaba de pasar.

Esto contradice el estándar que el propio proyecto se fijó en `ESTUDIO_conceptos_technostamp.md` §9: *"un gráfico no es un insight"*. Vale igual para una tabla de consola: 205 líneas de `stdout` no son un hallazgo.

**Recomendación (lista para implementar):** agregar una celda markdown de 2–3 líneas **después** de cada etapa con el titular de lo que esa etapa demostró. No requiere tocar ningún cálculo, no cambia ninguna conclusión, y convierte el notebook de "registro de ejecución" en "documento que se puede leer". Es la mejora de menor esfuerzo y mayor retorno de todo el proyecto.

**Recomendación complementaria (requiere criterio):** para las tres etapas más ruidosas, mover el detalle a un archivo de log y dejar en el notebook solo el bloque de resumen. No es urgente y se puede posponer.

---

## 4. Reproducibilidad: 17 de 18 scripts no corren fuera de esta máquina

Cada script tiene la raíz escrita a mano:

```python
D = Path(r"C:\Users\Dell\Agus\Nivii AI\06_resultados\Discovery\datos_transformados")
```

`18_visualizaciones_decision.py` es el único que hace lo correcto:

```python
ROOT = Path(__file__).resolve().parents[1]
```

Para un entregable que declara reproducibilidad como principio (DEC-001, DEC-014, sección 13 del informe), esto es la contradicción más cara del proyecto: la receta de limpieza de 31 pasos es reejecutable, pero el script que la ejecuta solo arranca en `C:\Users\Dell\`.

**Recomendación (lista para implementar):** propagar el patrón de `18` a los otros 17 scripts. Es mecánico, no cambia ninguna salida y elimina la objeción más obvia que puede hacer un cliente o un entrevistador.

---

## 5. Legibilidad: qué cuesta entender el proyecto hoy

### 5.1 La numeración miente sobre el orden

Orden real de ejecución:

```
01 → 02 → 13 → 04 → 05 → 06 → 07 → 08 → 10 → 11 → 12 → 14 → 15 → 16 → 17 → 18
```

Un lector nuevo asume que `03` va después de `02` y que `09` va después de `08`. Los dos están superados. Para descubrirlo hay que leer el notebook o `decisions.md`.

### 5.2 Dos versiones superadas siguen en disco sin marcar

`03_limpieza.py` y `09_business_case.py` están vigentes en la carpeta. No hay sufijo, comentario en el encabezado ni carpeta `_superado/`. El riesgo no es hipotético: la salida superada de `09` (`BC_resumen_oportunidades.csv`) sigue en `tablas_soporte/` contradiciendo el rango vigente (ver subentregable 02, §3).

### 5.3 La regla de negocio "sobrecarga crónica" está definida tres veces

`06_p3_p4_p5.py`, `10_sensibilidad_he.py` y `11_verif_cronicos_seguridad.py` cada uno recalcula:

```
umbral = p80 de horas_extra   ·   >=70% de los meses por encima   ·   >=6 meses observados
```

Hoy las tres coinciden (61 personas, verificado). Pero es la definición que sostiene un hallazgo publicado, escrita en tres lugares: cambiarla en dos de tres produce una divergencia silenciosa, sin error ni aviso.

**Recomendación (requiere criterio):** un módulo `04_scripts/_comun.py` con la raíz del proyecto, la carga de los parquet y las definiciones de negocio compartidas (sobrecarga crónica, período limpio, fuente canónica de incidentes). Reduce ~110 líneas de repetición y, más importante, deja una sola definición por concepto de negocio.

### 5.4 Un número publicado no lo produce ningún script

El `Discovery_report.md` §5 publica: *"Rotan 19,7% contra 16,4% del resto"*.

`10_sensibilidad_he.py` —el único script que calcula esa comparación— imprime **19,7% vs 19,0%**, porque usa `u.salio.mean()` sobre los 17 meses completos, sin aplicar el período limpio de DEC-017. El 16,4% del informe es el valor correcto (lo reproduje: 101/614 en el período limpio), pero **no sale de ninguna salida persistida**.

Es un número correcto sin fuente reproducible. Es exactamente el tipo de cosa que un directorio no detecta y un auditor sí.

**Recomendación (lista para implementar):** aplicar el período limpio dentro de `10_sensibilidad_he.py` para que la salida del script coincida con lo publicado, y actualizar la cifra de DEC-009.

---

## 6. Inconsistencias menores de texto

| Dónde | Dice | Es |
|---|---|---|
| Notebook, celda de cierre | "Se ejecutaron las 15 etapas vigentes" | 16 etapas en `ETAPAS_EJECUTADAS` |
| `Discovery_report.md` §13 | "Scripts del pipeline `01…14`" | 18 scripts |
| `Discovery_report.md` §13 | "Visualizaciones (G1–G7)" | 14 PNG (G1–G14) |
| `Discovery_report.md` §13 | "Tablas de soporte (12 CSV)" | 17 CSV + 1 JSON |
| `Discovery_report.md` §13, orden de ejecución | omite `12`, `15`, `16`, `17`, `18` | están en el notebook |

Ninguna cambia una conclusión. Todas juntas dan la impresión de que la documentación va detrás del código — que es justamente lo que un cliente evalúa cuando decide si confiar en el pipeline para los próximos seis meses de datos.

---

## 7. Lo que ya está bien y hay que preservar

- **Notebook orquestador sin lógica propia.** Es la decisión estructural más valiosa. No tocarla.
- **Proceso independiente por etapa.** Elimina el estado oculto entre celdas, el defecto clásico de los notebooks.
- **Fallo visible en vez de silencioso.** El `raise` de `ejecutar_etapa` es correcto: el problema es el script roto, no el mecanismo que lo denuncia.
- **Umbrales declarados, no escondidos.** `14_eda_sistematico.py` define `U_VACIO`, `U_CONSTANTE`, `U_RARA` arriba y con comentario. Es el patrón que deberían seguir los demás.
- **Encoding explícito en toda lectura y escritura.** Ningún script usa `open()` o `read_csv()` sin declarar `encoding`. Las 17 tablas de soporte y el `BC_supuestos.json` están en UTF-8 limpio. Verificado.
- **Escenarios de negocio como diccionario con su razón escrita al lado** (`17_business_case_v2.py`): cada supuesto lleva el texto que lo justifica en la misma estructura de datos. Es lo que permite publicar el rango de DEC-015 sin perder la trazabilidad del supuesto.

---

## 8. Resumen de este subentregable

| # | Hallazgo | Estado propuesto |
|---|---|---|
| 1 | El notebook se corta en la etapa 11/16 por contrato roto v1→v2 (`scrap_prom`) | Lista para implementar |
| 2 | 11,4 líneas de salida cruda por línea de narrativa; cero celdas de conclusión | Lista para implementar |
| 3 | 17 de 18 scripts con path absoluto; el patrón correcto ya existe en el repo | Lista para implementar |
| 4 | El 16,4% publicado no lo produce ningún script | Lista para implementar |
| 5 | Definición de sobrecarga crónica duplicada en 3 scripts | Requiere criterio (refactor) |
| 6 | `03` y `09` superados sin marcar; numeración que no refleja el orden | Requiere criterio (renombrar afecta la documentación) |
| 7 | Cinco inconsistencias de texto entre documentación y estado real | Lista para implementar |

---

## Próximo subentregable

`04_visualizaciones_y_narrativa.md` — calidad de los 14 gráficos, carga cognitiva, foco, escalas, y si cada visual responde las cuatro preguntas de negocio.
