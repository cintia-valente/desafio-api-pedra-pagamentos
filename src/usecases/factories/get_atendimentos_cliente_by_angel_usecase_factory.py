import os
from infrastructure.data.atendimento_repository import AtendimentoRepository
from infrastructure.db.database import connect_to_database
from usecases.atendimento.get_atendimentos.get_atendimentos_cliente_by_angel_usecase import GetAtendimentosClienteByAngelUseCase


class GetAtendimentosClienteByAngelUseCaseFactory:

    @staticmethod
    def create() -> GetAtendimentosClienteByAngelUseCase:
        conn = connect_to_database(os.getenv("DATABASE_URL"))
        atendimento_repository = AtendimentoRepository(conn)
        return GetAtendimentosClienteByAngelUseCase(atendimento_repository)

    
