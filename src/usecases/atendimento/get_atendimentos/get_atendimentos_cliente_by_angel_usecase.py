from domain.___seedwork.use_case_interface import UseCaseInterface
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from usecases.atendimento.get_atendimentos.dtos.get_atendimentos_cliente_by_angel_input_dto import GetAtendimentosClienteByAngelInputDto
from usecases.atendimento.get_atendimentos.dtos.get_atendimentos_output_dto import GetAtendimentosOutputDto

class GetAtendimentosClienteByAngelUseCase(UseCaseInterface):

    def __init__(self, atendimento_repository: AtendimentoRepositoryInterface):
        self.atendimento_repository = atendimento_repository

    def execute(self, input_dto: GetAtendimentosClienteByAngelInputDto) -> list[GetAtendimentosOutputDto]:
        
        id_cliente = input_dto.id_cliente
        angel = input_dto.angel


        atendimentos = self.atendimento_repository.get_atendimentos_cliente_by_angel(id_cliente, angel)
       
        print(f"Atendimentos retornados: {atendimentos}") 
        
        if not atendimentos:
                return [] 
        
        return [
            GetAtendimentosOutputDto(
                id_atendimento=atendimento.id_atendimento,
                id_cliente=atendimento.id_cliente,
                angel=atendimento.angel,
                polo=atendimento.polo,
                data_limite=atendimento.data_limite,
                data_de_atendimento=atendimento.data_de_atendimento
            )

              for atendimento in atendimentos
        ]
        

    
    