# Revisión sistemática de variables — TechnoStamp

Revisión columna por columna de las tres tablas. No parte de ninguna pregunta de negocio: recorre todo el dataset buscando problemas que nadie sospecha.

**Umbrales usados:** vacíos > 20% · valor dominante ≥ 99% · etiqueta rara < 1%

## Tabla `empleados_mensual`

9,733 filas × 60 columnas

| Tipo de variable | Columnas |
|---|---|
| numerica continua | 23 |
| booleana | 11 |
| categorica | 8 |
| numerica discreta | 8 |
| fecha | 5 |
| alta cardinalidad | 5 |

### Alertas

| Columna | Tipo | Alerta | Detalle |
|---|---|---|---|
| `nombre` | alta cardinalidad | **ALTA CARDINALIDAD** | 596 valores distintos |
| `fecha_salida` | fecha | **VACÍOS** | 98.6% sin dato |
| `motivo_salida` | categorica | **VACÍOS** | 98.6% sin dato |
| `area` | categorica | **ETIQUETAS RARAS** | 1 etiquetas bajo el 1% |
| `subarea` | categorica | **ETIQUETAS RARAS** | 6 etiquetas bajo el 1% |
| `puesto` | alta cardinalidad | **ALTA CARDINALIDAD** | 52 valores distintos |
| `nivel_jerarquico` | numerica discreta | **MUY ASIMÉTRICA** | asimetría 2.8 — cola larga |
| `manager_nombre` | alta cardinalidad | **ALTA CARDINALIDAD** | 110 valores distintos |
| `span_of_control` | numerica discreta | **MUY ASIMÉTRICA** | asimetría 3.0 — cola larga |
| `tasa_scrap_porcentaje` | numerica continua | **VACÍOS** | 38.9% sin dato |
| `tasa_scrap_porcentaje` | numerica continua | **MUY ASIMÉTRICA** | asimetría 2.4 — cola larga |
| `dias_perdidos_scrap` | numerica continua | **MUY ASIMÉTRICA** | asimetría 2.8 — cola larga |
| `salario_base_mensual` | numerica continua | **MUY ASIMÉTRICA** | asimetría 5.0 — cola larga |
| `bonus_anual` | numerica continua | **VACÍOS** | 94.7% sin dato |
| `bonus_anual` | numerica continua | **MUY ASIMÉTRICA** | asimetría 2.3 — cola larga |
| `meses_desde_ultimo_aumento` | numerica discreta | **MUY ASIMÉTRICA** | asimetría 2.4 — cola larga |
| `dias_licencia_medica` | numerica discreta | **MUY ASIMÉTRICA** | asimetría 8.3 — cola larga |
| `incidentes_seguridad_count` | numerica discreta | **MUY ASIMÉTRICA** | asimetría 10.0 — cola larga |
| `horas_training_mes` | numerica continua | **MUY ASIMÉTRICA** | asimetría 5.3 — cola larga |
| `horas_training_acumulado_anio` | numerica continua | **MUY ASIMÉTRICA** | asimetría 2.3 — cola larga |
| `ultimo_training_fecha` | fecha | **VACÍOS** | 65.4% sin dato |
| `dias_time_to_fill` | numerica continua | **VACÍOS** | 77.0% sin dato |
| `dias_time_to_fill` | numerica continua | **MUY ASIMÉTRICA** | asimetría 2.4 — cola larga |
| `fuente_reclutamiento` | categorica | **VACÍOS** | 77.0% sin dato |
| `fuente_reclutamiento` | categorica | **ETIQUETAS RARAS** | 2 etiquetas bajo el 1% |
| `apellido` | alta cardinalidad | **ALTA CARDINALIDAD** | 177 valores distintos |
| `nombre_completo` | alta cardinalidad | **ALTA CARDINALIDAD** | 687 valores distintos |
| `flag_edad_inconsistente` | booleana | **CASI CONSTANTE** | 'False' ocupa el 99.5% |
| `flag_snapshot_pre_ingreso` | booleana | **CASI CONSTANTE** | 'False' ocupa el 99.3% |
| `costo_total_mes` | numerica continua | **MUY ASIMÉTRICA** | asimetría 4.8 — cola larga |
| `jubila_12m` | booleana | **CASI CONSTANTE** | 'False' ocupa el 99.8% |
| `jubila_24m` | booleana | **CASI CONSTANTE** | 'False' ocupa el 99.3% |

### Variables numéricas

|                               |    n |            media |          mediana |           desvío |              mín |              máx |
|:------------------------------|-----:|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|
| empleado_id                   | 9733 |   1327.11        |   1330           |    186.985       |   1000           |   1693           |
| edad                          | 9733 |     35.9176      |     35           |      7.78866     |     22           |     64           |
| antiguedad_meses              | 9733 |     74.3038      |     71           |     41.9917      |      0           |    185           |
| nivel_jerarquico              | 9733 |      1.24494     |      1           |      0.586537    |      1           |      5           |
| manager_id                    | 9611 |   1336.58        |   1359           |    152.803       |   1001           |   1603           |
| span_of_control               | 9733 |      0.9326      |      0           |      2.43265     |      0           |     18           |
| meses_hasta_jubilacion        | 9733 |    343.879       |    359           |     93.7208      |      6           |    516           |
| anios_en_puesto_actual        | 9733 |      6.16742     |      5.9         |      3.49957     |      0           |     15.3         |
| rating_performance            | 9733 |      3.22398     |      3           |      0.923932    |      1           |      5           |
| unidades_producidas           | 7801 |    981.672       |    991           |     71.2843      |    701           |   1130           |
| tasa_scrap_porcentaje         | 5943 |      2.29892     |      1.76        |      1.35059     |      0.7         |     14.1         |
| eficiencia_vs_target          | 7801 |     99.2776      |     99.74        |      9.31041     |     65.06        |    116.56        |
| dias_perdidos_scrap           | 9523 |      0.262711    |      0           |      0.548068    |      0           |      6           |
| salario_base_mensual          | 9733 |      1.75584e+06 |      1.58023e+06 | 603525           |      1.25175e+06 |      9.80607e+06 |
| horas_extra                   | 9733 |     10.0955      |     10.5         |      4.70959     |      0           |     33.4         |
| costo_horas_extra             | 9733 | 146129           | 147056           |  73025.4         |      0           | 723926           |
| bonus_anual                   |  518 |      2.0913e+06  |      1.94e+06    |      1.12866e+06 | 641207           |      1.08799e+07 |
| ultimo_aumento_porcentaje     | 9218 |      3.74033     |      0           |      4.30508     |      0           |     12           |
| meses_desde_ultimo_aumento    | 9733 |      2.41108     |      2           |      3.03829     |      0           |     17           |
| horas_trabajadas              | 9733 |    163.158       |    165           |     11.7247      |    116           |    188           |
| dias_ausente                  | 9733 |      1.1384      |      1           |      1.16005     |      0           |      7           |
| dias_licencia_medica          | 9733 |      0.169218    |      0           |      0.942026    |      0           |     15           |
| incidentes_seguridad_count    | 9733 |      0.0102743   |      0           |      0.101859    |      0           |      2           |
| duracion_turno_horas          | 9733 |      8.23045     |      8           |      0.421145    |      8           |      9           |
| horas_training_mes            | 9733 |      4.32796     |      0           |     17.8622      |      0           |    192           |
| horas_training_acumulado_anio | 9733 |     33.5717      |      4           |     61.0973      |      0           |    400           |
| dias_time_to_fill             | 2238 |     39.2525      |     32           |     21.3059      |     18           |    178           |
| antiguedad_meses_calc         | 9733 |     74.9695      |     72           |     42.045       |      0           |    185           |
| costo_total_mes               | 9733 |      1.90197e+06 |      1.725e+06   | 622898           |      1.26241e+06 |      1.01905e+07 |
| pct_he_sobre_base             | 9733 |      8.59027     |      8.86        |      4.00375     |      0           |     28.43        |
| antiguedad_anios              | 9733 |      6.18873     |      5.9         |      3.49853     |      0           |     15.4         |

### Variables categóricas

| columna                   |   categorías | más frecuente       | % que ocupa   | % vacío   |
|:--------------------------|-------------:|:--------------------|:--------------|:----------|
| activo                    |            2 | True                | 98.6%         | 0.0%      |
| genero                    |            2 | M                   | 63.5%         | 0.0%      |
| motivo_salida             |            5 | Renuncia voluntaria | 67.4%         | 98.6%     |
| area                      |           11 | Estampado           | 26.0%         | 0.0%      |
| subarea                   |           35 | Prensas Grandes     | 8.6%          | 0.0%      |
| categoria_collar          |            2 | Blue                | 81.9%         | 0.0%      |
| es_posicion_critica       |            2 | False               | 98.4%         | 0.0%      |
| es_top_performer          |            2 | False               | 91.9%         | 0.0%      |
| turno_trabajo             |            5 | Mañana              | 23.5%         | 0.0%      |
| fuente_reclutamiento      |            6 | Portal empleo       | 47.5%         | 77.0%     |
| es_produccion             |            2 | True                | 61.0%         | 0.0%      |
| scrap_valido              |            2 | True                | 60.9%         | 0.0%      |
| salario_sobre_tope_iqr    |            2 | False               | 85.7%         | 0.0%      |
| flag_edad_inconsistente   |            2 | False               | 99.5%         | 0.0%      |
| flag_antig_inconsistente  |            2 | False               | 95.0%         | 0.0%      |
| flag_snapshot_pre_ingreso |            2 | False               | 99.3%         | 0.0%      |
| banda_edad                |            5 | 30-39               | 45.0%         | 0.0%      |
| jubila_12m                |            2 | False               | 99.8%         | 0.0%      |
| jubila_24m                |            2 | False               | 99.3%         | 0.0%      |

### Fechas

| columna               | desde      | hasta      | % vacío   |
|:----------------------|:-----------|:-----------|:----------|
| mes_snapshot          | 2024-01-01 | 2025-05-01 | 0.0%      |
| fecha_nacimiento      | 1961-06-15 | 2003-05-01 | 0.0%      |
| fecha_ingreso         | 2009-12-31 | 2025-05-01 | 0.0%      |
| fecha_salida          | 2024-01-01 | 2025-05-22 | 98.6%     |
| ultimo_training_fecha | 2024-01-01 | 2025-05-31 | 65.4%     |

## Tabla `eventos_rrhh`

8,705 filas × 18 columnas

| Tipo de variable | Columnas |
|---|---|
| categorica | 9 |
| numerica continua | 5 |
| fecha | 1 |
| numerica discreta | 1 |
| texto | 1 |
| alta cardinalidad | 1 |

### Alertas

| Columna | Tipo | Alerta | Detalle |
|---|---|---|---|
| `mes_evento` | categorica | **ETIQUETAS RARAS** | 17 etiquetas bajo el 1% |
| `tipo_evento` | categorica | **ETIQUETAS RARAS** | 2 etiquetas bajo el 1% |
| `subtipo_evento` | categorica | **ETIQUETAS RARAS** | 18 etiquetas bajo el 1% |
| `severidad` | categorica | **VACÍOS** | 97.4% sin dato |
| `dias_perdidos` | numerica discreta | **MUY ASIMÉTRICA** | asimetría 36.5 — cola larga |
| `parte_cuerpo_afectada` | categorica | **VACÍOS** | 99.5% sin dato |
| `hora_evento` | categorica | **VACÍOS** | 97.4% sin dato |
| `hora_evento` | categorica | **ETIQUETAS RARAS** | 43 etiquetas bajo el 1% |
| `descripcion_detalle` | texto | **VACÍOS** | 97.4% sin dato |
| `accion_correctiva` | categorica | **VACÍOS** | 99.8% sin dato |
| `accion_correctiva` | categorica | **CASI CONSTANTE** | 'Capacitación refuerzo seguridad' ocupa el 100.0% |
| `accion_correctiva` | categorica | **CONSTANTE** | un único valor — no aporta información |
| `dias_time_to_fill` | numerica continua | **VACÍOS** | 97.9% sin dato |
| `costo_estimado` | numerica continua | **MUY ASIMÉTRICA** | asimetría 5.4 — cola larga |
| `area_empleado` | categorica | **ETIQUETAS RARAS** | 1 etiquetas bajo el 1% |
| `puesto_empleado` | alta cardinalidad | **ALTA CARDINALIDAD** | 52 valores distintos |

### Variables numéricas

|                         |    n |    media |   mediana |   desvío |   mín |    máx |
|:------------------------|-----:|---------:|----------:|---------:|------:|-------:|
| evento_id               | 8705 | 14141.8  |   14169   |  2565.5  |  8523 |  18521 |
| empleado_id             | 8705 |  1313.5  |    1322   |   181.49 |  1000 |   1693 |
| dias_perdidos           | 8705 |     0.99 |       1   |     0.52 |     0 |     25 |
| dias_time_to_fill       |  180 |    23.6  |      12.5 |    31.46 |     0 |    144 |
| costo_estimado          | 8702 | 28304.2  |   23830.8 | 16815    |  5000 | 150000 |
| antiguedad_meses_evento | 8705 |    77.53 |      72   |    40.48 |     0 |    179 |

### Variables categóricas

| columna               |   categorías | más frecuente                   | % que ocupa   | % vacío   |
|:----------------------|-------------:|:--------------------------------|:--------------|:----------|
| mes_evento            |           33 | 2024-01-01                      | 14.6%         | 0.0%      |
| tipo_evento           |            5 | ausencia                        | 97.4%         | 0.0%      |
| subtipo_evento        |           22 | Enfermedad                      | 32.9%         | 0.0%      |
| severidad             |            4 | info                            | 78.9%         | 97.4%     |
| parte_cuerpo_afectada |            6 | Mano                            | 22.2%         | 99.5%     |
| turno_evento          |            5 | Noche                           | 32.0%         | 0.0%      |
| hora_evento           |           45 | 09:00:00                        | 40.0%         | 97.4%     |
| accion_correctiva     |            1 | Capacitación refuerzo seguridad | 100.0%        | 99.8%     |
| area_empleado         |           11 | Estampado                       | 26.4%         | 0.0%      |

### Fechas

| columna      | desde      | hasta      | % vacío   |
|:-------------|:-----------|:-----------|:----------|
| fecha_evento | 2024-01-01 | 2025-05-28 | 0.0%      |

## Tabla `capacitaciones`

729 filas × 17 columnas

| Tipo de variable | Columnas |
|---|---|
| numerica continua | 5 |
| categorica | 5 |
| fecha | 2 |
| alta cardinalidad | 2 |
| numerica discreta | 2 |
| booleana | 1 |

### Alertas

| Columna | Tipo | Alerta | Detalle |
|---|---|---|---|
| `mes_training` | categorica | **ETIQUETAS RARAS** | 2 etiquetas bajo el 1% |
| `instructor` | alta cardinalidad | **ALTA CARDINALIDAD** | 580 valores distintos |
| `costo_training` | numerica continua | **MUY ASIMÉTRICA** | asimetría 4.6 — cola larga |
| `area_empleado` | categorica | **ETIQUETAS RARAS** | 1 etiquetas bajo el 1% |
| `puesto_empleado` | alta cardinalidad | **ALTA CARDINALIDAD** | 51 valores distintos |
| `nivel_jerarquico_empleado` | numerica discreta | **MUY ASIMÉTRICA** | asimetría 2.9 — cola larga |

### Variables numéricas

|                           |   n |    media |   mediana |    desvío |     mín |    máx |
|:--------------------------|----:|---------:|----------:|----------:|--------:|-------:|
| training_id               | 729 |  4472.55 |    5234   |   1782.23 |  600    |   5598 |
| empleado_id               | 729 |  1376.85 |    1391   |    200.97 | 1000    |   1693 |
| duracion_horas            | 729 |    65.57 |      64   |     36.22 |   16    |    160 |
| calificacion_examen       | 729 |    81.06 |      82   |     10.95 |   60    |    100 |
| rating_efectividad        | 729 |     3.61 |       4   |      1.13 |    2    |      5 |
| costo_training            | 729 | 66097.1  |   31309.3 | 113720    | 9096.06 | 800000 |
| nivel_jerarquico_empleado | 729 |     1.23 |       1   |      0.59 |    1    |      5 |

### Variables categóricas

| columna            |   categorías | más frecuente        | % que ocupa   | % vacío   |
|:-------------------|-------------:|:---------------------|:--------------|:----------|
| mes_training       |           18 | 2024-03              | 8.8%          | 0.0%      |
| tipo_training      |           25 | Capacitación General | 13.4%         | 0.0%      |
| categoria_training |            5 | Técnico              | 25.9%         | 0.0%      |
| modalidad          |            3 | Presencial           | 45.4%         | 0.0%      |
| completado         |            2 | True                 | 94.0%         | 0.0%      |
| area_empleado      |           11 | Estampado            | 22.8%         | 0.0%      |

### Fechas

| columna      | desde      | hasta      | % vacío   |
|:-------------|:-----------|:-----------|:----------|
| fecha_inicio | 2024-01-02 | 2025-05-31 | 0.0%      |
| fecha_fin    | 2024-01-10 | 2025-06-16 | 0.0%      |

## Resumen

**54 alertas** en total.

| Tipo de alerta | Cantidad |
|---|---|
| MUY ASIMÉTRICA | 17 |
| VACÍOS | 13 |
| ETIQUETAS RARAS | 10 |
| ALTA CARDINALIDAD | 8 |
| CASI CONSTANTE | 5 |
| CONSTANTE | 1 |

### Cómo leer estas alertas

Una alerta **no es un error**. Es una columna que merece una decisión explícita:

- **Vacíos** — hay que decidir si el dato falta o si no aplica a ese grupo (ver `politica_vacios.csv`).
- **Casi constante** — la columna casi no varía, así que aporta poco para comparar grupos.
- **Etiquetas raras** — categorías con muy pocos casos; los porcentajes sobre ellas son ruido.
- **Muy asimétrica** — unos pocos valores muy altos tiran del promedio; conviene mirar la mediana.
- **Alta cardinalidad** — demasiados valores distintos (nombres, identificadores); no sirve para agrupar.
