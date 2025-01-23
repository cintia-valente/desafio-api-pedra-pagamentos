import logging
import os
from dotenv import load_dotenv

from infrastructure.db.create_tables import create_tables
from infrastructure.db.database import connect_to_database
from infrastructure.db.insert_data import insert_data
from infrastructure.process.processing import fetch_existing_data, process_dates
from infrastructure.scripts.load_data import load_csv_in_chunks

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

load_dotenv()

def main():
    try:
        database_url = os.getenv('DATABASE_URL')

        if not database_url:
            raise ValueError("Database URL not provided in .env")

        conn = connect_to_database(database_url)
        create_tables(conn)

        existing_data_limite = fetch_existing_data(conn, 'data_limite')
        existing_data_atendimento = fetch_existing_data(conn, 'data_de_atendimento')
        
        logger.info(f"Total of already processed dates: {len(existing_data_limite)}")
        logger.info(f"Total of already processed dates: {len(existing_data_atendimento)}")

        chunks = load_csv_in_chunks('/app/infrastructure/data/bd_desafio.csv')

        for i, df in enumerate(chunks):
            logger.info(f"Processing chunk {i + 1} with {len(df)} records...")

            df = process_dates(df, ['data_limite', 'data_de_atendimento'])

            if df.empty:
                logger.info(f"Chunk {i + 1} has no new records to insert.")
                continue

            insert_data(conn, df, existing_data_limite + existing_data_atendimento)

    except Exception as e:
        logger.critical(f"Critical error in the main execution: {e}")

    finally:
        try:
            if conn:    
                conn.close()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing the connection: {e}")

if __name__ == "__main__":
    main()