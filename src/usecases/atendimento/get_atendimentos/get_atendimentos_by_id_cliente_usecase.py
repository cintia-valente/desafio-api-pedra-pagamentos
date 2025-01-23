from domain.___seedwork.use_case_interface import UseCaseInterface
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from usecases.atendimento.get_atendimentos.get_atendimentos_by_id_cliente_input_dto import GetAtendimentosByIdClienteInputDto
from usecases.atendimento.get_atendimentos.get_atendimentos_by_id_cliente_output_dto import GetAtendimentosByIdClienteOutputDto

class GetAtendimentosByIdClienteUseCase(UseCaseInterface):

    def __init__(self, atendimento_repository: AtendimentoRepositoryInterface):
        self.atendimento_repository = atendimento_repository

    def execute(self, id_cliente_dto: GetAtendimentosByIdClienteInputDto) -> list[GetAtendimentosByIdClienteOutputDto]:
        id_cliente = id_cliente_dto.id_cliente
        
        atendimentos = self.atendimento_repository.get_atendimentos_by_id_cliente(id_cliente)

        print(f"Atendimentos retornados: {atendimentos}") 
        
        if not atendimentos:
                return [] 
        
        return [
            GetAtendimentosByIdClienteOutputDto(
                id_atendimento=atendimento.id_atendimento,
                id_cliente=atendimento.id_cliente,
                angel=atendimento.angel,
                polo=atendimento.polo,
                data_limite=atendimento.data_limite,
                data_de_atendimento=atendimento.data_de_atendimento
            )

              for atendimento in atendimentos
        ]
        

    
    