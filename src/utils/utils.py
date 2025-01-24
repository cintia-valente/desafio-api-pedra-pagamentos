from typing import List

def format_atendimentos(atendimentos: List) -> List[dict]:
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
