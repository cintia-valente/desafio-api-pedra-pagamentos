import os
from infrastructure.data.atendimento_repository import AtendimentoRepository
from infrastructure.db.database import connect_to_database
from usecases.atendimento.put_atendimento.put_atendimento_usecase import PutAtendimentoUseCase

class PutAtendimentoUseCaseFactory:

    @staticmethod
    def create() -> PutAtendimentoUseCase:
        conn = connect_to_database(os.getenv("DATABASE_URL"))
        atendimento_repository = AtendimentoRepository(conn)
        return PutAtendimentoUseCase(atendimento_repository)
