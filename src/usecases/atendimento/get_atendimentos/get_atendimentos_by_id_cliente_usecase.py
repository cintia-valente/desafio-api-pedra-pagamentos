import logging
from domain.___seedwork.use_case_interface import UseCaseInterface
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from usecases.atendimento.dto.atendimento_output_dto import AtendimentoOutputDto
from usecases.atendimento.dto.get_atendimentos_dto.get_atendimentos_by_cliente_input_dto import GetAtendimentosByClienteInputDto
from utils.utils import format_atendimentos

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
class GetAtendimentosByIdClienteUseCase(UseCaseInterface):

    def __init__(self, atendimento_repository: AtendimentoRepositoryInterface):
        self.atendimento_repository = atendimento_repository

    def execute(self, id_cliente_dto: GetAtendimentosByClienteInputDto) -> list[AtendimentoOutputDto]:
        id_cliente = id_cliente_dto.id_cliente
        
        atendimentos = self.atendimento_repository.get_atendimentos_by_id_cliente(id_cliente)

        
        if not atendimentos:
            raise ValueError("Atendimentos not found.")
        
        atendimentos_formatados = format_atendimentos(atendimentos)
    
        return {"atendimentos": atendimentos_formatados}, 200
    
        

    
    