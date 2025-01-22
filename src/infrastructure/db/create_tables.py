import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

load_dotenv()

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
                id_atendimento INTEGER PRIMARY KEY,
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
