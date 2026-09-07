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
| 2-4 | `02_guion_ejecutivo.md` (bloques A, B y C) | **Hecho — completo** |
| 5 | `03_insights_nuevos.md` | **Hecho** |
| 6+ | `04_puente_discovery_automation.md` | **Entregas 6, 7 y 8 hechas** (I2, I10, I4, I6, I12, I8); falta la 9 |

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

- [x] **3 — Guion ejecutivo, diagnóstico organizacional (bloque B)** → `02_guion_ejecutivo.md`,
      secciones B.1 a B.4. Cada una con pregunta · titular · evidencia · decisión habilitada ·
      límite de la evidencia · métrica de seguimiento con línea de base.
      · **B.1 (G8)** rotación plana, arrastre de enero, 19,0% → 16,7%.
      · **B.2 (G9)** Mantenimiento Eléctrico, tabla completa de las diez áreas con IC95 y Bonferroni.
      · **B.3 (G10)** horas extra como corte limpio en dos grupos.
      · **B.4** tarjeta de alerta de sucesión, reemplaza el scatter G13.
      Contradicciones resueltas en este subentregable: **C1** (no se repite "4 de 5 posiciones
      críticas"; se corrige explícitamente en B.4 citando DEC-006) y **C5** (G10 es boxplot, así
      que todo B.3 cita **medianas**, con la media al lado en la misma tabla).
      Hallazgos nuevos verificados al escribirlo:
      · Medianas de HE por área: el corte es 11,2 h de un lado y 6,1 del otro, sin zona gris.
      · **Mantenimiento Eléctrico es la única área donde la media (12,1) supera a la mediana
        (11,3)** — cola larga, unas pocas personas acumulan mucho más que sus pares. Es la misma
        área con peor rotación. Se presenta como coincidencia a mirar, nunca como causa.
      · Crónicos por área: Estampado 13, Pintura 12, Ensamble 11, Logística 6, Calidad 3,
        Mant. Eléctrico 2, Mant. Mecánico 2. Total 49 sobre 562 activos.
      · **Candidato verificado y DESCARTADO:** sobrecarga crónica por turno — Noche 15,4% (19/123)
        vs Mañana 11,5% (16/139) vs Tarde 9,0% (12/134). **z = 1,48, no se distingue del azar.**
        Queda registrado en B.3 para que nadie lo presente después como hallazgo.
      · Serie mensual limpia: se mueve entre 0,5% y 3,0% sin dirección; picos aislados en marzo
        2024 (17 salidas), diciembre 2024 (14) y abril 2025 (15).

- [x] **4 — Guion ejecutivo, anexo financiero y selección visual (bloque C)** →
      `02_guion_ejecutivo.md`, secciones C.1 a C.4. El guion queda **completo** (656 líneas).
      · **C.1** las tres tasas de rotación posibles y por qué la oficial es 16,7% (DEC-019).
      · **C.2** business case en rango: tabla 3×3 de escenarios, piso $23,3M, centro $82,7M, techo
        $194,8M, amplitud 8,4x, piso verificable $1,64M, los dos supuestos explícitos y N1+N2.
      · **C.3** selección visual documentada: mostrar / reformular / reemplazar / fuera.
      · **C.4** las cuatro brechas de dato que se devuelven al cliente, priorizadas.
      Contradicción resuelta: **C6** — `BC_resumen_oportunidades.csv` queda marcado como superado
      dentro del propio guion; la fuente vigente es `BC_supuestos.json`.
      Cifras nuevas verificadas al escribirlo:
      · Descomposición exacta del costo por salida central ($6.044.356): dato duro **$200.000** +
        vacancia **$2.991.905** (47,2 días de time-to-fill × $1.901.634 de salario medio del
        saliente) + rampa **$2.852.451** (3 meses al 50%). El dato duro es el **3,3%**.
      · `meses_desde_ultimo_aumento`: **1,0 en renuncias voluntarias (n=89) vs 4,5 en activos
        (n=562)**. Confirma el patrón contraintuitivo que motiva la brecha N6.
      · Amplitud del rango: 194.840.088 / 23.298.312 = **8,4x**.
      · Renuncias voluntarias anualizadas exactas: **54,75** (se cita como ≈55).

- [x] **5 — Lista formal de insights nuevos** → `03_insights_nuevos.md`. Tres secciones:
      preguntas iniciales respondidas (P1–P5) · **doce insights nuevos** con las nueve columnas
      pedidas · seis brechas de medición priorizadas.
      Insights numerados I1 a I12, todos con fuente verificable. Además:
      · Se documenta el candidato **verificado y descartado** (sobrecarga crónica por turno,
        z = 1,48) para que no reaparezca como hallazgo.
      · Se documentan las **dos debilidades que el proyecto declara sobre sí mismo**: censura por
        la derecha sin tratar, y costo real del accidente no medido.
      · Se desarma el "~14 incidentes/año evitables" del informe técnico: es aritmética de brecha
        contra la tasa de mañana/tarde (14,3/año); contra el promedio de compañía da **10,6/año**.
        Ninguna es una promesa; si se usa, va etiquetada como brecha.
      **Veredicto preliminar de los doce: ninguno justifica Automation hoy.** El desarrollo del
      porqué, insight por insight, va en el subentregable 6+.

- [x] **6 — Puente Discovery → Automation, entrega 6 (I2 + I10)** →
      `04_puente_discovery_automation.md`. Se tratan juntos porque son las dos mitades de la misma
      pregunta: quién se va y cuánto cuesta. Es donde la tentación de modelar es máxima.
      **Ambos veredictos: `ninguno — sigue siendo Discovery recurrente`**, por motivos distintos:
      · **I2** no se modela por **escala** y por **cuello de botella**. Cifras nuevas verificadas:
        694 personas, 132 salidas, **89 renuncias voluntarias** (la clase positiva real), **11** en
        Mantenimiento Eléctrico, contra **60 columnas candidatas** en el panel. 89 positivos vs 60
        variables no es un problema de algoritmo: el fenómeno ocurrió 89 veces. Y la etiqueta está
        mal definida por censura a derecha. Lo que falta saber es *por qué*, no *quién*.
      · **I10** no se modela porque **el problema no es de inferencia, es de medición**. Faltan dos
        cantidades que nadie registró (N1, N2). Un modelo entrenado sobre estos datos devolvería
        nuestros propios supuestos con apariencia de resultado.
      Ambos cierran con el **umbral** escrito: qué tendría que cambiar para que el veredicto fuera
      sí. Otras cifras verificadas: 52 puestos distintos, **90 contrataciones** en el período,
      motivos de salida (89 renuncia voluntaria · 27 despido · 7 jubilación · 5 reestructuración ·
      4 fin de contrato).

- [x] **7 — Puente Discovery → Automation, entrega 7 (I4 + I6)** →
      `04_puente_discovery_automation.md`. El segundo candidato a modelo predictivo.
      **Ambos veredictos: `ninguno — sigue siendo Discovery recurrente`.**
      Dos hallazgos previos verificados en esta entrega, y **los dos obligaron a corregir
      documentos ya escritos**:
      · **V1 — `severidad` es una recodificación de `dias_perdidos`.** Cero solapamiento:
        Leve = **0 días los treinta casos**, Moderado = 1–5, Grave = 8–25. Un corte así de limpio
        no sale de dos personas clasificando a criterio: la etiqueta se deriva del número.
        Consecuencia: "predecir severidad" y "predecir días perdidos" son el mismo problema, y un
        modelo de severidad que use días perdidos como entrada es fuga de la variable objetivo.
      · **V2 — la concentración de gravedad en el turno noche NO se distingue del azar.**
        Graves 5 vs 1 → Fisher exacto bilateral **p = 0,205**. Incidentes con días perdidos
        10 vs 5 → **p = 0,352**. Los **leves se reparten 15 y 15**, idénticos.
        El "5 de 6" es un conteo real y se puede decir; afirmar que la gravedad se concentra en la
        noche es una generalización que con seis casos no se sostiene.
      Cifras nuevas verificadas: 45 incidentes en **41 personas distintas**, solo **3 reincidentes**
      · tasa base **0,47%** por empleado-mes (45 / 9.601) · **6,1%** de las personas tuvo al menos
      un incidente · ~2,8 incidentes por mes, máximo 6 · solo **15 de 45** incidentes tienen algún
      día perdido.
      El veredicto de I4 suma dos razones que no son estadísticas: **la acción correctiva no es
      individual** (dotación, supervisión y relevo se ejecutan sobre el turno, no sobre personas), y
      un score de riesgo por operario desplazaría la responsabilidad de las condiciones a la
      persona. También se anticipa y responde la objeción "balanceá las clases".

### Correcciones aplicadas a documentos ya entregados (por V2)

| Archivo | Qué decía | Qué dice ahora |
|---|---|---|
| `02_guion_ejecutivo.md` §A.2 | "El riesgo severo es casi exclusivamente nocturno" | Conteo observado, no patrón demostrado; Fisher p = 0,205 |
| `02_guion_ejecutivo.md` §A.4 | — | Nueva subsección "Y un segundo límite, sobre la gravedad", con los dos tests y cómo decirlo en la slide |
| `02_guion_ejecutivo.md` §A.7 | Métrica "casos graves, turno noche" | Se sigue como **conteo**, no como tasa: con seis casos no hay base para una tasa de gravedad por turno |
| `01_matriz_evidencia.md` fila 4 | — | Se agrega a "qué no se puede afirmar": ni que la gravedad se concentre en la noche |

- [x] **8 — Puente Discovery → Automation, entrega 8 (I12 + I8)** →
      `04_puente_discovery_automation.md`. Los dos casos donde **el dato existe pero faltaba la
      interpretación**. Ninguno necesitaba un dato nuevo: necesitaba que alguien corriera el cruce.
      **Ambos veredictos: `ninguno`.** Y los dos **cerraron una brecha del backlog**.

      · **I12 — N6 queda RESUELTA, y el insight se cae.** `meses_desde_ultimo_aumento` es un
        **artefacto de registro**, no una señal de fuga. La prueba: el campo abierto por motivo de
        salida repite el mismo perfil en los cinco motivos — renuncia 1,03 · despido 0,96 ·
        **jubilación 1,43** · reestructuración 1,40 · fin de contrato 0,50 — y
        **ninguna de las 132 bajas supera el valor 3**, contra **183 de 562 activos** que sí lo
        superan (activos: media 4,53, mediana 2,0, máx 17 = el largo del panel).
        Nadie se jubila porque le dieron un aumento hace un mes. El campo se reescribe o se trunca
        al registrar la baja, para todos los motivos por igual.
        **Consecuencia operativa: el campo queda PROHIBIDO** como variable de rotación. Es el tipo
        de variable que un modelo encontraría "muy predictiva" y que estaría prediciendo el acto de
        registrar la baja, no la decisión de irse.

      · **I8 — el cruce temporal sí se podía correr, y refuta el titular de G12.** Sobre los 45
        incidentes: **5 con capacitación de seguridad previa · 4 con posterior · 36 (80%) con
        ninguna**. Los 4 "posteriores" recibieron el curso a una **mediana de 108 días** (máx 344):
        calendario normal, no reacción. A nivel persona: accidentados **22,0%** (9 de 41) vs no
        accidentados **19,1%** (121 de 634), Fisher **p = 0,683**. Cobertura del universo: **19,3%**
        (130 de 675). Insumos: 145 capacitaciones de Seguridad sobre 133 empleados, con
        `fecha_inicio`/`fecha_fin`.
        **El hallazgo real es mejor que el anterior:** la capacitación cubre al 19,3% y se asigna
        sin ninguna relación con quién se lastima. Y el cuello de botella no es medir, es **diseño**:
        la asignación no fue aleatoria ni está documentada, así que capacitados y no capacitados no
        son comparables. Lo que corresponde es una **evaluación de impacto**, no un modelo.

### Correcciones aplicadas a documentos ya entregados (por la entrega 8)

| Archivo | Qué decía | Qué dice ahora |
|---|---|---|
| `03_insights_nuevos.md` I12 | "Señal de fuga temprana sin validar" | Artefacto de registro confirmado; variable prohibida |
| `03_insights_nuevos.md` I8 | "Nadie mide si la capacitación previene algo" | Tres mediciones independientes, incluido el cruce temporal |
| `03_insights_nuevos.md` I6 | — | Se agrega el caveat de gravedad por turno (Fisher p = 0,205) |
| `03_insights_nuevos.md` §3 | N6 en prioridad 3 | **N6 tachada como resuelta**, con el motivo |
| `04_puente...` entrega 6, I2 | N6 como "la señal más discriminante del dataset" | Tachado y corregido: es un artefacto y una variable prohibida |
| `02_guion_ejecutivo.md` §C.3 | Titular de G12: "no sabemos si previene, porque nadie lo mide" | "La capacitación cubre al 19,3% y no llega a quien se accidenta", con el cruce completo |
| `01_matriz_evidencia.md` fila 5 | "No hay ninguna comparación de fechas" | El cruce se corrió; el titular anterior de G12 queda refutado |

---

## 7. Próximo subentregable — **último**

**Entrega 9 del puente Discovery → Automation** → agregar a `04_puente_discovery_automation.md` y
**cerrar el documento**: **I3**, **I11**, **I5**, **I7**, **I9** e **I1**.

Son los seis que quedan, y ninguno es un candidato serio a modelo — son decisiones de gestión o
arreglos de captura. Se pueden tratar más breve que los anteriores, pero con el mismo formato de
cuatro apartados y con el umbral escrito.

| Insight | Naturaleza | Nota para el tratamiento |
|---|---|---|
| **I3** | Horas extra: decisión de capacidad | Ya resuelto económicamente por DEC-009. El "no" es casi trivial |
| **I11** | Cola larga de HE en Mant. Eléctrico | Es un diagnóstico interno de un área de 46 personas |
| **I5** | Turno asignado ≠ turno del hecho | Arreglo de captura, no proyecto |
| **I7** | El riesgo sube con la experiencia | Hipótesis: asignación de tareas de riesgo a veteranos. Falta la tarea del hecho |
| **I9** | Sucesión unipersonal | Un caso. No hay patrón que modelar |
| **I1** | Arrastre de enero | Regla de higiene de datos |

**Cierre del documento a escribir en esa entrega:** una tabla resumen de los doce veredictos, y la
conclusión transversal — ninguno falla por falta de técnica; fallan por escala, por falta del dato
que explicaría el fenómeno, o porque el problema no era de inferencia. Más las dos lecciones
transferibles que ya aparecieron: **(a)** cuando una variable separa demasiado bien, la primera
pregunta es cuándo se escribe ese dato; **(b)** antes de pedirle un dato al cliente, agotar lo que
ya está en la mesa — dos de las seis brechas del backlog eran análisis pendientes, no datos
faltantes.

### Formato fijo por insight (ya aplicado en la entrega 6)

Para cada uno, cuatro apartados:

1. **Tipo de proyecto posible** — una sola opción: `supervisado` · `no supervisado` ·
   `ninguno — sigue siendo Discovery`. Si supervisado: variable objetivo y anticipación necesaria.
   Si no supervisado: patrón buscado y decisión que habilitaría.
2. **Datos faltantes** — conectados únicamente con brechas reales ya identificadas (N1–N6, o las
   verificadas en el preflight). No inventar.
3. **Veredicto explícito** aplicando `ESTUDIO_conceptos_technostamp.md` §1: frecuencia de decisión,
   escala, y si el cuello de botella es velocidad de scoring o calidad de inferencia. Concluir sin
   ambigüedad: `sí justifica Automation` o `ninguno — sigue siendo Discovery recurrente`.
4. **Mapa ds-*** solo si se justifica (`ds-06-transformar-datos`, `ds-07-seleccionar-variables`,
   `ds-08-balancear-clases` si corresponde, `ds-09-modelizar`). Si no, escribir textualmente:
   *"No pasar a ds-06 todavía; sostener como análisis recurrente de Discovery y mejorar la captura
   de datos."*

**Orden sugerido de tratamiento** (los más discutibles primero, porque son donde la tentación de
modelar es mayor):

| Entrega | Insights | Por qué juntos |
|---|---|---|
| 6 | **I2** (rotación en Mant. Eléctrico) + **I10** (costo de la rotación) | Es el candidato obvio a "modelo de churn". Hay que responderlo bien y de frente |
| 7 | **I4** (seguridad nocturna) + **I6** (concentración de la gravedad) | El segundo candidato a modelo predictivo. n=45 y n=6 son la respuesta |
| 8 | **I12** (señal de fuga temprana) + **I8** (eficacia preventiva de capacitación) | Los dos casos donde el dato existe pero no se sabe qué significa |
| 9 | **I3** (horas extra), **I11** (cola larga) y **I5/I7/I9/I1** | Cierre: los que son decisiones de gestión o arreglos de captura |

**Escribir además el umbral, no solo el "no".** Para cada veredicto negativo, dejar dicho qué
tendría que cambiar —volumen, frecuencia de decisión, o naturaleza del cuello de botella— para que
la respuesta pasara a ser sí. Un "no" sin umbral no es un veredicto, es una opinión.

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
