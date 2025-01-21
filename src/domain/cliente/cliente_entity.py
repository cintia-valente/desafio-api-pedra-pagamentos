from typing import List
from domain.atendimento.atendimento_entity import Atendimento


class Cliente:

    id_cliente: int
    atendimentos: List[Atendimento]

    def __init__(self, id_cliente: int,  atendimentos: List[Atendimento]):
        self.id_cliente = id_cliente,
        self.atendimentos = atendimentos if atendimentos else []
        

