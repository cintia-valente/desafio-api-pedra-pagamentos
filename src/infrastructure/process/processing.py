import logging
import os
from dotenv import load_dotenv
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

load_dotenv()

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

        file_path = '/app/infrastructure/data/bd_erros_de_conversao_datas.csv'
        error_df.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))
        logger.info(f"Conversion errors logged in 'bd_erros_de_conversao_datas.csv'")

    return df

def fetch_existing_data(conn, date_column):
    try:
        cur = conn.cursor()
        # Agora, a query é montada diretamente dentro do f-string
        query = f"SELECT DISTINCT {date_column} FROM atendimentos"
        cur.execute(query)  # Execute a consulta corretamente
        result = cur.fetchall()
        
        return [row[0] for row in result if row[0] is not None]
    except Exception as e:
        logger.error(f"Error fetching existing {date_column}: {e}")
        raise
