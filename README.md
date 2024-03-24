# Real-Time Data Streaming Project

# Overview:

This project demonstrates real-time data streaming using Apache Kafka and Apache Spark. It includes components for generating sample data, producing it to Kafka, and processing it using Spark Streaming. Docker is utilized for containerization, making deployment easier across different environments.

# Folder Structure:

Real-Time_Data_Streaming_Project/

│

├── app/                           # Contains Python scripts for data generation, Kafka producing, logging configuration, and Spark streaming.

│   ├── data_generator.py          # Python script for generating sample data.

│   ├── kafka_producer.py          # Python script for producing data to Kafka.

│   ├── logging_config.py          # Configuration file for logging.

│   └── spark_streaming.py         # Python script for processing data using Spark Streaming.

│

├── data/                          # Holds the sample transaction data in CSV format.

│   └── transactions_data.csv

│

├── scripts/                       # Includes a shell script for handling dependencies.

│   └── wait-for-it.sh

│

├── docker-compose.yml            # Configuration file for Docker containers.

├── Dockerfile                    # Dockerfile for building containers.

├── requirements.txt              # Lists the project dependencies.

├── .env                          # Environment variables file.

└── .gitignore                    # Specifies intentionally untracked files to be ignored by Git.

# Implementation Steps:

# Clone the Repository:

To clone this repository, use the following command:

```git clone https://github.com/Kaushik-Puttaswamy/Real-Time_Data_Streaming_Project```

# Navigate to Project Directory:

Change directory to Real-Time_Data_Streaming_Project

```cd Real-Time_Data_Streaming_Project```

# Install Requirements:

Install dependencies listed in requirements.txt file

```pip install -r requirements.txt```

# Set Environment Variables:

Ensure that necessary environment variables are configured in the .env file.

# Start Docker Containers:

```docker-compose up -d```
This command will build and start the Docker containers defined in docker-compose.yml.

# Run the Scripts:

# Spark Streaming:

We will utilize Spark to consume the Kafka topic, perform transformations on the data, and subsequently write it to Cassandra. To execute the Spark job, run the following command in the project directory:

```docker-compose exec spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,com.datastax.spark:spark-cassandra-connector_2.12:3.5.0,org.apache.kafka:kafka-clients:3.7.0 /app/spark_stream.py```


# Cassandra:

To access the Cassandra shell, execute the following command in the project directory:

```docker-compose exec cassandra cqlsh```

You can then inspect the keyspace and table schema in Cassandra using CQL (Cassandra Query Language). You can utilize the following commands:

command to describes the keyspace named transaction_data:

```DESCRIBE transaction_data;```

command to selects the keyspace named transaction_data:

```USE transaction_data;```

command to describe a table named transaction_data_table within the keyspace transaction_data:

```DESCRIBE transaction_data_table;```

command selects all data from the table named transaction_data_table within the keyspace transaction_data:

```select * from transaction_data.transaction_data_table;```

You can also execute the following command to view the total data in the table:

```SELECT COUNT(*) FROM transaction_data_table;```

# Monitor Output:

# Monitor Kafka and Spark:

You can also monitor the data flow using Kafka’s Control Center and Spark’s Web UI. To access Kafka’s Control Center, navigate to http://localhost:9021. For Spark’s Web UI, navigate to http://localhost:8090.

# Additional Notes:

Make sure that Docker and Docker Compose are installed on your system.

# Contact:
Author: https://www.linkedin.com/in/kaushik-puttaswamy-317475148




