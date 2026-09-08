# TechnoStamp — Discovery 

## Resumen ejecutivo

Este proyecto analiza información de empleados, incidentes de RR. HH. y capacitaciones de TechnoStamp Industries. El objetivo es transformar datos operativos en evidencia para decisiones sobre rotación, seguridad, sucesión, carga de trabajo, equidad salarial y trazabilidad.

El resultado  es un Discovery reproducible en capas: datos originales, limpieza y linaje, análisis, visualizaciones, tablas de soporte e informes ejecutivos. El proyecto es descriptivo y de diagnóstico; no entrena modelos predictivos ni automatiza decisiones.

## Problema

El negocio necesitaba entender si existían riesgos relevantes en cinco áreas:

- sucesión y jubilaciones próximas;
- representación de género y brecha salarial;
- horas extra y sobrecarga;
- prevención de incidentes de seguridad;
- rotación y costo de retención.

El desafío no era solamente calcular indicadores. Las fuentes presentaban inconsistencias, campos faltantes, dos registros distintos de incidentes y diferencias entre la dotación informada y la observada. Por eso, antes de interpretar resultados, se documentan calidad, cobertura, supuestos y límites de cada dato.

## Objetivo

### Objetivo general

Construir un diagnóstico de RR. HH. que permita distinguir señales accionables de patrones que no se sostienen con la evidencia disponible.

### Objetivos específicos

1. Preservar los datos originales y hacer trazables las transformaciones.
2. Construir tablas analíticas a nivel empleado y empleado-mes.
3. Medir tasas normalizadas, evitando comparar conteos de grupos de distinto tamaño.
4. Contrastar las principales hipótesis del negocio con evidencia estadística.
5. Traducir los resultados a informes, visualizaciones y entregables ejecutivos.

### Fuera de alcance

- Entrenar o desplegar modelos de machine learning.
- Inferir causalidad a partir de datos observacionales.
- Prometer ahorros como cifras garantizadas.

## Enfoque técnico

El flujo real del proyecto es:

```text
Datos originales
    ↓
Perfilado y control de calidad
    ↓
Limpieza versionada + linaje
    ↓
Parquets analíticos
    ↓
Análisis y tablas de soporte
    ↓
Visualizaciones exploratorias y de decisión
    ↓
Informes, guiones y presentaciones
```

### 1. Fuentes de datos

Las fuentes principales son:

- `empleados_mensual.csv`: panel mensual de empleados.
- `eventos_rrhh.csv`: fuente auditable de incidentes.
- `capacitaciones.csv`: registros de capacitaciones.

Los archivos originales se conservan sin sobrescribirlos.
### 2. Perfilado y calidad

`04_scripts/01_perfilado.py` y `04_scripts/02_calidad.py` inspeccionan estructura, tipos, valores faltantes, categorías, duplicados, rangos y consistencia temporal.

La limpieza vigente se encuentra en `04_scripts/13_limpieza_v2.py`. Genera datos derivados en `06_resultados/Discovery/datos_transformados/`, junto con:

- `transformaciones.json`: receta persistida de transformaciones;
- `_linaje.json`: información de procedencia;
- `politica_vacios.csv`: clasificación de valores ausentes.

### 3. Tablas analíticas

La tabla de panel conserva el nivel empleado-mes. La tabla `empleados_nivel_persona.parquet` contiene una fila por persona y se usa para preguntas de entidad, como rotación y salario. Esta separación evita ponderar  a una persona por la cantidad de meses que permaneció en la empresa.

### 4. Análisis

Los scripts de `04_scripts/` leen los parquets transformados y producen resultados en `06_resultados/Discovery/tablas_soporte/`. Entre los análisis se incluyen:

- preguntas P1 y P2 sobre sucesión y género;
- verificaciones de criticidad;
- horas extra, incidentes y rotación;
- verificaciones de seguridad;
- Análisis Exploratorio de Datos (EDA);
- diagnóstico de fragilidad;
- rotación temporal;
- hora extra estructural vs volatilidad de demanda (pregunta C-level Q2, `19_hora_extra_estructural.py`);
- costo laboral por pieza buena (pregunta C-level Q1, `20_costo_pieza_buena.py`);
- business case.

Las versiones vigentes para limpieza y business case son `13_limpieza_v2.py` y `17_business_case_v2.py`. `03_limpieza.py` y `09_business_case.py` permanecen en el repositorio como versiones anteriores y no deben confundirse con el flujo vigente.

### 5. Visualizaciones

- `04_scripts/08_visualizaciones.py` genera visualizaciones exploratorias `G1` a `G9` y `G15`–`G16`.
- `04_scripts/18_visualizaciones_decision.py` genera visualizaciones de decisión `G8` a `G14`.

Los prefijos `G8` y `G9` aparecen en los dos scripts con el mismo número pero nombres de archivo distintos; al citar un gráfico conviene usar el nombre de archivo completo (ver pendiente de trazabilidad en `decisions.md`).

Las imágenes se escriben en `06_resultados/Discovery/visualizaciones/`. Son artefactos regenerables y están excluidas del versionado mediante `.gitignore`.

### 6. Notebook

`03_notebooks/Technostamp_Completo.ipynb` funciona como narrativa y orquestador. La lógica analítica debe permanecer en los scripts; el notebook no debería duplicarla. Ejecuta etapas, captura salida y muestra visualizaciones inline.

## Decisiones técnicas relevantes

El registro completo está en [`decisions.md`](decisions.md) y el detalle ampliado en [`decisions_detalle.md`](decisions_detalle.md). Las decisiones más importantes son:

| Decisión | Motivo |
|---|---|
| Raw inmutable | Permite corregir encoding y transformaciones sin perder la fuente original. |
| Flags en lugar de borrar filas | Evita sesgar resultados eliminando inconsistencias relevantes. |
| `eventos_rrhh` como fuente canónica de incidentes | Es auditable y contiene 45 casos detallados, frente a los 100 agregados del panel. |
| Una fila por persona para preguntas de persona | Evita que el panel longitudinal sobrepondere a quienes permanecen más meses. |
| Tasas por exposición, no conteos | Permite comparar grupos con distinta dotación o cantidad de empleado-mes. |
| Valores extremos salariales detectados, no recortados | Siguen la estructura jerárquica y no fueron considerados errores. |
| Enero de 2024 excluido del cálculo oficial de rotación | Las 19 salidas corresponden a arrastre del corte inicial. |
| Rotación oficial de 16,7% | Es la tasa acumulada del período limpio: 113 salidas sobre 675 personas expuestas. |
| Intervalos y corrección de Bonferroni en comparaciones | Evita presentar como diferencias reales variaciones compatibles con el azar. |
| Business case como rango | La mayor parte del costo por salida depende de supuestos de vacancia y rampa. |
| No avanzar a proyectos de ML | Los insights actuales no superan los umbrales de frecuencia, escala y calidad de inferencia necesarios. |
| Hora extra tratada como déficit de dotación estructural | Es plana durante 17 meses y no sigue al volumen producido; condiciona —no revierte— la conclusión de no contratar. |
| Costo por pieza: descriptivo sí, efecto de la rotación no | El costo unitario subió con la caída de volumen; controlado el tiempo, la rotación no lo explica. |

## Estructura del proyecto

```text
.
├── 01_Documentos/                 # Andamiaje documental
├── 02_datos/
│   └── 01_Originales/             # Fuentes originales, inmutables
├── 03_notebooks/
│   └── Technostamp_Completo.ipynb # Narrativa y orquestación
├── 04_scripts/                    # Perfilado, limpieza, análisis y gráficos
├── 05_modelos/                    # Sin modelos predictivos en este alcance
├── 06_resultados/
│   ├── Discovery/
│   │   ├── datos_transformados/   # Parquets, receta y linaje
│   │   ├── tablas_soporte/        # CSVs y supuestos analíticos
│   │   ├── visualizaciones/       # PNGs regenerables
│   │   ├── business_case/         # Guiones y entregables de negocio
│   │   └── Discovery_report.md    # Informe técnico principal
│   └── EDA/                       # Informe de alertas exploratorias
├── decisions.md                   # Registro corto de decisiones
├── decisions_detalle.md           # Justificación detallada
├── ESTUDIO_conceptos_technostamp.md # Marco conceptual
└── .gitignore                     # Datos y artefactos no versionables
```

Los directorios de datos derivados y resultados dependen de la ejecución del pipeline. Los datos fuente, scripts, notebook y documentación son los elementos principales del proyecto. Los cachés, builds y visualizaciones regenerables no deben confundirse con entregables finales.

## Cómo reproducir el proyecto

### Requisitos observados

- Python con `pandas`, `numpy`, `matplotlib`, `pyarrow` y las dependencias utilizadas por los scripts.
- Jupyter para ejecutar el notebook.
- Windows, o adaptación de las rutas de datos: la mayoría de los scripts todavía contiene la ruta absoluta `C:\Users\Dell\Agus\Nivii AI`.

No existe actualmente un archivo de dependencias versionado ni un comando único de instalación verificado.

### Orden lógico del pipeline

El orden vigente documentado es:

```text
01 → 02 → 13 → 04 → 05 → 06 → 07 → 08 →
10 → 11 → 19 → 20 → 12 → 14 → 15 → 16 → 17 → 18
```

La numeración de los archivos no coincide completamente con el orden de ejecución. Antes de declarar reproducible el proyecto, debe corregirse la etapa que interrumpe el notebook y conviene reemplazar las rutas absolutas por rutas relativas a la raíz del repositorio.

## Resultados principales

Los resultados están documentados en [`06_resultados/Discovery/Discovery_report.md`](06_resultados/Discovery/Discovery_report.md). Entre los hallazgos respaldados por los análisis se encuentran:

- la rotación limpia es **16,7% acumulada** en el período analizado;
- Mantenimiento Eléctrico es la única área que se distingue del promedio después de considerar incertidumbre y comparaciones múltiples;
- cuatro personas se encuentran próximas a jubilarse, pero el caso operativo más urgente es un puesto unipersonal de Supervisor de Logística sin sucesor;
- la brecha salarial cruda se reduce prácticamente a cero al controlar por composición y nivel;
- la seguridad del turno noche presenta una tasa de incidentes mayor, pero las conclusiones causales requieren mejores registros;
- el business case de retención debe expresarse como rango, no como ahorro garantizado;
- la hora extra de las áreas de producción es estructural: plana durante 17 meses y sin relación con el volumen producido, equivalente a 24–34 operarios de dotación;
- el costo laboral por pieza buena (~$2.000) subió alrededor de 17 % en el período, aproximadamente mitad por menor productividad y mitad por el precio de la hora; la rotación mes a mes no lo explica una vez descontada la tendencia.

Estos resultados son descriptivos o estimados según cada caso. No prueban causalidad ni implican que una intervención específica vaya a producir el valor económico estimado.

## Limitaciones

- El período observado es enero de 2024 a mayo de 2025.
- El primer mes contiene arrastre de corte y se excluye de la rotación oficial.
- Hay inconsistencias internas de antigüedad, edad y snapshots; se conservan con flags.
- La dotación observada no coincide con la dotación mencionada en el brief.
- Los incidentes del panel y los eventos auditables no tienen la misma cobertura.
- El notebook no completa actualmente todas las etapas en una ejecución lineal.
- Los scripts dependen de rutas absolutas locales.
- No hay información suficiente para identificar causas de renuncia ni estimar efectos causales.
- El business case contiene supuestos relevantes sobre vacancia y productividad del reemplazo.
- Los datos activos están sujetos a censura por derecha: una persona activa todavía puede salir después del cierre observado.

## Convenciones y buenas prácticas

- No modificar los datos originales.
- Persistir las transformaciones y su linaje.
- Marcar inconsistencias en lugar de borrar filas sin justificación.
- Comparar tasas normalizadas, no conteos brutos.
- Mostrar denominadores y declarar el universo de cada métrica.
- Separar resultados descriptivos, estimaciones y supuestos.
- Registrar decisiones nuevas en `decisions.md` y ampliar el detalle en `decisions_detalle.md`.
- Mantener la lógica en scripts y usar el notebook como narrativa y orquestación.
- No versionar caches, builds, datos locales ni visualizaciones regenerables.

## Estado del proyecto

### Completado

- Discovery de datos y calidad.
- Limpieza con receta y linaje.
- Análisis de las preguntas P1 a P5.
- Visualizaciones exploratorias y de decisión.
- Informe técnico, documentación de decisiones y business case.

### Pendiente

- Corregir la ejecución lineal del notebook.
- Eliminar rutas absolutas y parametrizar la raíz del proyecto.
- Incorporar un archivo de dependencias reproducible.
- Confirmar con el cliente la diferencia entre dotación informada y observada.
- Definir formalmente si el índice propio de criticidad reemplaza al campo del sistema origen.
- Renumerar los gráficos `G8`/`G9`, que hoy tienen el mismo número en `08_visualizaciones.py` y `18_visualizaciones_decision.py`.

## Licencia y uso

No se encontró una licencia de software definida. El repositorio contiene datos y documentación de negocio; su uso debe limitarse a los fines autorizados por TechnoStamp.

## Auditoría del README

### Fuentes inspeccionadas

- `decisions.md` y `decisions_detalle.md`.
- `06_resultados/Discovery/Discovery_report.md`.
- `06_resultados/Discovery/auditoria_mejoras_technostamp/01_contexto_y_mapa.md`.
- `06_resultados/Discovery/business_case/ESTADO_business_case.md`.
- `03_notebooks/Technostamp_Completo.ipynb`.
- `04_scripts/` y `.gitignore`.

### Verificaciones realizadas

- Se verificó la estructura real de carpetas y scripts.
- Se verificó la existencia de los archivos enlazados.
- Se contrastó el orden lógico del pipeline con la documentación de auditoría.
- Se verificó que las visualizaciones PNG estén excluidas del versionado.

### Información no confirmada

- No existe un archivo de dependencias completo.
- No existe un comando único verificado para reconstruir todo el proyecto.
- La ejecución de punta a punta del notebook requiere correcciones pendientes.

### Mejoras futuras de documentación

- Crear `requirements.txt` o `pyproject.toml`.
- Documentar una ejecución limpia desde un entorno virtual nuevo.
- Parametrizar las rutas y agregar un comando de pipeline.
- Separar explícitamente versiones vigentes y obsoletas de los scripts.
