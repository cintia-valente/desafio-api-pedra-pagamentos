import logging
from typing import List
from domain.atendimento.atendimento_entity import Atendimento

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def format_atendimentos(atendimentos: List[Atendimento]) -> List[dict]:
    try:
        result = [
            {
                "id_atendimento": atendimento.id_atendimento,
                "id_cliente": atendimento.id_cliente,
                "angel": atendimento.angel,
                "polo": atendimento.polo,
                "data_limite": atendimento.data_limite.strftime('%Y-%m-%d'),
                "data_de_atendimento": atendimento.data_de_atendimento.strftime('%Y-%m-%d')
            }
            for atendimento in atendimentos
        ]

        return result
    except Exception as e:
        logger.exception(f"Error formatting atendimentos: {str(e)}")
        raise