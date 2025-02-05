import logging
from dotenv import load_dotenv
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

load_dotenv()

def insert_data(conn, df, existing_data):
    try:
        cur = conn.cursor()

        existing_data = pd.to_datetime(existing_data, errors='coerce')
        df = df[~df['data_limite'].isin(existing_data)]

        if df.empty:
            logger.info("No new rows to insert.")
            return
        
        df.copy()
        df['data_de_atendimento'] = df['data_de_atendimento'].replace({pd.NaT: None})
        df['data_limite'] = df['data_limite'].replace({pd.NaT: None})

        clientes_data = df[['id_cliente']].drop_duplicates()
        cur.executemany("""
            INSERT INTO clientes (id_cliente)
            VALUES (%s)
            ON CONFLICT (id_cliente) DO NOTHING;
        """, [(int(row['id_cliente']),) for _, row in clientes_data.iterrows()])

        atendimentos_data = df[['id_atendimento', 'id_cliente', 'angel', 'polo', 'data_limite', 'data_de_atendimento']].drop_duplicates()
        cur.executemany("""
            INSERT INTO atendimentos (id_atendimento, id_cliente, angel, polo, data_limite, data_de_atendimento)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_atendimento) DO NOTHING;
        """, [tuple(row) for _, row in atendimentos_data.iterrows()])

        logger.info(f"{len(atendimentos_data)} records inserted into the 'atendimentos' table")
        conn.commit()

    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        conn.rollback()
        raise

