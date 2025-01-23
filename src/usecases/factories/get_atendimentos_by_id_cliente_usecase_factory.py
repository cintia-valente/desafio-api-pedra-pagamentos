import os
from infrastructure.data.atendimento_repository import AtendimentoRepository
from infrastructure.db.database import connect_to_database
from usecases.atendimento.get_atendimentos.get_atendimentos_by_id_cliente_usecase import GetAtendimentosByIdClienteUseCase


class GetAtendimentosByIdClienteUseCaseFactory:

    @staticmethod
    def create() -> GetAtendimentosByIdClienteUseCase:
        conn = connect_to_database(os.getenv("DATABASE_URL"))
        atendimento_repository = AtendimentoRepository(conn)
        return GetAtendimentosByIdClienteUseCase(atendimento_repository)

    
