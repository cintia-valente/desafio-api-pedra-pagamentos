from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from usecases.atendimento.post_atendimento.post_atendimento_usecase import PostAtendimentoUseCase

class PostAtendimentoUseCaseFactory:

    @staticmethod
    def create(atendimento_repository: AtendimentoRepositoryInterface) -> PostAtendimentoUseCase:
        return PostAtendimentoUseCase(atendimento_repository)

    