from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, LongType, StringType

def main():
    # Initialize a Spark session
    spark = SparkSession.builder \
        .appName("KafkaSparkStream") \
        .getOrCreate()

    # Define Kafka parameters
    kafka_bootstrap_servers = 'broker:29092'
    kafka_topic = 'crypto.cryptocompare'

    # Create a DataFrame that streams data from Kafka
    kafkaStreamDF = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .load()

    # Define schemas
    # userSchema = StructType([
    #     StructField("registertime", LongType(), True),
    #     StructField("userid", StringType(), True),
    #     StructField("regionid", StringType(), True),
    #     StructField("gender", StringType(), True)
    # ])

    # Cast the value column as String
    kafkaStreamValuesDF = kafkaStreamDF.selectExpr("CAST(value AS STRING)")

    # Define a schema and use it to parse the JSON data
    # parsedDF = kafkaStreamValuesDF.select(from_json(col("value"), userSchema).alias("message"))

    # Output the parsed data to the console (for testing purposes)
    query = kafkaStreamValuesDF \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .trigger(processingTime='1 seconds') \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()


## cmd to submit the app to the spark cluster
# /opt/bitnami/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3 /app/spark_app.py
