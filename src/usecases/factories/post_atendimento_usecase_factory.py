import os
from infrastructure.data.atendimento_repository import AtendimentoRepository
from infrastructure.db.database import connect_to_database
from usecases.atendimento.post_atendimento.post_atendimento_usecase import PostAtendimentoUseCase

class PostAtendimentoUseCaseFactory:

    @staticmethod
    def create() -> PostAtendimentoUseCase:
        conn = connect_to_database(os.getenv("DATABASE_URL"))
        atendimento_repository = AtendimentoRepository(conn)
        return PostAtendimentoUseCase(atendimento_repository)

    