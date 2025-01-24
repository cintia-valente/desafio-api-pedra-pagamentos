from domain.___seedwork.use_case_interface import UseCaseInterface
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from domain.atendimento.atendimento_entity import Atendimento
from usecases.atendimento.dtos.atendimento_output_dto import AtendimentoOutputDto
from usecases.atendimento.dtos.put_atendimentos_dto.put_atendimento_input_dto import PutAtendimentoInputDto

class PutAtendimentoUseCase(UseCaseInterface):
    def __init__(self, atendimento_repository: AtendimentoRepositoryInterface):
        self.atendimento_repository = atendimento_repository

    def execute(self, atendimento_dto: int) -> AtendimentoOutputDto:
        atendimento = self.atendimento_repository.get_atendimento_by_id(atendimento_dto.id_atendimento)

        if not atendimento:
            raise Exception("Atendimento não encontrado")

        atendimento.id_cliente = atendimento_dto.id_cliente
        atendimento.angel = atendimento_dto.angel
        atendimento.polo = atendimento_dto.polo
        atendimento.data_limite = atendimento_dto.data_limite
        atendimento.data_de_atendimento = atendimento_dto.data_de_atendimento

        updated_atendimento = self.atendimento_repository.put_atendimento(atendimento)

        atendimentos_formatados = self.format_atendimentos(updated_atendimento)
    
        return {"atendimentos": atendimentos_formatados}, 200
    
    def format_atendimentos(self, atendimento):
        result = [
            {
                "id_atendimento": atendimento.id_atendimento,
                "id_cliente": atendimento.id_cliente,
                "angel": atendimento.angel,
                "polo": atendimento.polo,
                "data_limite": atendimento.data_limite.strftime('%Y-%m-%d'),
                "data_de_atendimento": atendimento.data_de_atendimento.strftime('%Y-%m-%d')
            }, 
        ]
        return result


