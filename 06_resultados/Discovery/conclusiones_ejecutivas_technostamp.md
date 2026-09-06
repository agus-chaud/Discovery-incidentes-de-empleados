# TechnoStamp — conclusiones ejecutivas

**Audiencia:** Martina Rosales, Head de RR.HH.; CEO y Directorio  
**Período analizado:** enero de 2024 a mayo de 2025; para rotación, período corregido desde febrero de 2024.  
**Propósito:** transformar las planillas existentes en prioridades concretas de negocio.

---

## Conclusión integradora

> **TechnoStamp no enfrenta un problema generalizado de personas: enfrenta cuatro riesgos focalizados —retención, sobrecarga, seguridad nocturna y sucesión— que amenazan costo, continuidad y operación.**

---

## 1. La rotación requiere una intervención focalizada en Mantenimiento Eléctrico

### Gran conclusión
La rotación de TechnoStamp en el período corregido (febrero 2024 – mayo 2025) es **16,7%**. Mantenimiento Eléctrico llega a **34,8%**: es la única área cuya rotación se distingue estadísticamente del promedio disponible. No hay evidencia suficiente para afirmar que las demás áreas roten distinto del promedio.

### Cómo afecta al negocio
La salida de personal técnico deja capacidad sin cubrir y prolonga la vacancia: el tiempo medio de cobertura es de **47 días** y el percentil 90 es de **92 días**. En un área de 46 personas, perder 16 durante el período pone presión sobre la continuidad operativa y obliga a reemplazos reactivos.

### Evidencia

| Indicador | Total compañía | Mantenimiento Eléctrico |
|---|---:|---:|
| Rotación en período limpio | 16,7% | **34,8%** |
| Salidas / personas | 113 / 675 | **16 / 46** |
| Intervalo de confianza 95% | — | **22,7%–49,2%** |
| Veredicto frente al promedio | — | **Peor que el promedio** |

**Visual de soporte:** `visualizaciones/G9_rotacion_area_ic95.png`. Usar el intervalo de confianza para mostrar por qué se prioriza esta área y no se sobrerreacciona sobre las demás.

### Acción correctiva concreta
- Revisar, mediante entrevistas de salida y permanencia, los motivos específicos de las **11 renuncias voluntarias** del área.
- Crear una lista de puestos difíciles de cubrir y aplicar retención selectiva: trayectoria técnica visible, entrenamiento crítico y conversación de permanencia antes de buscar reemplazos.

---

## 2. Las horas extra dejaron de ser una respuesta a picos: ya son un costo estructural

### Gran conclusión
Las horas extra representan **8,3% de la nómina base**: aproximadamente **$987,6M anualizados**. El nivel se mantiene cercano a 10 horas mensuales por persona a lo largo de 17 meses; no responde a un evento puntual. Además, **61 personas** presentan sobrecarga crónica.

### Cómo afecta al negocio
La empresa financia parte de su capacidad operativa con un mecanismo más caro y menos sostenible que una dotación o programación adecuadas. La sobrecarga sostenida también aumenta exposición a ausencias, desgaste y desorganización de turnos, aunque los datos no permiten atribuir causalidad individual.

### Evidencia

| Indicador | Valor |
|---|---:|
| Costo total de horas extra, 17 meses | $1.399,1M |
| Costo anualizado | **$987,6M** |
| Peso sobre nómina base | **8,3%** |
| Horas extra promedio, enero 2024 | 9,86 h/empleado/mes |
| Horas extra promedio, mayo 2025 | 10,21 h/empleado/mes |
| Personas con sobrecarga crónica | **61** |

**Visual de soporte:** `visualizaciones/G10_distribucion_horas_extra_area.png`. Muestra las 11 áreas ordenadas por horas extra, con las dos en los extremos etiquetadas (Pintura y Ingeniería); no convertir diferencias chicas entre las seis áreas del cluster alto en conclusiones causales.

### Acción correctiva concreta
- Separar en cada área prioritaria las horas extra asociadas a demanda real de las asociadas a vacantes, ausencias o mala programación.
- Revisar la asignación de turnos y cobertura de los **61 casos crónicos** para eliminar dependencias individuales antes de normalizar nuevas horas extra.

---

## 3. El turno noche concentra el riesgo de seguridad que más días de operación cuesta

### Gran conclusión
Con la fuente auditable `eventos_rrhh`, el turno noche concentra **25 de 45 incidentes (56%)**. Los **6 incidentes graves** concentran **109 de 138 días perdidos (79%)**: el problema no es solo la frecuencia, sino la severidad y su impacto operativo.

### Cómo afecta al negocio
Cada incidente grave interrumpe la disponibilidad de personal, aumenta costos y expone a TechnoStamp a riesgo operativo y reputacional. La concentración nocturna permite intervenir donde el retorno preventivo puede ser mayor.

### Evidencia

| Indicador | Valor |
|---|---:|
| Incidentes auditables | 45 |
| Incidentes en turno noche | **25 (56%)** |
| Días perdidos totales | 138 |
| Días perdidos por incidentes graves | **109 (79%)** |
| Subtipos con más días perdidos | Caídas: 51; Sobreesfuerzo: 36 |

**Visual de soporte:** `visualizaciones/G11_incidentes_por_turno.png`. Muestra la tasa por 1.000 empleado-mes de cada turno, no el conteo bruto; no usar el conteo del panel mensual porque discrepa de la fuente de eventos.

### Acción correctiva concreta
- Realizar observaciones de tarea y chequeos de inicio de turno específicamente en noche, priorizando prevención de caídas y sobreesfuerzos.
- Analizar individualmente los seis incidentes graves para identificar controles ausentes o fallidos, en lugar de responder con capacitación genérica para toda la compañía.

---

## 4. La sucesión es un riesgo inmediato, no una planificación de largo plazo

### Gran conclusión
**Cuatro de las cinco posiciones críticas activas** llegan a jubilación en un plazo de 12 meses o menos. El caso más expuesto es Supervisor de Logística: una sola persona ocupa el puesto y se jubila en seis meses.

### Cómo afecta al negocio
La pérdida simultánea de conocimiento técnico y liderazgo operativo puede interrumpir decisiones, coordinación y capacidad de respuesta. La vulnerabilidad es especialmente alta cuando no existe una segunda persona con experiencia en el mismo puesto.

### Evidencia

| Puesto crítico en riesgo | Personas en riesgo | Dotación del puesto | Cobertura potencial | Plazo |
|---|---:|---:|---:|---:|
| Supervisor de Logística | **1** | **1** | **0** | 6 meses |
| Team Leader Logística | 2 | 5 | 3 | 9–12 meses |
| Técnico Setup, Estampado | 1 | 25 | 24 | 6 meses |

**Visual de soporte:** `visualizaciones/G13_riesgo_sucesion_por_puesto.png`. Mostrar los puestos y su cobertura, no solo las edades.

### Acción correctiva concreta
- Documentar las decisiones, contactos, rutinas y excepciones operativas que hoy dependen del Supervisor de Logística.
- Asignar formación cruzada y acompañamiento en puesto para cubrir primero el rol unipersonal y, luego, los dos Team Leaders de Logística.

---

## Nota de interpretación financiera

La reducción de renuncias voluntarias tiene una oportunidad estimada de **$23,3M a $194,8M anuales** según escenario; el punto central es **$82,7M**. Es un rango, no un ahorro garantizado: el **97% del costo por salida** depende de supuestos de vacancia y rampa productiva que la empresa aún no mide.

**Visual de soporte:** `visualizaciones/G14_business_case_escenarios.png`. Presentar el rango completo y diferenciar visualmente datos observados de supuestos.
