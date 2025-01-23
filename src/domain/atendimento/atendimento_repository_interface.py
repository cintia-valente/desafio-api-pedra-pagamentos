from abc import ABC, abstractmethod
from domain.atendimento.atendimento_entity import Atendimento

class AtendimentoRepositoryInterface(ABC):

    @abstractmethod
    def post_atendimento(self, atendimento: Atendimento) -> Atendimento:
        pass
    
    @abstractmethod
    def get_atendimentos_by_id_cliente(self, id_cliente: int) -> list[Atendimento]:
        pass

    @abstractmethod
    def get_atendimentos_cliente_by_angel(self, id_cliente: int, angel: str) -> list[Atendimento]:
        pass

    