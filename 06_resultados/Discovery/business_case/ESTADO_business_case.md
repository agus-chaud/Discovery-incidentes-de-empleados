# Estado — Business Case TechnoStamp (Discovery → PowerPoint)

**Archivo de reanudación.** Si la sesión se corta, el próximo chat retoma leyendo este archivo.
Última actualización: 2026-09-07 · Subentregable 0 (preflight) cerrado.

---

## 1. Objetivo

Transformar el análisis de Discovery en documentos Markdown que sostengan un PowerPoint para
Martina Rosales (RR.HH.), CEO y Directorio. El foco es **decisión de negocio**, no metodología.

Entregables previstos, en carpeta `06_resultados/Discovery/business_case/`:

| # | Archivo | Estado |
|---|---|---|
| 0 | `ESTADO_business_case.md` | **Hecho** |
| 1 | `01_matriz_evidencia.md` | **Hecho** |
| 2-4 | `02_guion_ejecutivo.md` (bloque operativo + diagnóstico + anexo financiero) | **Bloque A hecho**; faltan B y C |
| 5 | `03_insights_nuevos.md` | Pendiente |
| 6+ | `04_puente_discovery_automation.md` | Pendiente |

---

## 2. Decisiones ya cerradas (no re-litigar)

1. **Prioridad del caso: seguridad del turno noche.**
2. **Recomendación 90 días: auditoría operativa nocturna focalizada** — dotación, tareas,
   supervisión, fatiga, mantenimiento y relevo entre turnos. Antes de ampliar capacitación general.
3. **Presentación operativa primero:** reducir riesgo y días perdidos. El impacto financiero
   de seguridad va como anexo o como brecha, nunca como titular.
4. **No crear, entrenar ni ejecutar modelos.** Solo evaluar el puente Discovery → Automation.
5. **No inventar brechas, causalidades ni ahorros garantizados.**

Decisiones heredadas que gobiernan las cifras: DEC-004 (fuente auditable de incidentes),
DEC-006 (índice propio de criticidad), DEC-007 (tasas, no conteos), DEC-015 (ahorro en rango),
DEC-016 (margen de error en toda comparación), DEC-017 (excluir enero 2024),
DEC-019 (rotación oficial = 16,7% acumulada del período), DEC-020 (Bonferroni),
DEC-021 (G11 por turno y tasa).

Criterio de veredicto Discovery → Automation: `ESTUDIO_conceptos_technostamp.md` §1 —
frecuencia de decisión, escala, y si el cuello de botella es velocidad de scoring o calidad
de inferencia. ML solo si la decisión se toma muchas veces, rápido y a escala no revisable
por una persona.

---

## 3. Fuentes verificadas en este preflight

Leídas y contrastadas contra los outputs, no contra la narrativa:

- `ESTUDIO_conceptos_technostamp.md` (§1, §5, §6, §7, §8, §9, §10)
- `decisions.md` (DEC-004, 006, 007, 015, 016, 017, 018, 019, 020, 021 + decisiones abiertas)
- `04_scripts/06_p3_p4_p5.py`, `07_verif_incidentes_p5.py`, `13_limpieza_v2.py`,
  `17_business_case_v2.py`, `18_visualizaciones_decision.py`
- `06_backlog_priorizado.md` (N1–N6 completos)
- `conclusiones_ejecutivas_technostamp.md`
- Tablas de soporte: `P4_incidentes_por_turno.csv`, `P5_rotacion_por_area_con_IC.csv`,
  `P3_horas_extra_por_area.csv`, `P3_sobrecargados_cronicos.csv`, `P1_riesgo_sucesion_por_puesto.csv`,
  `P6_training_seguridad_vs_incidentes.csv`, `BC_rango_retencion.csv`, `BC_supuestos.json`
- Parquets: `eventos_limpio.parquet`, `panel_mensual_limpio.parquet` (consulta directa)

### Cifras confirmadas contra output, listas para citar

| Cifra | Valor verificado | Fuente |
|---|---|---|
| Rotación limpia de la compañía | **16,7%** (113 salidas / 675 personas expuestas) | `17_business_case_v2.py`, DEC-019 |
| Rotación Mantenimiento Eléctrico | **34,8%** (16/46), IC95 22,7–49,2, z=3,28, p=0,00105 | `P5_rotacion_por_area_con_IC.csv` |
| Umbral Bonferroni | 0,05 / 10 áreas = 0,005 → **se sostiene** | ídem, columna `sig_bonferroni` |
| Áreas que se distinguen del promedio | **1 de 10** | ídem |
| Arrastre de enero 2024 | 19 salidas, las 19 con 1 solo mes observado | DEC-017 |
| Efecto de excluir el arrastre | 19,0% → 16,7% | DEC-017 (actualización 2026-09-06) |
| Tasa de incidentes turno Noche | **11,8 cada 1.000 empleado-mes** | `P4_incidentes_por_turno.csv` |
| Tasa Mañana / Tarde | 2,2 cada 1.000 empleado-mes → **5,4x** | ídem |
| Tasa Administrativo / Rotativo | 3,8 / 2,3 | ídem |
| Incidentes en Noche | **25 de 45 (56%)** | `eventos_limpio.parquet` |
| Días perdidos en Noche | **102 de 138 (74%)** | ídem |
| Incidentes graves | 6 casos, **109 de 138 días perdidos**, $600.000 | ídem |
| Graves en turno Noche | **5 de 6** | ídem |
| Exposición Noche | 2.124 empleado-mes (comparable a Mañana 2.254 y Tarde 2.256) | `P4_incidentes_por_turno.csv` |
| Horas extra: áreas sobre 11 h/mes | 6 (Mant. Eléctrico 12,1 · Pintura 11,9 · Logística 11,5 · Estampado 11,3 · Ensamble 11,1 · Mant. Mecánico 11,1) | `P3_horas_extra_por_area.csv` |
| Horas extra: áreas bajo 6 h/mes | 5 (Ingeniería 3,6 · Administración 4,1 · Calidad 5,2 · RRHH 4,3 · Dirección 5,5) | ídem |
| HE como % de nómina base | 3,0% (Ingeniería) a 10,3% (Mant. Eléctrico) | ídem |
| Sobrecargados crónicos (≥70% de sus meses sobre p80) | **49 activos** en el CSV persistido | `P3_sobrecargados_cronicos.csv` |
| Sucesión: puestos en riesgo persistidos | **1 fila** — Supervisor de Logística, dotación 1, 0 sucesores | `P1_riesgo_sucesion_por_puesto.csv` |
| Criticidad por índice propio | 47 empleados activos (8,4%), score ≥ 2 | DEC-006, `13_limpieza_v2.py` |
| Business case retención — piso | **$23.298.312/año** (conservador, −15%) | `BC_supuestos.json` |
| Business case — punto central | **$82.732.125/año** (central, −25%) | ídem |
| Business case — techo | **$194.840.088/año** (agresivo, −40%) | ídem |
| Piso solo con dato duro del cliente | **$1.642.500/año** | ídem |
| Renuncias voluntarias anualizadas | 55/año | ídem |
| % del costo por salida que es supuesto propio | 97% ($5,68M de $5,88M) | DEC-015 |

---

## 4. Hallazgo nuevo del preflight — límite real de la evidencia de seguridad

**Verificado ejecutando sobre `eventos_limpio.parquet`, no inferido.**

1. `eventos_limpio.parquet` **sí tiene** la columna `turno_evento`, poblada en los 45 incidentes.
   El backlog N4 afirma que "no tiene columna de turno": **esa afirmación es incorrecta**.
2. Pero `turno_evento` coincide con el `turno_trabajo` del panel en **45 de 45 casos**. Coincidencia
   perfecta. Es el turno asignado a la persona, no un dato levantado del incidente.
3. `hora_evento` de los 25 incidentes rotulados "Noche" va de las **06:53 a las 22:00**. Ningún
   incidente del dataset ocurre entre las 23:00 y las 06:00. El rango horario global es 6–22 h.

**Qué significa.** El hallazgo sigue en pie y sigue siendo el más fuerte del proyecto: *la gente
asignada al turno noche tiene 5,4 veces la tasa de incidentes de mañana o tarde, con exposición
comparable*. Eso es una propiedad de esa población y de cómo se la opera — dotación, supervisión,
relevo, mantenimiento — y es exactamente lo que justifica una auditoría operativa.

**Qué NO puede afirmarse.** Que los accidentes ocurran de madrugada, ni que la causa sea la
oscuridad, el horario o el sueño. Los datos no lo muestran. El campo `hora_evento` contradice esa
lectura. Toda hipótesis de fatiga circadiana queda como hipótesis a investigar, nunca como evidencia.

Este punto refuerza —no debilita— la recomendación de auditoría: hay una diferencia real y grande,
y ningún dato disponible que explique por qué. Eso es precisamente lo que se va a buscar al piso.

---

## 5. Contradicciones internas detectadas, a resolver en los subentregables

| # | Contradicción | Dónde | Cómo se resolverá |
|---|---|---|---|
| C1 | El insight ejecutivo 4 (sucesión) publica una tabla de **3 puestos** ("4 de 5 posiciones críticas") construida sobre `es_posicion_critica`, que DEC-006 declaró no utilizable. El único output persistido tiene **1 fila** | `conclusiones_ejecutivas_technostamp.md` §4 vs `P1_riesgo_sucesion_por_puesto.csv` | Subentregable 3/4: reemplazar por tarjeta de alerta sobre el caso unipersonal verificable (Supervisor de Logística). Coincide con la decisión abierta de `decisions.md` línea 17 |
| C2 | G12 titula "se entrena después del accidente, no antes". El script agrega totales de todo el período; **no hay ninguna comparación temporal** entre fecha de capacitación y fecha de incidente | `18_visualizaciones_decision.py` (G12) | Subentregable 4: reformular como brecha de medición preventiva. Nunca como orden causal |
| C3 | DEC-009 menciona 61 sobrecargados crónicos; el CSV persistido tiene 49 filas (el filtro se aplica sobre activos) | `decisions.md` DEC-009 vs `P3_sobrecargados_cronicos.csv` | Subentregable 1: citar 49 con universo explícito ("activos"), o no citar el número |
| C4 | Backlog N4 afirma que falta la columna de turno en `eventos_rrhh`. La columna existe | `06_backlog_priorizado.md` N4 | Subentregable 5: reescribir la brecha real — el turno está, pero es el turno *asignado*, no el turno *del hecho*; y `hora_evento` no lo respalda |
| C5 | El título de G10 cita "Pintura: 12,2 h" (mediana del boxplot) mientras la tabla reporta 11,9 (media) | `18_visualizaciones_decision.py` vs `P3_horas_extra_por_area.csv` | Subentregable 3: citar una sola de las dos, con su definición al lado |
| C6 | `BC_resumen_oportunidades.csv` publica "Rotacion voluntaria: $92,4M esperado", que es la cifra única descartada por DEC-015 | `BC_resumen_oportunidades.csv` | Subentregable 4: usar solo el rango de `BC_supuestos.json`. Marcar el CSV como superado |

---

## 6. Subentregables terminados

- [x] **0 — Preflight.** Fuentes leídas, cifras verificadas contra output, contradicciones listadas.
- [x] **1 — Matriz de evidencia** → `01_matriz_evidencia.md`. Siete temas cubiertos con las seis
      columnas pedidas. Hallazgo adicional verificado al escribirla: la correlación área a área
      entre horas de capacitación en seguridad y tasa de incidentes es **r = 0,394, p = 0,260**
      (n = 10 áreas; sin Logística, r = 0,279). **No se distingue de cero.** El título actual de
      G12 —"Más capacitación coincide con más incidentes"— sobreafirma incluso el patrón
      descriptivo, además del problema de temporalidad ya registrado como C2. Confirma la decisión
      de reformular G12 como brecha de medición preventiva.
      También verificado: el costo anual total de horas extra suma **$987,6M**, consistente con
      los "$988M" de DEC-009.

- [x] **2 — Guion ejecutivo, bloque operativo (A)** → `02_guion_ejecutivo.md`, secciones A.1 a A.7.
      Titular, impacto en días de operación, evidencia G11, límite de la evidencia declarado en la
      slide, auditoría de 90 días sobre seis ejes, cinco hipótesis con criterio de confirmación y
      descarte, y métricas de resultado y de proceso con línea de base.
      Cifras nuevas verificadas al escribirlo:
      · dotación nocturna ~125 personas/mes, **151 distintas** en el período (Estampado 51,
        Ensamble 40, Pintura 24, Mant. Mecánico 12, Logística 11, Mant. Eléctrico 9, Calidad 4);
      · los 5 graves nocturnos explican **84 de los 102 días** perdidos de ese turno;
      · subtipos noche vs resto: quemadura **5 vs 1**, caída 5 vs 3, corte 4 vs 2, atrapamiento
        2 vs 5. La noche está peor en casi toda la tabla → no es una máquina ni una tarea única;
      · antigüedad del accidentado más nuevo: **14 meses**; mediana **79 meses**. Ningún incidente
        en el primer año de nadie;
      · costo registrado de los 45 incidentes: **$975.000** total. No usar como impacto: cubre la
        atención del hecho, no los 138 días de producción;
      · tasa promedio de compañía: **4,7** ×1.000 empleado-mes (45 / 9.601). La noche está 2,5x
        por encima del promedio y 5,4x por encima de mañana o tarde.

---

## 7. Próximo subentregable

**Subentregable 3 — Guion ejecutivo, diagnóstico organizacional** → agregar bloque B a
`02_guion_ejecutivo.md`.

Cuatro apartados, cada uno con: pregunta · evidencia · decisión habilitada · límite de la
evidencia · métrica de seguimiento.

- **G8** — enero es arrastre del corte, no una crisis del período. La rotación es plana.
- **G9** — Mantenimiento Eléctrico es la única diferencia de rotación que se sostiene (Bonferroni).
- **G10** — horas extra como capacidad concentrada, no problema homogéneo. Resolver antes la
  contradicción C5 (11,9 media vs 12,2 mediana en Pintura): citar una sola, con su definición.
- **G13 → tarjeta de alerta de sucesión**, no scatter, porque el output persistido tiene un solo
  caso (Supervisor de Logística). Resolver C1: no repetir "4 de 5 posiciones críticas", que se
  apoya en el flag descartado por DEC-006.

---

## 8. Afirmaciones que requieren evidencia adicional (no publicar sin cerrar)

| Afirmación | Por qué no se sostiene hoy | Qué la cerraría |
|---|---|---|
| "Los accidentes ocurren de noche por fatiga u oscuridad" | `hora_evento` va de 6 a 22 h; ningún incidente de madrugada | Hora real del hecho, validada contra el parte de turno |
| "La capacitación se dicta después del accidente" | Ninguna comparación de fechas en el código | Cruce fecha de training vs fecha de incidente por empleado |
| "Cuatro de cinco posiciones críticas se jubilan en 12 meses" | Construida sobre `es_posicion_critica`, descartado por DEC-006 | Recalcular sobre el índice propio y persistir la tabla |
| "Las horas extra causan accidentes" | DEC-009: vínculo no concluyente | Diseño con temporalidad, no correlación por decil |
| "Reducir rotación ahorra $82,7M" | 97% del costo por salida es supuesto propio (DEC-015) | N1 (producción de operario formado) + N2 (meses hasta rendimiento pleno) |
| "Los top performers rotan más" | DEC-016: los IC se solapan, retirada | Más período o más casos |
| "Estampado rota mal" | DEC-016: su IC contiene al promedio | ídem |
| Toda tasa de rotación del proyecto | Censura por la derecha sin tratar (ESTUDIO §7) | Análisis de supervivencia, si el período se extiende |
