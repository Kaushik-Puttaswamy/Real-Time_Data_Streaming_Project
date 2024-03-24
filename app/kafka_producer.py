import os
import asyncio
import csv
import logging
from kafka import KafkaProducer
import kafka.errors
from logging_config import configure_logging
from data_generator import get_dataset, fetch_random_record  

configure_logging()

# Get the current directory path
dir_path = os.path.dirname(os.path.realpath(__file__))
# Get the project root directory path
project_root_path = os.path.dirname(dir_path)
# Define the data directory path
data_dir_path = os.path.join(project_root_path, 'data')

#Data ingestion
async def produce_kafka_messages(producer, data):
    """
    Asynchronously produce Kafka messages.

    Args:
        producer (KafkaProducer): Kafka producer instance.
        data: Data generator to produce Kafka messages.

    Returns:
        None
    """
    try:
        # Check if data is available
        if data is None:
            logging.error("No dataset found.")
            return

        # Iterate over randomly fetched records
        async for record in fetch_random_record(data):
            # Convert record to a comma-separated string
            message = ','.join(map(str, record))
            # Send the message to the Kafka topic
            producer.send("transaction_data", value=message)
            logging.info(f"Message sent: {message}")
            # Wait for 5 seconds
            await asyncio.sleep(5)
    except Exception as e:
        logging.error(f'An error occurred in produce_kafka_messages: {e}')

if __name__ == '__main__':
    # Get the dataset
    data_generator = get_dataset()
    # Check if dataset is available
    if data_generator is None:
        logging.info(f"No dataset was found")
    else:
        producer = None
        try:
            # Define Kafka broker address
            kafka_broker_address = 'broker:29092'  # Kafka broker address and port
            # Initialize Kafka producer
            producer = KafkaProducer(
                bootstrap_servers=kafka_broker_address,
                value_serializer=lambda v: str(v).encode('utf-8')
            )
            # Start producing Kafka messages asynchronously
            asyncio.run(produce_kafka_messages(producer, data_generator))
        except KeyboardInterrupt:
            logging.info("Program was cancelled by the user.")
        except kafka.errors.NoBrokersAvailable:
            logging.error("No Kafka brokers available. Check your configuration.")
        except FileNotFoundError as e:
            logging.error(f"File not found error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        finally:
            # Close the Kafka producer
            if producer:
                producer.close()
