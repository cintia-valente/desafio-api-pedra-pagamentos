import logging
from domain.___seedwork.use_case_interface import UseCaseInterface
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from domain.atendimento.atendimento_entity import Atendimento
from usecases.atendimento.dtos.atendimento_output_dto import AtendimentoOutputDto
from usecases.atendimento.dtos.post_atendimentos_dto.post_atendimento_input_dto import PostAtendimentoInputDto

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
class PostAtendimentoUseCase(UseCaseInterface):

   def __init__(self, atendimento_repository: AtendimentoRepositoryInterface):
      self.atendimento_repository = atendimento_repository

   def execute(self, atendimento_dto: PostAtendimentoInputDto) -> AtendimentoOutputDto:
      try:
         atendimento = Atendimento(
            id_atendimento= atendimento_dto.id_atendimento,
            id_cliente=atendimento_dto.id_cliente,
            angel=atendimento_dto.angel,
            polo=atendimento_dto.polo,
            data_limite=atendimento_dto.data_limite,
            data_de_atendimento=atendimento_dto.data_de_atendimento)
         
         saved_atendimento = self.atendimento_repository.post_atendimento(atendimento=atendimento)
         
      except Exception as e:
            logger.exception(f"Unexpected error while fetching atendimentos: {str(e)}")
            return {"error": "Error processing the request"}, 500
      
      return AtendimentoOutputDto(
         id_atendimento=saved_atendimento.id_atendimento,
         id_cliente=saved_atendimento.id_cliente,
         angel=saved_atendimento.angel,
         polo=saved_atendimento.polo,
         data_limite=saved_atendimento.data_limite,
         data_de_atendimento=saved_atendimento.data_de_atendimento
      )