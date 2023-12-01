import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import (
    from_json,
    col,
    regexp_replace,
    udf,
    explode,
    split,
    lit,
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    FloatType,
    DoubleType,
    TimestampType,
    ArrayType,
)

database_url = "jdbc:postgresql://postgres:5432/crypto_viz"
properties = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "driver": "org.postgresql.Driver",
}


def main():
    # Initialize a Spark session
    # (https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.html#)
    spark = (
        SparkSession.builder.appName("KafkaSparkStream")
        .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-jdbc.jar")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # Define Kafka parameters
    kafka_bootstrap_servers = "broker:29092"
    kafka_topic = "crypto.cryptocompare"

    # Define a SparkStreamReader
    # (https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamReader.html#pyspark.sql.streaming.DataStreamReader)
    kafka_stream_reader = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
        .option("subscribe", kafka_topic)
    )

    # Generate DataFrame from the Stream
    # (https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html#pyspark.sql.DataFrame)
    # +------------------+------------------+---- SHAPE OF THE DATA -----+---------------------+-------------+
    # | key              | value            | topic   |partition| offset | timestamp           |timestampType|
    # +------------------+------------------+---------+---------+--------+---------------------+-------------+
    # | [binary key]     | [binary value]   | "topic1"|   0     | 123    | 2021-01-01 10:00:00 |      0      |
    # +------------------+------------------+---------+---------+--------+---------------------+-------------+
    kafka_df = kafka_stream_reader.load()

    # SCHEMAS
    # Define the schema of the inner JSON objects in the "data" array
    data_schema = ArrayType(
        StructType(
            [
                StructField("place", StringType()),
                StructField("name", StringType()),
                StructField("price", StringType()),
                StructField("volume", StringType()),
                StructField("top_tier_volume", StringType()),
                StructField("market_cap", StringType()),
                StructField("percentage_change", StringType()),
            ]
        )
    )
    # Define schema of your JSON data
    json_schema = StructType(
        [StructField("timestamp", TimestampType()), StructField("data", data_schema)]
    )

    # Convert binary "value" column to string and parse JSON
    # +------------ SHAPE OF THE DATA ----------+
    # | parsed_data                             |
    # +-----------------------------------------+
    # | {timestamp: "2021-01-01 10:00:00",      |
    # |  data: {field1: "value1", field2: 100}} |
    # +-----------------------------------------+
    parsed_df = kafka_df.select(
        from_json(col("value").cast("string"), json_schema).alias("parsed_data")
    )

    # Explode the nested JSON array into individual columns
    # +------------ SHAPE OF THE DATA -----------+------------+
    # | timestamp              | data                         |
    # +------------------------+------------------------------+
    # | "2021-01-01 10:00:00"  | {name:"A", field1:"", ...},  |
    # +-------------------------------------------------------+
    # | "2021-01-01 10:00:00"  | {name:"B"m field1:"", ...},  |
    # +-------------------------------------------------------+
    exploded_df = parsed_df.select(
        col("parsed_data.timestamp"), explode(col("parsed_data.data")).alias("data")
    )

    # Explode the array into individual rows
    # +------------ SHAPE OF THE DATA -----------+-----------+
    # | timestamp              |  Name           |...        |
    # +------------------------+-----------------+-----------+
    # | "2021-01-01 10:00:00"  | A               | ...,      |
    # +------------------------------------------------------+
    # | "2021-01-01 10:00:00"  | B               | ...,      |
    # +------------------------------------------------------+
    # Flatten the DataFrame
    flattened_df = exploded_df.select(
        "timestamp",
        col("data.place").alias("place"),
        col("data.name").alias("name"),
        col("data.price").alias("price"),
        col("data.volume").alias("volume"),
        col("data.top_tier_volume").alias("top_tier_volume"),
        col("data.market_cap").alias("market_cap"),
        col("data.percentage_change").alias("percentage_change"),
    )
    # .explain(True)

    # +--------------------+-----+--------------------+--------+--------+--------------------+--------------------+-----------------+
    # |           timestamp|place|                name|   price|  volume|     top_tier_volume|          market_cap|percentage_change|
    # +--------------------+-----+--------------------+--------+--------+--------------------+--------------------+-----------------+
    # |2023-11-30 14:00:...|    1|        Bitcoin\nBTC|37730.93|  9.04E9|              4.94E9|            7.379E11|             0.28|
    # |2023-11-30 14:00:...|    2|       Ethereum\nETH| 2035.45|  4.16E9|2.0099999999999998E9|           2.4474E11|             0.94|
    # +--------------------+-----+--------------------+--------+--------+--------------------+--------------------+-----------------+

    # clean and format data
    cleaned_df = format_cryptocompare(flattened_df)
    cleaned_df.printSchema()

    # save to DB
    save_cryptocompare(spark, cleaned_df)

    # Display data in console
    # query = cleaned_df.writeStream.outputMode("update").format("console").start()

    # query = cleaned_df.writeStream.foreachBatch(foreach_batch_function).start()
    cleaned_df.printSchema()

    query = (cleaned_df.writeStream
             .outputMode("update")
             .format('jdbc')
             #.trigger(processingTime="1 seconds")
             .foreachBatch(foreach_batch_function)
             .start())

    # query = (cleaned_df.writeStream
    #          .outputMode("update")
    #          .format("console")
    #          #.trigger(processingTime="1 seconds")
    #          .foreachBatch(foreach_batch_function)
    #          .start())
    query.awaitTermination()
    spark.stop() # stop session
    spark.stop()  # stop session


#     return df
def format_cryptocompare(df):
    # format M and B to real numbers
    def convert_value(val: str):
        if val is None:
            return None
        val = val.replace(",", "").upper()  # remove "," and uppercase letts
        if val.endswith("B"):
            return float(val.replace("B", "")) * 1e9  # billions (milliards)
        elif val.endswith("M"):
            return float(val.replace("M", "")) * 1e6  # millions
        else:
            return float(val)  # convert directly

    try:
        convert_udf = udf(convert_value, DoubleType())

        #  replaces all characters in the "price" column that are not digits, dots, 'M', or 'B' with an empty string
        df = (
            df.withColumn("price", regexp_replace("price", "[^\d.MB]", ""))
            .withColumn("volume", regexp_replace("volume", "[^\d.MB]", ""))
            .withColumn(
                "top_tier_volume", regexp_replace("top_tier_volume", "[^\d.MB]", "")
            )
            .withColumn("market_cap", regexp_replace("market_cap", "[^\d.MB]", ""))
            .withColumn(
                "percentage_change", regexp_replace("percentage_change", "[^\d.MB]", "")
            )
        )

        # format M and B to real numbers
        df = (
            df.withColumn("price", convert_udf(col("price")))
            .withColumn("volume", convert_udf(col("volume")))
            .withColumn("top_tier_volume", convert_udf(col("top_tier_volume")))
            .withColumn("market_cap", convert_udf(col("market_cap")))
            .withColumn(
                "percentage_change", col("percentage_change").cast(DoubleType())
            )
        )

        # Split crypto_name and it's symbol into another col
        splited = split(df['name'], '\\n')
        df = df.withColumn('symbol', splited.getItem(1))
        df = df.withColumn('name', splited.getItem(0))

        # Convert place to integer
        df = df.withColumn('place', col("place").cast(IntegerType))
        
    except Exception as e:
        print(e)  # crash with empty dataframe

    return df


def save_cryptocompare(spark, df):
    cryptocompare_schema = StructType([
        StructField("timestamp", TimestampType()),
        StructField("name", StringType()),
        StructField("symbol", StringType()),
        StructField("place", IntegerType()),
        StructField("price", DoubleType()),
        StructField("volume", DoubleType()),
        StructField("top_tier_volume", DoubleType()),
        StructField("market_cap", DoubleType()),
        StructField("percentage_change", DoubleType())
    ])

    table_name = "cryptocompare"
    try:
        df_existing = spark.read.jdbc(
            url=database_url, table=table_name, properties=properties
        )
    except:
        # creates the table if the table doesn't exist
        df_schema = spark.createDataFrame([], cryptocompare_schema)
        df_schema.write.jdbc(url=database_url, table=table_name, mode='overwrite', properties=properties)
    

def foreach_batch_function(df, epoch_id):
    # before inserting, check if df is not empty
    #if df.head(1):
    table_name = "cryptocompare"
    df.write.jdbc(url=database_url, table=table_name, mode='append', properties=properties)
    print('success')


if __name__ == "__main__":
    main()


## cmd to submit the app to the spark cluster
# /opt/bitnami/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3 /app/spark_app.py
