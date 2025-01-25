import logging
from domain.___seedwork.use_case_interface import UseCaseInterface
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from usecases.atendimento.dtos.atendimento_output_dto import AtendimentoOutputDto
from usecases.atendimento.dtos.get_atendimentos_dto.get_atendimentos_cliente_by_angel_input_dto import GetAtendimentosClienteByAngelInputDto
from utils.utils import format_atendimentos

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class GetAtendimentosClienteByAngelUseCase(UseCaseInterface):

    def __init__(self, atendimento_repository: AtendimentoRepositoryInterface):
        self.atendimento_repository = atendimento_repository

    def execute(self, input_dto: GetAtendimentosClienteByAngelInputDto) -> list[AtendimentoOutputDto]:
        try:
            id_cliente = input_dto.id_cliente
            angel = input_dto.angel

            atendimentos_cliente_by_angel = self.atendimento_repository.get_atendimentos_cliente_by_angel(id_cliente, angel)
        
            if not atendimentos:
                raise ValueError("Atendimentos not found for cliente {id_cliente} and angel {angel}")
            
            atendimentos= format_atendimentos(atendimentos_cliente_by_angel)
        
            return {"atendimentos": atendimentos}, 200
        
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return {"error": str(e)}, 404

        except Exception as e:
            logger.exception(f"Unexpected error while fetching atendimentos: {str(e)}")
            return {"error": "Error processing the request"}, 500
        
        