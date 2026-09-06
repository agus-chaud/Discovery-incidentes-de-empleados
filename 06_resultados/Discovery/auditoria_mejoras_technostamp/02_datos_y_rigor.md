# 02 · Datos y rigor

**Auditoría integral TechnoStamp — subentregable 2 de 6**
**Método:** se recalcularon las cifras publicadas contra `datos_transformados/*.parquet` y `tablas_soporte/*.csv`. Todo lo que sigue es verificación, no reinterpretación.

---

## 1. Cifras ejecutivas verificadas y correctas

Se reprodujeron desde los datos limpios. Ninguna necesita corrección.

| Cifra publicada | Recalculado | Estado |
|---|---|---|
| Horas extra anualizadas $987,6M | $987,6M | ✅ |
| Horas extra = 8,3% de la nómina base | 8,31% | ✅ |
| Costo total HE 17 meses $1.399,1M | $1.399,1M | ✅ |
| 45 incidentes auditables | 45 | ✅ |
| 6 incidentes graves = 109 de 138 días perdidos (79%) | 6 → 109/138 | ✅ |
| Tiempo medio de cobertura 47 días · p90 92 días | 47,2 · 91,6 (n=90) | ✅ |
| Mantenimiento Eléctrico: 46 personas, 16 salidas, 34,8% | 46 · 16 · 34,8% | ✅ |
| 11 renuncias voluntarias en Mantenimiento Eléctrico | 11 (+3 despidos, +2 reestructuración) | ✅ |
| 113 salidas en el período limpio · 73 voluntarias · 55/año | 113 · 73 · 54,8 | ✅ |
| Sucesión: 4 de las 5 posiciones críticas activas se jubilan ≤12 meses | 4 de 5, todas con `es_posicion_critica = True` | ✅ (con una salvedad, ver §4) |
| 61 personas con sobrecarga crónica | 61 | ✅ |
| Rango de retención $23,3M – $194,8M · central $82,7M | idéntico a `BC_rango_retencion.csv` | ✅ |

**Conclusión de esta sección:** la aritmética del proyecto es sólida. Los problemas que siguen son de *definición*, *consistencia entre documentos* y *trazabilidad* — no de cálculo.

---

## 2. Hallazgo principal: hay tres tasas de rotación anual defendibles y el informe usa dos sin distinguirlas

Los tres cálculos salen de los mismos 113 casos:

| Definición | Fórmula | Resultado |
|---|---|---|
| **A. Salidas anualizadas sobre dotación activa promedio** | (113 / 16 × 12) / 563,4 | **15,04%** |
| **B. Tasa acumulada del período limpio** | 113 / 675 personas expuestas | **16,74%** |
| **C. Tasa del período anualizada** | 16,74% × 12/16 | **12,56%** |

El `Discovery_report.md` y las conclusiones ejecutivas publican **A (15,0%)** como titular y **B (16,7%)** como promedio de comparación entre áreas. El problema aparece dentro de un mismo insight:

> Insight 1 · titular: *"La rotación anual corregida de TechnoStamp es **15,0%**"*
> Insight 1 · tabla de evidencia, dos párrafos más abajo: *"Rotación en período limpio — Total compañía **16,7%** · Mantenimiento Eléctrico **34,8%**"*

Un directorio lee dos tasas de rotación de la misma empresa en la misma slide y no tiene forma de saber que son la misma realidad medida con distinto denominador.

**Y hay un efecto de segundo orden más serio:** el 34,8% de Mantenimiento Eléctrico está calculado con la lógica **B** (16 salidas / 46 personas expuestas). Comparar 34,8% contra el titular de 15,0% mezcla denominadores e **infla la brecha percibida**: contra el 16,7% correcto, el área rota 2,08 veces el promedio; contra el 15,0%, parece 2,32 veces. La tabla de evidencia hace la comparación correcta; el titular instala el ancla equivocada.

**Recomendación:** elegir una definición, escribirla una vez debajo del titular (*"salidas anualizadas sobre dotación activa promedio, febrero 2024 – mayo 2025"*) y usar el mismo denominador en toda comparación entre grupos. No es un error de cálculo: es un riesgo de credibilidad que se resuelve con una línea de texto.

---

## 3. Dos business cases contradictorios conviven en la misma carpeta

`tablas_soporte/` contiene dos tablas que responden la misma pregunta con números distintos:

| Archivo | Oportunidad de retención | Fecha |
|---|---|---|
| `BC_resumen_oportunidades.csv` | $55,4M / **$92,4M** / $147,8M | 4 de septiembre |
| `BC_rango_retencion.csv` | $23,3M / **$82,7M** / $194,8M | 5 de septiembre |

`BC_resumen_oportunidades.csv` es la salida de `09_business_case.py`, superado por `17_business_case_v2.py` (DEC-015). Nada en el nombre del archivo, ni en la carpeta, ni en el informe lo indica. La fila de horas extra de ese archivo sí sigue vigente, lo que lo vuelve más engañoso todavía: es un archivo *parcialmente* correcto.

Esto es exactamente el riesgo que DEC-015 quiso evitar. Si el directorio abre la carpeta de soporte, encuentra dos cifras centrales de ahorro que difieren en $10M y un rango que difiere en ambos extremos.

**Recomendación:** mover las salidas superadas a `tablas_soporte/_superado/` o eliminarlas, y dejar un `README.md` de una línea por tabla vigente. Es de esfuerzo bajo y elimina la peor contradicción del proyecto.

---

## 4. El insight de sucesión se apoya justamente en el flag que DEC-006 declaró inutilizable

**El dato es correcto:** los 4 empleados que se jubilan en ≤12 meses tienen `es_posicion_critica = True`, sobre 5 posiciones críticas activas.

```
1547  Logística  Supervisor de Logística   64 años   6 meses   dotación 1   sucesores 0
1098  Estampado  Técnico Setup             64 años   6 meses   dotación 25  sucesores 24
1544  Logística  Team Leader Logística     63 años   9 meses   dotación 5   sucesores 3
1542  Logística  Team Leader Logística     62 años  12 meses   dotación 5   sucesores 3
```

**El problema es de coherencia interna.** DEC-006 concluye textualmente:

> *"El flag `es_posicion_critica` se reporta al cliente como brecha de calidad, no se usa como insumo analítico. […] Nunca presentar un resultado basado en un flag sin mantener sin declarar esa limitación."*

El insight ejecutivo 4 se titula *"Cuatro de las cinco posiciones críticas activas llegan a jubilación"* — es decir, usa el flag como insumo analítico y como universo, sin declarar la limitación. Además el `Discovery_report.md` §3 responde la pregunta de Martina con "cuatro personas" y en la misma sección explica que el flag marca solo el 1,4% del padrón y no se mantiene.

**Por qué importa para el negocio:** el titular tiene doble lectura. *"Cuatro de cinco posiciones críticas se jubilan"* suena a que el 80% del riesgo crítico se va — cuando lo que en verdad dice el dato es *"el registro de posiciones críticas del sistema tiene 5 personas y no sirve para planificar"*. El hallazgo accionable y honesto es el que ya está en el informe pero no en el titular: **un puesto unipersonal sin backup se va en 6 meses.**

**Recomendación:** reformular el titular alrededor del caso unipersonal (que es puro dato observable: dotación 1, sucesores 0) y mover "4 de 5 críticos" a evidencia con la salvedad de cobertura del flag. Requiere validación humana porque cambia el mensaje ejecutivo.

**Traceabilidad menor asociada:** la columna de `P1_riesgo_sucesion_por_puesto.csv` se llama `en_riesgo_24m` mientras que el horizonte publicado es 12 meses. En este dataset ambos horizontes dan los mismos 4 casos, así que no cambia el número — pero un lector del CSV concluye lo contrario de lo que dice el informe.

---

## 5. DEC-017 se aplicó al titular pero no se retro-aplicó a DEC-009

La comparación de rotación entre sobrecargados crónicos y el resto aparece con dos bases distintas:

| Fuente | Crónicos | Resto | Período usado |
|---|---|---|---|
| `decisions.md` DEC-009 | 19,7% | **19,0%** | 17 meses (incluye enero 2024) |
| `Discovery_report.md` §5 | 19,7% | **16,4%** | 16 meses (período limpio) |

Ambos números se reproducen exactamente desde los datos. No hay error de cálculo: **DEC-009 quedó escrito antes de DEC-017 y nunca se recalculó.** La versión correcta es la del período limpio (16,4%), porque DEC-017 estableció que enero es arrastre del corte de archivo, no rotación del período.

El efecto práctico es que el registro de decisiones subestima la brecha (0,7 puntos en vez de 3,3) en la decisión que justifica descartar el business case de horas extra. La conclusión de DEC-009 **no cambia** — con 61 personas los intervalos siguen solapando y la diferencia sigue sin ser demostrable (z = 0,64) — pero un lector que compare ambos documentos encuentra dos cifras y no sabe cuál rige.

**Recomendación:** recalcular la cifra de DEC-009 con el período limpio y anotar en la propia entrada que se actualizó por DEC-017. Es esfuerzo bajo y no cambia ninguna conclusión.

---

## 6. Una debilidad autodeclarada que en realidad ya está resuelta

`ESTUDIO_conceptos_technostamp.md` §7 declara como hueco abierto:

> *"No hubo corrección por comparaciones múltiples. […] el análisis nunca corrió la corrección (por ejemplo, Bonferroni) que permitiría decirlo con la misma confianza."*

Se corrió. Con los z que ya publica `P5_rotacion_por_area_con_IC.csv`:

| Prueba | z | p bilateral | Umbral Bonferroni (10 áreas) | Veredicto |
|---|---:|---:|---:|---|
| **Mantenimiento Eléctrico** | 3,28 | **0,00104** | 0,0050 | **Sobrevive** |
| Estampado | 1,19 | 0,234 | 0,0050 | No, como ya se reportó |
| Top performers | 1,51 | 0,131 | — | No, como ya se reportó |

El hallazgo que sostiene la prioridad #1 del proyecto **resiste la corrección más estricta**: p = 0,00104 contra un umbral de 0,005, y z = 3,28 contra un z crítico de 2,81.

Esto no es un hallazgo nuevo, es evidencia adicional para un hallazgo existente. Y tiene valor de negocio directo: convierte *"la única área que se distingue, aunque no corregimos por múltiples pruebas"* en *"la única área que se distingue, y se distingue incluso corrigiendo por haber testeado las diez"*. Es la diferencia entre una afirmación con asterisco y una sin él, delante de un directorio que va a asignar presupuesto.

**Recomendación:** agregar la columna `p_bonferroni` a `P5_rotacion_por_area_con_IC.csv` y una línea en el informe. Esfuerzo bajo, no cambia ninguna conclusión, cierra una debilidad que el propio proyecto declaró.

---

## 7. Trazabilidad: el hallazgo de seguridad más robusto no tiene tabla de soporte

`tablas_soporte/` tiene `P4_tasa_incidentes_por_area.csv`, `P4_incidentes_por_antiguedad.csv` y `P4_incidentes_antiguedad_fuente_eventos.csv`. **No existe ninguna tabla de incidentes por turno.**

Sin embargo, el turno noche es:
- el hallazgo de seguridad que el informe califica de *robusto* ("aparece en ambas fuentes de datos");
- el que sostiene la Ficha C y la oportunidad #3 de la matriz;
- el titular completo del insight ejecutivo 3.

Además, `eventos_limpio.parquet` no tiene columna de turno: el cruce se hace contra el panel dentro del script y el resultado solo existe en `stdout`. Si alguien quiere verificar el 5,4x sin reejecutar el pipeline, no puede.

**Recomendación:** persistir `P4_incidentes_por_turno.csv` con incidentes, empleado-mes de exposición, tasa ×1.000 y días perdidos. Esfuerzo bajo, impacto alto en credibilidad.

---

## 8. Límites metodológicos correctamente declarados que siguen abiertos

Estos no son defectos: están declarados y se listan para el backlog.

| Límite | Dónde está declarado | Estado |
|---|---|---|
| Censura por la derecha no tratada (activos ≠ "se quedan para siempre") | ESTUDIO §7 | Abierto. Con 16 meses el impacto es acotado, pero conviene nombrarlo en el informe técnico, no solo en el material de estudio. |
| 97% del costo por salida son supuestos | DEC-015, informe §9 | Abierto y bien gestionado (rango + piso verificable + qué dato lo cerraría). **Preservar.** |
| Dotación informada 450 vs 562 observados | `decisions.md` pendientes | Abierto — **decisión del cliente**, bloquea la definición del universo. |
| `meses_desde_ultimo_aumento` anómalo en bajas (1,0 vs 4,5) | `decisions.md` pendientes, informe §7 | Abierto — bien marcado como "señal a investigar, no a concluir". **Preservar.** |
| Ninguna causalidad afirmada | informe §11 | Cumplido en todo el informe técnico. **Preservar.** |

---

## 9. Resumen de este subentregable

| # | Hallazgo | Tipo | Cambia conclusiones |
|---|---|---|---|
| 1 | Tres tasas de rotación defendibles; dos publicadas sin distinguir denominador | Claridad / credibilidad | No, pero cambia cómo se lee |
| 2 | `BC_resumen_oportunidades.csv` obsoleto contradice el rango vigente | Contradicción de datos | No, si se retira |
| 3 | El insight de sucesión usa el flag que DEC-006 declaró inutilizable | Coherencia interna | **Sí — requiere validación humana** |
| 4 | DEC-009 no se recalculó tras DEC-017 (19,0% vs 16,4%) | Consistencia | No |
| 5 | Bonferroni no corrido, pero el hallazgo lo sobrevive (p = 0,00104) | Rigor — refuerza | No, refuerza |
| 6 | No hay tabla de soporte de incidentes por turno | Trazabilidad | No |
| 7 | `en_riesgo_24m` con horizonte publicado de 12 meses | Trazabilidad | No |

---

## Próximo subentregable

`03_notebook_y_scripts.md` — legibilidad, duplicación, complejidad innecesaria y experiencia de lectura del notebook y de `04_scripts/`.
