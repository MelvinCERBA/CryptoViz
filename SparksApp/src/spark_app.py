from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import from_json, col, regexp_replace, udf, explode
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, TimestampType, ArrayType

def main():
    # Initialize a Spark session
    spark = SparkSession.builder \
        .appName("KafkaSparkStream") \
        .getOrCreate()

    # Define Kafka parameters
    kafka_bootstrap_servers = 'broker:29092'
    kafka_topic = 'crypto.cryptocompare'

    # Read data from Kafka
    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .load()

    # Define the schema of the inner JSON objects in the "data" array
    # data_schema = ArrayType(StructType([
    #     StructField("place", StringType()),
    #     StructField("name", StringType()),
    #     StructField("price", StringType()),
    #     StructField("volume", StringType()),
    #     StructField("top_tier_volume", StringType()),
    #     StructField("market_cap", StringType()),
    #     StructField("percentage_change", StringType())
    # ]))

    # # Define schema of your JSON data
    # json_schema = StructType([
    #     StructField("timestamp", TimestampType()),
    #     StructField("data", data_schema)
    # ])

    # # Convert binary "value" column to string and parse JSON
    # parsed_df = kafka_df.select(from_json(col("value").cast("string"), json_schema).alias("parsed_data"))

    # # Explode the nested JSON array into individual rows
    # exploded_df = parsed_df.select("parsed_data.timestamp", explode("parsed_data.data").alias("data"))

    # # Flatten the DataFrame
    # flattened_df = exploded_df.select(
    #     "timestamp",
    #     col("data.place").alias("place"),
    #     col("data.name").alias("name"),
    #     col("data.price").alias("price"),
    #     col("data.volume").alias("volume"),
    #     col("data.top_tier_volume").alias("top_tier_volume"),
    #     col("data.market_cap").alias("market_cap"),
    #     col("data.percentage_change").alias("percentage_change")
    # )

    # print("FLATTENED DF:", flattened_df)
    # print()
    #foreach_batch_function(flattened_df)
    
    # Apply the cleaning function
    #cleaned_df = format_cryptocompare(flattened_df)

    #print("CLEANED_DF:\n", cleaned_df)

    # Output the parsed data to the console (for testing purposes)
    query = kafka_df \
        .writeStream \
        .outputMode("append") \
        .foreachBatch(foreach_batch_function)\
        .trigger(processingTime='1 seconds') \
        .start()
    
    #.format("console") \

    query.awaitTermination()

def foreach_batch_function(df, epoch_id):
    print("HELLO")
    # Print column names
    print("Columns:", df.columns)

    # Show the DataFrame contents (for demonstration purposes, limit the number of rows to print)
    df.show(truncate=False)


def format_cryptocompare(df):
        # format M and B to real numbers
        def convert_value(val: str):
            if val is None:
                return None
            val = val.replace(',', '').upper()  # remove "," and uppercase letts
            if val.endswith('B'):
                return float(val.replace('B', '')) * 1e9  # billions (milliards)
            elif val.endswith('M'):
                return float(val.replace('M', '')) * 1e6  # millions
            else:
                return float(val)  # convert directly
            
        convert_udf = udf(convert_value, DoubleType())
            
        df = df.withColumn("price", regexp_replace("price", "[^\d\.MB]", ""))\
                .withColumn("price", convert_udf(col("price")))
        df = df.withColumn("volume", regexp_replace("volume", "[^\d\.MB]", ""))\
                .withColumn("volume", convert_udf(col("volume")))
        df = df.withColumn("top_tier_volume", regexp_replace("top_tier_volume", "[^\d\.MB]", ""))\
                .withColumn("top_tier_volume", convert_udf(col("top_tier_volume")))
        df = df.withColumn("market_cap", regexp_replace("market_cap", "[^\d\.MB]", ""))\
                .withColumn("market_cap", convert_udf(col("market_cap")))
        df = df.withColumn("percentage_change", regexp_replace("percentage_change", "[^\d\.]", ""))\
                .withColumn("percentage_change", col("percentage_change").cast(DoubleType()))

        return df

if __name__ == "__main__":
    main()


## cmd to submit the app to the spark cluster
# /opt/bitnami/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3 /app/spark_app.py
