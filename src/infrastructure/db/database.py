import logging
import time
from dotenv import load_dotenv
import psycopg2
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

load_dotenv()

def connect_to_database(database_url, retries=5, delay=5):
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(database_url)
            logger.info("Database connection successful")

            return conn
        
        except Exception as e:
            logger.info(f"Attempt {attempt + 1} of {retries} failed: {e}")
            if attempt < retries - 1:
                logger.info(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            else:
                logger.info("Error connecting to the database after several attempts")
                raise
