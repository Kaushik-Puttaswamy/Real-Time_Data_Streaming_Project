import pandas as pd
import asyncio
import random
import os
import logging
from logging_config import configure_logging

# Configure logging
configure_logging()

# Define paths
dir_path = os.path.dirname(os.path.realpath(__file__))
project_root_path = os.path.dirname(dir_path)
dataset_path = os.path.join(project_root_path, 'data', 'transaction_data.csv')

async def fetch_random_record(data):
    """
    Asynchronously fetches random records from a DataFrame.

    Args:
        data (pandas.DataFrame): The DataFrame containing the data.

    Yields:
        pandas.Series: A random record from the DataFrame.

    """
    try:
        while True:
            rand_index = random.randint(0, data.shape[0] - 1)
            record = data.iloc[rand_index]
            await asyncio.sleep(5)  # Wait for 5 seconds
            yield record
    except asyncio.CancelledError:
        logging.info("Task was cancelled.")
    except IndexError as e:
        logging.error(f"An error occurred in fetch_random_record: {e}")

async def print_records(data):
    """
    Asynchronously prints records fetched from the DataFrame.

    Args:
        data (pandas.DataFrame): The DataFrame containing the data.

    """
    try:
        async for record in fetch_random_record(data):
            record_str = ','.join(map(str, record.values))
            logging.info(record_str)
    except Exception as e:
        logging.error(f'An error occurred in print_records: {e}')

def get_dataset(filepath=None):
    """
    Reads a CSV file into a pandas DataFrame.

    Args:
        filepath (str, optional): The path to the CSV file. Defaults to None.

    Returns:
        pandas.DataFrame or None: The DataFrame containing the data, or None if an error occurs.
        
    """
    filepath = filepath if filepath is not None else dataset_path
    if os.path.exists(filepath):
        try:
            col_types = {27: str}
            return pd.read_csv(filepath, dtype=col_types)
        except pd.errors.ParserError as e:
            logging.error(f"An error occurred in get_dataset. Failed to read {filepath}: {e}")
            return None
    else:
        logging.error(f"An error occurred in get_dataset: {filepath} does not exist")
        return None

if __name__ == '__main__':
    data = get_dataset()
    if data is None:
        logging.info(f"No dataset was found")
    else:
        try:
            asyncio.run(print_records(data))
        except KeyboardInterrupt:
            logging.info("Program was cancelled by user.")
