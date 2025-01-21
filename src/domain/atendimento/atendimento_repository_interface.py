from abc import ABC, abstractmethod
from domain.atendimento.atendimento_entity import Atendimento

class AtendimentoRepositoryInterface(ABC):

    @abstractmethod
    def post_atendimento(self, atendimento: Atendimento) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_atendimento_by_id_cliente(self, atendimento: Atendimento) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def put_atendimento(self, atendimento: Atendimento) -> None:
        raise NotImplementedError