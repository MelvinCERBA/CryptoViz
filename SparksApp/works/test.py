from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

def foreach_batch_function(df, epoch_id):
    # Convert Spark DataFrame to Pandas DataFrame
    pandas_df = df.toPandas()
    # Perform a simple operation on the Pandas DataFrame
    print(pandas_df.head())  # Just print the first few rows for demonstration

def main():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("KafkaSparkStructuredStreaming") \
        .getOrCreate()

    # Set log level to WARN
    #spark.sparkContext.setLogLevel("WARN")

    # Enable Arrow-based columnar data transfers
    spark.conf.set("spark.sql.execution.arrow.enabled", "true")

    # Create a DataFrame representing the stream of input lines from Kafka
    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "crypto.cryptocompare") \
        .load()
    
    # Cast the value column as String
    string_df = kafka_df.selectExpr("CAST(value AS STRING)")

    # Here you would typically have your transformations, for example:
    # transformed_df = string_df.withColumn("value", expr("some transformation"))

    # Write the results of each batch using `foreachBatch`
    query = string_df \
        .writeStream \
        .foreachBatch(foreach_batch_function) \
        .start()
    
    # Wait for the streaming to finish
    query.awaitTermination()
    
    
    


    
