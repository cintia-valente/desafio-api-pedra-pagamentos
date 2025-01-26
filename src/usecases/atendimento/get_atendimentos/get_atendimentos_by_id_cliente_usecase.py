import logging
from domain.___seedwork.use_case_interface import UseCaseInterface
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from usecases.atendimento.dtos.atendimento_output_dto import AtendimentoOutputDto
from usecases.atendimento.dtos.get_atendimentos_dto.get_atendimentos_by_cliente_input_dto import GetAtendimentosByClienteInputDto
from utils.format import format_atendimentos

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
class GetAtendimentosByIdClienteUseCase(UseCaseInterface):

    def __init__(self, atendimento_repository: AtendimentoRepositoryInterface):
        self.atendimento_repository = atendimento_repository

    def execute(self, id_cliente_dto: GetAtendimentosByClienteInputDto) -> list[AtendimentoOutputDto]:
        try:    
            id_cliente = id_cliente_dto.id_cliente
        
            atendimentos_by_id_cliente = self.atendimento_repository.get_atendimentos_by_id_cliente(id_cliente)

            if not atendimentos_by_id_cliente:
                raise ValueError(f"Atendimentos not found for cliente with id {id_cliente}")
            
            atendimentos = format_atendimentos(atendimentos_by_id_cliente)
            
            return {"atendimentos": atendimentos}, 200
        
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return {"error": str(e)}, 404

        except Exception as e:
            logger.exception(f"Unexpected error while fetching atendimentos: {str(e)}")
            return {"error": "Error processing the request"}, 500
        

    
    