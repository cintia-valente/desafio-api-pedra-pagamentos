from domain.___seedwork.use_case_interface import UseCaseInterface
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from usecases.atendimento.dtos.get_atendimentos_dtos.get_atendimentos_cliente_by_angel_input_dto import GetAtendimentosClienteByAngelInputDto
from usecases.atendimento.dtos.atendimento_output_dto import AtendimentoOutputDto

class GetAtendimentosClienteByAngelUseCase(UseCaseInterface):

    def __init__(self, atendimento_repository: AtendimentoRepositoryInterface):
        self.atendimento_repository = atendimento_repository

    def execute(self, input_dto: GetAtendimentosClienteByAngelInputDto) -> list[AtendimentoOutputDto]:
        
        id_cliente = input_dto.id_cliente
        angel = input_dto.angel


        atendimentos = self.atendimento_repository.get_atendimentos_cliente_by_angel(id_cliente, angel)
       
        print(f"Atendimentos retornados: {atendimentos}") 
        
        if not atendimentos:
                return [] 
        
        return [
            AtendimentoOutputDto(
                id_atendimento=atendimento.id_atendimento,
                id_cliente=atendimento.id_cliente,
                angel=atendimento.angel,
                polo=atendimento.polo,
                data_limite=atendimento.data_limite,
                data_de_atendimento=atendimento.data_de_atendimento
            )

              for atendimento in atendimentos
        ]
        

    
    