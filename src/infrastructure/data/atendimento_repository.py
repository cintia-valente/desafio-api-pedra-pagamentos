from domain.atendimento.atendimento_entity import Atendimento
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface


class AtendimentoRepository(AtendimentoRepositoryInterface):

    def __init__(self, session: Session):
        self.session = session

    def post_atendimento(self, atendimento: Atendimento):
        self.session.add(atendimento)
        self.session.commit()
        self.session.refresh(atendimento)

        return atendimento