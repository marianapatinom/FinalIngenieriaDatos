from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def run_etl():
    print("==============================================================")
    print("Iniciando el Pipeline ETL con PySpark...")
    print("==============================================================")
    
    # 1. Crear o recuperar la sesión de Spark
    spark = SparkSession.builder \
        .appName("SalesETL") \
        .getOrCreate()
    
    # Establecer el nivel de log a WARN para evitar exceso de mensajes informativos en consola
    spark.sparkContext.setLogLevel("WARN")
    
    # 2. Cargar el archivo CSV
    # Se infiere el esquema y se indica que el archivo tiene cabecera
    path_csv = "data/ventas.csv"
    print(f"1. Cargando el archivo CSV desde: {path_csv}...")
    df_ventas = spark.read.option("header", "true").option("inferSchema", "true").csv(path_csv)
    
    # Mostrar el esquema inicial para validación
    print("\nEsquema de los datos cargados:")
    df_ventas.printSchema()
    
    # 3. Calcular la nueva columna total_venta (cantidad * precio)
    print("\n2. Calculando la columna 'total_venta' (cantidad * precio)...")
    df_procesado = df_ventas.withColumn("total_venta", col("cantidad") * col("precio"))
    
    # 4. Mostrar el resultado final en consola
    print("\n3. Resultado final del procesamiento:")
    df_procesado.show(n=35, truncate=False)
    
    # 5. Guardar los datos procesados en formato Parquet
    path_parquet = "data/ventas_procesadas"
    print(f"4. Guardando los datos procesados en formato Parquet en: {path_parquet}...")
    df_procesado.write.mode("overwrite").parquet(path_parquet)
    
    print("\n¡Pipeline ETL ejecutado con éxito y datos guardados en formato Parquet!")
    print("==============================================================")
    
    # Detener la sesión de Spark
    spark.stop()

if __name__ == "__main__":
    run_etl()
