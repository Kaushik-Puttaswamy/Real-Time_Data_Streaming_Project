#!/usr/bin/env python3

from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, when, udf, current_timestamp, date_format, abs, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from cassandra.cluster import Cluster
import uuid
import logging
import time
import sys

#Pre-processing the data
# Function to configure logging
def configure_logging():
    """Configures logging for the script."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to clean categorical data
def clean_categorical_data(df, columns):
    """Cleans categorical data in the DataFrame."""
    for column in columns:
        df = df.withColumn(column, when(col(column).isNull(), "unknown").otherwise(col(column)))
    return df

# Function to clean numerical data
def clean_numerical_data(df, columns):
    """Cleans numerical data in the DataFrame."""
    for column in columns:
        df = df.withColumn(column, when(col(column).isNull(), lit(0)).otherwise(abs(col(column))))
    return df

# Function to clean transaction time data
def clean_transaction_time(df, column):
    """Cleans transaction time data in the DataFrame."""
    default_time = "Sun Jan 00 00:00:00 IST 0000"
    df = df.withColumn(column, when(col(column).isNull(), default_time).otherwise(col(column)))
    return df

# Function to generate UUID
def generate_uuid():
    """Generates a UUID."""
    return str(uuid.uuid4())

# Function to wait for Cassandra to be ready
def wait_for_cassandra():
    """Waits for Cassandra to be ready."""
    retries = 5
    delay = 10  # seconds

    while retries > 0:
        try:
            cluster = Cluster(['cassandra'])
            session = cluster.connect()
            session.execute("SELECT now() FROM system.local")  # A simple query to check Cassandra connectivity
            cluster.shutdown()
            return True
        except Exception as e:
            logging.error(f"Failed to connect to Cassandra: {e}")
            retries -= 1
            if retries > 0:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    
    logging.error("Failed to connect to Cassandra after retries, exiting...")
    return False

# Function to create Cassandra schema
def create_cassandra_schema():
    """Creates the Cassandra schema."""
    cluster = Cluster(['cassandra'])
    session = cluster.connect()

    keyspace_query = """
    CREATE KEYSPACE IF NOT EXISTS transaction_data 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    """
    session.execute(keyspace_query)

    session.set_keyspace('transaction_data')

    table_query = """
    CREATE TABLE IF NOT EXISTS transaction_data_table (
        id UUID PRIMARY KEY,
        user_id INT,
        transaction_id INT,
        transaction_time TEXT,
        item_code INT,
        item_description TEXT,
        number_of_items_purchased INT,
        cost_per_item DOUBLE,
        country TEXT,
        total_cost DOUBLE
    );
    """
    try:
        session.execute(table_query)
        logging.info("Table created successfully")
    except Exception as e:
        logging.error(f"Error creating table: {e}")

    cluster.shutdown()

#Aggregating the data
# Function to write to Cassandra
def write_to_cassandra(df, epoch_id):
    """Writes DataFrame to Cassandra."""
    create_cassandra_schema()

    df.select(
        col("id"),
        col("userid").alias("user_id"),
        col("transactionid").alias("transaction_id"),
        col("transactiontime").alias("transaction_time"),
        col("itemcode").alias("item_code"),
        col("itemdescription").alias("item_description"),
        col("numberofitemspurchased").alias("number_of_items_purchased"),
        col("costperitem").cast("double").alias("cost_per_item"),
        col("country"),
        (col("numberofitemspurchased") * col("costperitem").cast("double")).alias("total_cost")
    ).write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="transaction_data_table", keyspace="transaction_data") \
        .save()

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,com.datastax.spark:spark-cassandra-connector_2.12:3.5.0,org.apache.kafka:kafka-clients:3.7.0") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.cassandra.connection.port", "9042") \
    .getOrCreate()

# Configure logging
configure_logging()

# Check if Cassandra is ready before proceeding
if not wait_for_cassandra():
    sys.exit(1)  # Exit the script if Cassandra is not ready

# Kafka configuration
kafka_topic = "transaction_data"
kafka_bootstrap_servers = "broker:29092"

# Define CSV schema
csv_schema = StructType([
    StructField("userid", IntegerType()),
    StructField("transactionid", IntegerType()),
    StructField("transactiontime", StringType()),
    StructField("itemcode", IntegerType()),
    StructField("itemdescription", StringType()),
    StructField("numberofitemspurchased", IntegerType()),
    StructField("costperitem", StringType()),
    StructField("country", StringType())
])

# Read from Kafka stream
kafka_raw_data = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "earliest") \
    .load()

# Parse CSV data
parsed_data = kafka_raw_data \
    .selectExpr("CAST(value AS STRING) as csv_data") \
    .select(split("csv_data", ",").alias("csv_array"))

# Apply CSV schema
for i, field in enumerate(csv_schema.fields):
    parsed_data = parsed_data.withColumn(field.name, col("csv_array")[i].cast(field.dataType))

# Clean categorical and numerical data
categorical_columns = ["itemdescription", "country"]
numerical_columns = ["userid", "transactionid", "itemcode", "numberofitemspurchased"]

parsed_data = clean_categorical_data(parsed_data, categorical_columns)
parsed_data = clean_numerical_data(parsed_data, numerical_columns)

# Clean transaction time and generate UUID
parsed_data = clean_transaction_time(parsed_data, "transactiontime")
generate_uuid_udf = udf(generate_uuid, StringType())
parsed_data = parsed_data.withColumn("id", generate_uuid_udf())

# Write to Cassandra
parsed_query = parsed_data \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_cassandra) \
    .start()

# Wait for termination
parsed_query.awaitTermination()

# Stop Spark session
spark.stop()
