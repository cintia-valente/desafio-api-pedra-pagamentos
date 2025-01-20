import logging
import os
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

def create_tables(conn):
    try:
        cur = conn.cursor()

        logger.info("Creating clients table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente SERIAL PRIMARY KEY
            );
        """)

        logger.info("Creating attendances table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS atendimentos (
                id_atendimento SERIAL PRIMARY KEY,
                id_cliente INTEGER REFERENCES clientes(id_cliente),
                angel VARCHAR(255),
                polo VARCHAR(255),
                data_limite DATE,
                data_de_atendimento TIMESTAMP
            );
        """)

        logger.info("Tables created successfully")
        conn.commit()

    except Exception as e:
        logger.error(f"Error while creating tables: {e}")
        conn.rollback()
        raise

def process_dates(df, date_columns):
    error_rows = []
    original_dates = df[date_columns].copy()

    for column in date_columns:
        try:
            if df[column].str.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$').any():
                df[column] = pd.to_datetime(df[column], format='%Y-%m-%d %H:%M:%S', errors='coerce', dayfirst=False)
            else:
                df[column] = pd.to_datetime(df[column], errors='coerce', dayfirst=True)
        
            invalid_dates = df[df[column].isna()]
            if not invalid_dates.empty:
                    error_rows.append(invalid_dates)

        except Exception as e:
            logger.error(f"Error processing date column {column}: {e}")      
            raise

    if error_rows:
        error_df = pd.concat(error_rows)
        for column in date_columns:
            error_df[f"original_{column}"] = original_dates[column] 

        file_path = '/src/data/bd_erros_de_conversao_datas.csv'
        error_df.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))
        logger.info(f"Conversion errors logged in 'bd_erros_de_conversao_datas.csv'")

    return df

def fetch_existing_data_limite(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT data_limite FROM atendimentos")
        result = cur.fetchall()
        
        return [row[0] for row in result if row[0] is not None]
    except Exception as e:
        logger.error(f"Error fetching existing data_limite: {e}")
        raise

def insert_data(conn, df, existing_data):
    try:
        cur = conn.cursor()

        existing_data = pd.to_datetime(existing_data, errors='coerce')
        df = df[~df['data_limite'].isin(existing_data)]

        if df.empty:
            print("No new rows to insert.")
            return

        df['data_de_atendimento'] = df['data_de_atendimento'].replace({pd.NaT: None})
        df.dropna(subset=['id_cliente', 'data_limite'], inplace=True)

        clientes_data = df[['id_cliente']].drop_duplicates()
        cur.executemany("""
            INSERT INTO clientes (id_cliente)
            VALUES (%s)
            ON CONFLICT (id_cliente) DO NOTHING;
        """, [(int(row['id_cliente']),) for _, row in clientes_data.iterrows()])

        atendimentos_data = df[['id_cliente', 'angel', 'polo', 'data_limite', 'data_de_atendimento']].drop_duplicates()
        cur.executemany("""
            INSERT INTO atendimentos (id_cliente, angel, polo, data_limite, data_de_atendimento)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id_atendimento) DO NOTHING;
        """, [tuple(row) for _, row in atendimentos_data.iterrows()])

        logger.info(f"{len(atendimentos_data)} records inserted into the 'atendimentos' table")
        conn.commit()

    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        conn.rollback()
        raise

def load_csv_in_chunks(csv_file, chunk_size=100000):
    try:
        return pd.read_csv(csv_file, delimiter=";", chunksize=chunk_size)
    except Exception as e:
        logger.error(f"Error reading CSV file {csv_file}: {e}")
        raise

def main():
    try:
        database_url = os.getenv('DATABASE_URL')

        if not database_url:
            raise ValueError("Database URL not provided in .env")

        conn = connect_to_database(database_url)
        create_tables(conn)

        existing_data = fetch_existing_data_limite(conn)
        print(f"Total of already processed dates: {len(existing_data)}")

        chunks = load_csv_in_chunks('/src/data/bd_desafio.csv')

        for i, df in enumerate(chunks):
            print(f"Processing chunk {i + 1} with {len(df)} records...")
            df = process_dates(df, ['data_limite', 'data_de_atendimento'])
            insert_data(conn, df, existing_data)

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