from abc import ABC, abstractmethod
from domain.atendimento.atendimento_entity import Atendimento

class AtendimentoRepositoryInterface(ABC):

    @abstractmethod
    def post_atendimento(self, atendimento: Atendimento) -> Atendimento:
        pass
    
   