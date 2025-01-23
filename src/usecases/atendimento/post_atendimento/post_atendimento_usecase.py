from domain.___seedwork.use_case_interface import UseCaseInterface
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from domain.atendimento.atendimento_entity import Atendimento
from usecases.atendimento.post_atendimento.post_atendimento_input_dto import PostAtendimentoInputDto
from usecases.atendimento.post_atendimento.post_atendimento_output_dto import PostAtendimentoOutputDto

class PostAtendimentoUseCase(UseCaseInterface):

    def __init__(self, atendimento_repository: AtendimentoRepositoryInterface):
        self.atendimento_repository = atendimento_repository

    def execute(self, atendimento: PostAtendimentoInputDto) -> PostAtendimentoOutputDto:
       atendimento = Atendimento(
          id_atendimento= atendimento.id_atendimento,
          id_cliente=atendimento.id_cliente,
          angel=atendimento.angel,
          polo=atendimento.polo,
          data_limite=atendimento.data_limite,
          data_de_atendimento=atendimento.data_de_atendimento)
       
       saved_atendimento = self.atendimento_repository.post_atendimento(atendimento=atendimento)

       return PostAtendimentoOutputDto(
          id_atendimento=saved_atendimento.id_atendimento,
          id_cliente=saved_atendimento.id_cliente,
          angel=saved_atendimento.angel,
          polo=saved_atendimento.polo,
          data_limite=saved_atendimento.data_limite,
          data_de_atendimento=saved_atendimento.data_de_atendimento
       )