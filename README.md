# TechnoStamp — Discovery 

## Resumen ejecutivo

Este proyecto analiza información de empleados, incidentes de RR. HH. y capacitaciones de TechnoStamp Industries. El objetivo es transformar datos operativos en evidencia para decisiones sobre rotación, seguridad, sucesión, carga de trabajo, equidad salarial y trazabilidad.

El resultado  es un Discovery reproducible en capas: datos originales, limpieza y linaje, análisis, visualizaciones, tablas de soporte e informes ejecutivos. El proyecto es descriptivo y de diagnóstico; no entrena modelos predictivos ni automatiza decisiones. Está todo explicado en el notebook Technostamp_Completo.

## Problema

El negocio necesitaba entender si existían riesgos relevantes en cinco áreas:

- sucesión y jubilaciones próximas;
- representación de género y brecha salarial;
- horas extra y sobrecarga;
- prevención de incidentes de seguridad;
- rotación y costo de retención.

Las fuentes presentaban inconsistencias, campos faltantes, dos registros distintos de incidentes y diferencias entre la dotación informada y la observada. Por eso, antes de interpretar resultados, se documentan calidad, cobertura, supuestos y límites de cada dato.

## Objetivo

### Objetivo general

Construir un diagnóstico de RR. HH. que permita distinguir señales accionables de patrones que no se sostienen con la evidencia disponible.

### Objetivos específicos

1. Preservar los datos originales y hacer trazables las transformaciones.
2. Construir tablas analíticas a nivel empleado y empleado-mes.
3. Medir tasas normalizadas, evitando comparar conteos de grupos de distinto tamaño.
4. Contrastar las principales hipótesis del negocio con evidencia estadística.
5. Traducir los resultados a informes, visualizaciones y entregables ejecutivos.
6. Descubrir insights ni el equipo de RRHH sabe que no sabe.

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

- `transformaciones.json`: receta persistida de transformaciones y procedencia;
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

Las versiones vigentes para limpieza y business case son `13_limpieza_v2.py` y `17_business_case_v2.py`. Reemplazaron a `03_limpieza.py` y `09_business_case.py`, que fueron removidas del repositorio.

### 5. Visualizaciones

- `04_scripts/08_visualizaciones.py` genera visualizaciones exploratorias `G1` a `G9` y `G15`–`G16`.
- `04_scripts/18_visualizaciones_decision.py` genera visualizaciones de decisión `G8` a `G14`.

Los prefijos `G8` y `G9` aparecen en los dos scripts con el mismo número pero nombres de archivo distintos; al citar un gráfico conviene usar el nombre de archivo completo (ver pendiente de trazabilidad en `decisions.md`).

Las imágenes se escriben en `06_resultados/Discovery/visualizaciones/`. Son artefactos regenerables y están excluidas del versionado.
### 6. Notebook

`03_notebooks/Technostamp_Completo.ipynb` funciona como narrativa y orquestador. La lógica analítica permanece en los scripts; el notebook no las duplica . Ejecuta etapas, captura salida y muestra visualizaciones.

## Decisiones técnicas relevantes

El registro completo está en [`decisions.md`](decisions.md) y el detalle ampliado en [`decisions_detalle.md`](decisions_detalle.md). Las decisiones más importantes son:


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
├── requirements.txt              # Dependencias del pipeline y el notebook
└── .gitignore                     # Datos y artefactos no versionables
```


## Cómo reproducir el proyecto

### Requisitos

- Python 3.11 o superior (probado en 3.13.7).
- Las librerías de `requirements.txt`: `pandas`, `numpy`, `pyarrow` (para los `.parquet`), `matplotlib` y `jupyterlab`.

Los scripts derivan la raíz del proyecto de su propia ubicación (`Path(__file__).resolve().parents[1]`), así que la carpeta puede extraerse en cualquier ruta y en cualquier sistema operativo. No hay rutas absolutas.

### Pasos

```bash
# 1. Entorno e instalación
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt

# 2a. Opción recomendada: el notebook
jupyter lab                       # abrir 03_notebooks/Technostamp_Completo.ipynb y "Run All"

# 2b. Opción alternativa: los scripts, en orden (desde cualquier carpeta)
python 04_scripts/01_perfilado.py
python 04_scripts/02_calidad.py
python 04_scripts/13_limpieza_v2.py
python 04_scripts/04_p1_p2.py
python 04_scripts/05_verif_critica.py
python 04_scripts/06_p3_p4_p5.py
python 04_scripts/07_verif_incidentes_p5.py
python 04_scripts/08_visualizaciones.py
python 04_scripts/10_sensibilidad_he.py
python 04_scripts/11_verif_cronicos_seguridad.py
python 04_scripts/19_hora_extra_estructural.py
python 04_scripts/20_costo_pieza_buena.py
python 04_scripts/12_diagnostico_gaps.py
python 04_scripts/14_eda_sistematico.py
python 04_scripts/15_diagnostico_fragilidad.py
python 04_scripts/16_rotacion_temporal.py
python 04_scripts/17_business_case_v2.py
python 04_scripts/18_visualizaciones_decision.py
```

`13_limpieza_v2.py` es la entrada del pipeline: lee los CSV de `02_datos/01_Originales/` y genera los parquet en `06_resultados/Discovery/datos_transformados/`. El resto lee esos parquet. Salidas: parquet en `datos_transformados/`, CSV en `tablas_soporte/`, PNG en `visualizaciones/` (los directorios se crean solos si no existen).

`13_limpieza_v2.py` y `17_business_case_v2.py` son las versiones vigentes. La numeración de los archivos no coincide del todo con el orden de ejecución.

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

Estos resultados son descriptivos, No prueban causalidad ni implican que una intervención específica vaya a producir el valor económico estimado.

## Limitaciones

- El período observado es enero de 2024 a mayo de 2025.
- El primer mes contiene arrastre de corte y se excluye de la rotación oficial.
- Hay inconsistencias internas de antigüedad, edad y snapshots; se conservan con flags.
- La dotación observada no coincide con la dotación mencionada en el brief.
- Los incidentes del panel y los eventos auditables no tienen la misma cobertura.
- No hay información suficiente para identificar causas de renuncia ni estimar efectos causales.
- El business case contiene supuestos relevantes sobre vacancia y productividad del reemplazo.

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

- Verificar la corrida lineal completa del notebook (la celda de `mostrar_graficos` de las visualizaciones de decisión).
- Definir formalmente si el índice propio de criticidad reemplaza al campo del sistema origen.


### Mejoras futuras de documentación

- Agregar un único script que ejecute todo el pipeline en orden.
- Separar explícitamente versiones vigentes y obsoletas de los scripts.
- Renumerar los gráficos `G8`/`G9` para eliminar la ambigüedad entre los dos scripts de visualización.
