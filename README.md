# Real-Time Data Streaming Project

# Overview:

This project demonstrates real-time data streaming using Apache Kafka and Apache Spark. It includes components for generating sample data, producing it to Kafka, and processing it using Spark Streaming. Docker is utilized for containerization, making deployment easier across different environments.

# Real-time streaming data architecture:

![Real-time streaming data architecture](https://github.com/Kaushik-Puttaswamy/Real-Time_Data_Streaming_Project/raw/main/Real-time%20streaming%20data%20architecture.png)


# Project Folder Structure:

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

├── Real-time streaming data architecture.png  # Diagram illustrating real-time streaming data architecture.

└── README.md                     # Project README providing an overview and instructions.

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

# Build the Docker Image:

Run the docker build command to build the Docker image from the Dockerfile.

```docker build -t custom-spark .```

# Verify the Image:

Verify that the image was created successfully by running:

```docker images```

# Start Docker Containers:

```docker-compose up -d```

This command will build and start the Docker containers defined in docker-compose.yml.

Command to display information about all containers managed by Docker Compose:

```docker-compose ps -a```

#  Verify Kafka Producer Logs:

After ensuring that all containers are successfully running, confirm whether the Kafka producer is generating messages by checking its logs.

```docker-compose logs kafka-producer```

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

command will select the keyspace named transaction_data for subsequent queries:

```USE transaction_data;```

command to describe a table named transaction_data_table within the keyspace transaction_data:

```DESCRIBE transaction_data_table;```

command selects all data from the table named transaction_data_table within the keyspace transaction_data:

```select * from transaction_data.transaction_data_table;```

command will give you the total count of rows in the table transaction_data_table:

```SELECT COUNT(*) FROM transaction_data_table;```

# Monitor Output:

# Monitor Kafka and Spark:

You can also monitor the data flow using Kafka’s Control Center and Spark’s Web UI. To access Kafka’s Control Center, navigate to http://localhost:9021. For Spark’s Web UI, navigate to http://localhost:8090.

# Additional Notes:

Make sure that Docker and Docker Compose are installed on your system.

**Manually Download the transaction_data.csv File**: Visit the `data` folder in this repository and download the `transaction_data.csv` file.

**Replace the Existing File**: After downloading, move or copy the downloaded `transaction_data.csv` file into the `data` folder of your local project directory, replacing the existing file.


# Contact:
Author: https://www.linkedin.com/in/kaushik-puttaswamy-317475148




