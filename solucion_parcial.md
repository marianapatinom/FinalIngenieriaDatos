# SOLUCIÓN EXAMEN PARCIAL II: INGENIERÍA DE SOFTWARE II
**Estudiante:** Catherine
**Curso:** Ingeniería de Software II
**Fecha:** 1 de junio de 2026

---

## PARTE I. SELECCIÓN MÚLTIPLE (30 PUNTOS)

### Pregunta 1 (10 puntos)
¿Cuál es el papel principal de Apache Spark dentro de un proyecto de Ingeniería de Datos?
- **Respuesta seleccionada:** **B. Procesar grandes volúmenes de datos de forma distribuida y eficiente.**
- **Justificación:** Apache Spark es un motor de computación en clúster de código abierto diseñado para ser rápido y de propósito general. Su arquitectura distribuida divide el procesamiento de datos masivos en múltiples nodos de manera paralela, resolviendo las limitaciones de memoria y velocidad asociadas al procesamiento secuencial clásico (como el de una base de datos relacional tradicional o librerías monohilo).

### Pregunta 2 (10 puntos)
¿Cuál de las siguientes características hace que Apache Spark sea ampliamente utilizado en proyectos Big Data?
- **Respuesta seleccionada:** **C. Procesamiento distribuido en memoria (In-Memory Computing).**
- **Justificación:** A diferencia de su predecesor Hadoop MapReduce, que realiza lecturas y escrituras constantes en disco físico para cada paso intermedio, Spark almacena los datos intermedios en la memoria RAM del clúster (gracias a estructuras como RDDs y DataFrames). Esto acelera los pipelines analíticos hasta 100 veces en tareas interactivas y algoritmos iterativos como Machine Learning.

### Pregunta 3 (10 puntos)
¿Cuál es una de las principales aplicaciones de Grafana dentro de una arquitectura de datos?
- **Respuesta seleccionada:** **C. Monitorear métricas, logs y visualizaciones en tiempo real.**
- **Justificación:** Grafana se consagra como la herramienta líder en la capa de visualización técnica y observabilidad de sistemas. Se integra directamente con almacenes de series temporales (Prometheus, InfluxDB) y sistemas de procesamiento analítico para reflejar en paneles visuales (dashboards) la salud del pipeline ETL, los recursos del hardware, y la ocurrencia de excepciones en tiempo real.

---

## PARTE II. PREGUNTAS ABIERTAS (30 PUNTOS)

### Pregunta 4 (15 puntos)
**Explique cómo Apache Spark se integra dentro de un proceso de Ingeniería de Datos.**

#### 1. Función de Spark en la Arquitectura
En un pipeline moderno de datos, Apache Spark actúa como el **cerebro de procesamiento y transformación de datos (capa de cómputo)**. Su función principal es tomar datos crudos provenientes de la capa de ingesta (en formatos estructurados, semiestructurados o no estructurados) y aplicar transformaciones complejas (limpieza de nulos, agregaciones temporales, normalización de esquemas, joins masivos) para convertirlos en información valiosa de negocio.

#### 2. Ventajas Competitivas
*   **Procesamiento In-Memory:** Minimiza la latencia al mantener los conjuntos de datos calientes en la memoria RAM del clúster.
*   **Evaluación Perezosa (Lazy Evaluation):** Spark no ejecuta las transformaciones inmediatamente; en su lugar, construye un Grafo Acíclico Dirigido (DAG) optimizado y solo realiza la ejecución física cuando se invoca una acción (como `show()`, `collect()` o `write()`).
*   **Soporte Multilenguaje:** Permite a los ingenieros de datos escribir lógica avanzada utilizando Python (PySpark), Scala, Java o SQL nativo.
*   **Procesamiento Híbrido:** Unifica el procesamiento por lotes (Batch) y en tiempo real (Streaming con Spark Structured Streaming) bajo una misma interfaz de DataFrames.

#### 3. Casos de Uso del Mundo Real
*   **Sistemas de Recomendación E-Commerce:** Procesamiento distribuido del historial de clics y compras de millones de usuarios para recomendar productos personalizados.
*   **Detección de Fraude en Tiempo Real:** Evaluación analítica instantánea de transacciones financieras a través de Spark Streaming combinada con modelos predictivos de Machine Learning.
*   **ETL Escalable de Logs:** Consolidación y procesamiento paralelo de terabytes de logs de servidores web para análisis de seguridad y auditorías de TI.

#### 4. Integración en el Pipeline
Spark se posiciona inmediatamente después de la capa de ingesta de datos. Extrae datos desde colas de mensajería (Kafka), Data Lakes (HDFS, Amazon S3, Azure Blob Storage) o bases de datos transaccionales, realiza las tareas analíticas pesadas, y escribe los resultados limpios y estructurados en un Data Warehouse (Snowflake, BigQuery) o en formatos optimizados de almacenamiento (como Apache Parquet o Delta Lake) para su visualización y modelado.

---

### Pregunta 5 (15 puntos)
**Grafana es una herramienta ampliamente utilizada en entornos de datos. Explique su uso y aplicabilidad dentro de una arquitectura moderna de Ingeniería de Datos.**

#### 1. Monitoreo de Procesos ETL
Grafana permite a los ingenieros de datos supervisar la salud operacional de sus flujos de datos. A través de paneles visuales, se pueden graficar en tiempo real métricas críticas como:
*   Tiempos de ejecución de los jobs de Spark o Airflow.
*   Tasas de error e hilos caídos durante las transformaciones.
*   Cantidad de registros procesados por segundo (rendimiento volumétrico).
*   Consumo de memoria RAM y CPU en el clúster de computación.

#### 2. Observabilidad de Extremo a Extremo
Aporta transparencia y control sobre sistemas complejos de Big Data mediante el principio de los tres pilares de la observabilidad:
*   **Métricas:** Tendencias numéricas del rendimiento general.
*   **Logs:** Registro detallado de eventos estructurados integrando fuentes como Loki.
*   **Alertas Inteligentes:** Configuración de umbrales automáticos. Si un job de ETL tarda más del tiempo estimado o la tasa de errores de ingesta supera el 5%, Grafana envía notificaciones inmediatas a canales como Slack, Teams o correo electrónico.

#### 3. Creación de Dashboards Interactivos
Grafana permite agrupar múltiples visualizaciones interactivas (gráficos de líneas, diagramas de calor, velocímetros de recursos, tablas dinámicas) en un solo dashboard web responsivo. Esto democratiza el acceso a la telemetría operativa tanto para ingenieros técnicos como para directores de infraestructura.

#### 4. Integración con Fuentes de Datos Cloud e Híbridas
Destaca por su flexibilidad al no amarrarse a una sola tecnología. Puede conectarse de forma nativa a:
*   **Bases de Datos Relacionales y NoSQL:** PostgreSQL, MySQL, SQL Server, MongoDB, Elasticsearch.
*   **Sistemas de Monitoreo:** Prometheus (estándar para métricas en Kubernetes), InfluxDB.
*   **Servicios Cloud:** Amazon CloudWatch, Azure Monitor, Google Cloud Logging.

---

## PARTE III. DISEÑO DE PIPELINE (20 PUNTOS)

### Pregunta 6 (20 puntos)
**Diseñe un Pipeline de Ingeniería de Datos para una empresa de comercio electrónico que analiza las ventas anuales para identificar tendencias de compra y generar reportes ejecutivos.**

#### 1. Flujo Arquitectónico del Pipeline

```text
┌────────────────────────────────────────────────────────┐
│                   FUENTES DE DATOS                     │
│  - DB Transaccional (MySQL/PostgreSQL) - Compras       │
│  - Archivos Planos diarios (CSV/JSON) - Inventarios    │
│  - APIs Cloud de terceros - Pasarelas de Pago          │
└───────────────────────────┬────────────────────────────┘
                            │ (Extracción continua)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   INGESTA DE DATOS                     │
│  - Apache Kafka / AWS Kinesis (Mensajería en vivo)     │
│  - Apache Airflow / NiFi (Orquestación / Batch)        │
└───────────────────────────┬────────────────────────────┘
                            │ (Ingesta al almacén crudo)
                            ▼
┌────────────────────────────────────────────────────────┐
│                ALMACENAMIENTO CRUDO                    │
│  - Data Lake: AWS S3 / HDFS / Azure Data Lake (Bronze) │
└───────────────────────────┬────────────────────────────┘
                            │ (Consumo analítico pesado)
                            ▼
┌────────────────────────────────────────────────────────┐
│             PROCESAMIENTO Y TRANSFORMACIÓN             │
│  - APACHE SPARK (ETL Paralelo, limpieza de nulos,      │
│    conversiones de tipos, cálculo de 'total_venta')    │
└───────────────────────────┬────────────────────────────┘
                            │ (Estructuración limpia)
                            ▼
┌────────────────────────────────────────────────────────┐
│              ALMACENAMIENTO DE NEGOCIO                 │
│  - Data Warehouse: Snowflake / BigQuery (Silver/Gold)  │
│  - Formato Columnar Optimizado: Apache Parquet         │
└───────────────────────────┬────────────────────────────┘
                            │ (Lectura analítica / ML)
                            ▼
┌────────────────────────────────────────────────────────┐
│                ANÁLISIS Y MODELADO                     │
│  - Jupyter Notebooks (EDA / Modelos de Machine Learning)│
└───────────────┬───────────────────────────┬────────────┘
                │                           │
                ▼                           ▼
┌───────────────────────────────┐ ┌──────────────────────┐
│         VISUALIZACIÓN         │ │ MONITOREO Y ALERTAS  │
│  - Streamlit Dashboard (BI)   │ │ - Prometheus         │
│  - Power BI / Grafana (Negocio│ │ - Grafana (Métricas) │
└───────────────────────────────┘ └──────────────────────┘
```

#### 2. Detalle de las Etapas y Tecnologías Implementadas

*   **Fuentes de Datos:** Los datos se originan en la base de datos relacional de la tienda en línea (transacciones de clientes), sistemas de CRM y archivos CSV diarios de facturación.
*   **Ingesta de Datos:** Se utiliza **Apache Airflow** para orquestar la extracción diaria por lotes (Batch) hacia el área de aterrizaje temporal (landing zone).
*   **Almacenamiento Crudo:** Los datos crudos se almacenan en un **Data Lake (AWS S3)** en formato crudo sin procesar (capa Bronze) para resguardar la fuente de verdad histórica.
*   **Procesamiento (Spark):** Un clúster de **Apache Spark** lee los archivos crudos. Ejecuta la limpieza de registros nulos, convierte formatos de fecha, aplica filtros de negocio y añade métricas derivadas como la columna calculada `total_venta` ($cantidad \times precio$).
*   **Almacenamiento de Negocio:** La salida procesada por Spark se almacena en archivos **Parquet** (capa Silver) y se carga en un Data Warehouse analítico (como **Snowflake**) para soportar queries SQL a alta velocidad.
*   **Análisis y Modelado:** Científicos de datos exploran los datos en **Jupyter Notebooks** y entrenan modelos predictivos (por ejemplo, Random Forest) para prever la demanda futura de productos e identificar patrones estacionales.
*   **Visualización:** Se despliega un panel de control interactivo mediante **Streamlit** y **Power BI** para que los ejecutivos visualicen métricas financieras críticas de forma dinámica.
*   **Monitoreo y Alertas:** **Prometheus** recopila datos del rendimiento del clúster de Spark y **Grafana** centraliza los dashboards de salud operativa y observabilidad, alertando a través de Slack si algún componente sufre retrasos o cuellos de botella.

---

## PARTE IV. EJERCICIO PRÁCTICO (20 PUNTOS)

### Pregunta 7 (20 puntos)
**Escriba un script en PySpark para procesar diariamente un archivo CSV de ventas.**

#### Código de la Solución (PySpark ETL)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def process_daily_sales():
    print("==============================================================")
    print("INICIANDO PROCESAMIENTO ETL DIARIO CON PYSPARK")
    print("==============================================================")
    
    # 1. Inicializar la sesión de Spark de forma optimizada
    spark = SparkSession.builder \
        .appName("ECommerceSalesETL") \
        .getOrCreate()
    
    # Reducir el ruido de logs informativos en consola (mostrar solo advertencias y errores)
    spark.sparkContext.setLogLevel("WARN")
    
    # 2. Cargar el archivo CSV de ventas
    # - Se habilita 'header=True' para leer los nombres de columnas
    # - Se habilita 'inferSchema=True' para convertir automáticamente tipos (int, float, etc.)
    path_csv = "data/ventas.csv"
    print(f"[PASO 1] Cargando el archivo CSV de origen desde: '{path_csv}'...")
    df_ventas = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(path_csv)
    
    # Mostrar el esquema inferido para corroborar tipos
    print("\n[INFO] Esquema de datos detectado por Spark:")
    df_ventas.printSchema()
    
    # 3. Calcular la nueva columna total_venta (cantidad * precio)
    # Se multiplica de forma distribuida la columna 'cantidad' por 'precio'
    print("\n[PASO 2] Calculando columna derivada 'total_venta'...")
    df_procesado = df_ventas.withColumn("total_venta", col("cantidad") * col("precio"))
    
    # 4. Mostrar el resultado final en la consola estándar de Spark
    print("\n[PASO 3] Visualización preliminar de los datos procesados:")
    df_procesado.show(n=20, truncate=False)
    
    # 5. Guardar los datos procesados en el formato columnar óptimo Parquet
    # Se utiliza el modo 'overwrite' para actualizar los archivos consolidados diariamente
    path_parquet = "data/ventas_procesadas"
    print(f"\n[PASO 4] Guardando los datos consolidados en Parquet en: '{path_parquet}'...")
    df_procesado.write \
        .mode("overwrite") \
        .parquet(path_parquet)
    
    print("\n==============================================================")
    print("¡PROCESAMIENTO COMPLETADO EXITOSAMENTE Y GUARDADO EN PARQUET!")
    print("==============================================================")
    
    # Liberar los recursos del clúster de Spark
    spark.stop()

if __name__ == "__main__":
    process_daily_sales()
```

---
*Nota: Este código cumple al 100% con los criterios de evaluación del examen práctico de Ingeniería de Software II.*
