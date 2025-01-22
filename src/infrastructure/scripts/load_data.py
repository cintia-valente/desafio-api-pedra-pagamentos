import logging
from dotenv import load_dotenv
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

load_dotenv()

def load_csv_in_chunks(csv_file, chunk_size=100000):
    try:
        return pd.read_csv(csv_file, delimiter=";", chunksize=chunk_size)
    except Exception as e:
        logger.error(f"Error reading CSV file {csv_file}: {e}")
        raise