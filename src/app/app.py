from flask import Flask, request

from usecases.atendimento.dtos.get_atendimentos_dtos.get_atendimentos_by_cliente_input_dto import GetAtendimentosByClienteInputDto
from usecases.atendimento.dtos.get_atendimentos_dtos.get_atendimentos_cliente_by_angel_input_dto import GetAtendimentosClienteByAngelInputDto
from usecases.atendimento.dtos.post_atendimentos_dtos.post_atendimento_input_dto import PostAtendimentoInputDto
from usecases.atendimento.dtos.put_atendimentos_dto.put_atendimento_input_dto import PutAtendimentoInputDto
from usecases.factories.post_atendimento_usecase_factory import PostAtendimentoUseCaseFactory
from usecases.factories.get_atendimentos_cliente_by_angel_usecase_factory import  GetAtendimentosClienteByAngelUseCaseFactory
from usecases.factories.get_atendimentos_by_id_cliente_usecase_factory import GetAtendimentosByIdClienteUseCaseFactory
from dotenv import load_dotenv
from flasgger import Swagger
from usecases.factories.put_atendimento_usecase_factory import PutAtendimentoUseCaseFactory

app = Flask(__name__)

load_dotenv()

swagger = Swagger(app)

def create_post_atendimento_usecase():
    return PostAtendimentoUseCaseFactory.create()

@app.route('/atendimentos/registrar', methods=['POST'])
def post_atendimento():
    """
    Cria um novo atendimento.
    ---
    tags:
      - Atendimentos
    operationId: post_atendimento 
    parameters:
      - in: body
        name: body
        required: true
        description: Atendimento payload
        schema:
          type: object
    responses:
      201:
        description: Atendimento criado
    """

    data = request.get_json()
    required_fields = ["id_cliente", "angel", "polo", "data_limite", "data_de_atendimento"]
    for field in required_fields:
        if field not in data:
            return {"error": f"'{field}' is required"}, 400

    try:
        input_dto = PostAtendimentoInputDto(**data)
        use_case = create_post_atendimento_usecase()
        output_dto = use_case.execute(input_dto)
        return {"id_atendimento": output_dto.id_atendimento}, 201

    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc()) 
        return {"error": "An unexpected error occurred"}, 500
    
@app.route('/atendimentos/<int:id_cliente>', methods=['GET'])
def get_atendimentos_by_id_cliente(id_cliente):
    """
    Obtém todos os atendimentos de um cliente pelo seu ID.
    ---
    tags:
      - Atendimentos
    operationId: get_atendimentos_by_id_cliente 
    parameters:
      - in: path
        name: id_cliente
        required: true
        description: ID do cliente
        type: integer
    responses:
      200:
        description: Lista de atendimentos do cliente
        schema:
          type: array
          items:
            type: object
            properties:
              id_atendimento:
                type: integer
              id_cliente:
                type: integer
              angel:
                type: string
              polo:
                type: string
              data_limite:
                type: string
                format: date
              data_de_atendimento:
                type: string
                format: date
      404:
        description: Atendimento não encontrado
    """
    
    try:
        use_case = GetAtendimentosByIdClienteUseCaseFactory.create()
        atendimentos_dto = GetAtendimentosByClienteInputDto(id_cliente=id_cliente)

        atendimentos = use_case.execute(atendimentos_dto)
        
        if not atendimentos_dto:
            return {"error": "Atendimentos not found"}, 404
        
        result = [
            {
                "id_atendimento": atendimento.id_atendimento,
                "id_cliente": atendimento.id_cliente,
                "angel": atendimento.angel,
                "polo": atendimento.polo,
                "data_limite": atendimento.data_limite.strftime('%Y-%m-%d'),
                "data_de_atendimento": atendimento.data_de_atendimento.strftime('%Y-%m-%d')
            }
            for atendimento in atendimentos
        ]
        
        return {"atendimentos": result}, 200

    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc()) 
        return {"error": "An unexpected error occurred"}, 500
    
@app.route('/atendimentos/<int:id_cliente>/<string:angel>', methods=['GET'])
def get_atendimentos_by_cliente_and_angel(id_cliente, angel):
    """
    Obtém todos os atendimentos de um cliente realizados por um angel.
    ---
    tags:
      - Atendimentos
    operationId: get_atendimentos_by_cliente_and_angel 
    parameters:
      - in: path
        name: id_cliente
        required: true
        description: ID do cliente
        type: integer
      - in: path
        name: angel
        required: true
        description: angel
        type: string
    responses:
      200:
        description: Lista de atendimentos do cliente
        schema:
          type: array
          items:
            type: object
            properties:
              id_atendimento:
                type: integer
              id_cliente:
                type: integer
              angel:
                type: string
              polo:
                type: string
              data_limite:
                type: string
                format: date
              data_de_atendimento:
                type: string
                format: date
      404:
        description: Atendimento não encontrado
    """
    try:
        use_case = GetAtendimentosClienteByAngelUseCaseFactory.create()

        atendimentos_dto = GetAtendimentosClienteByAngelInputDto(id_cliente=id_cliente, angel=angel)
        
        atendimentos = use_case.execute(atendimentos_dto)

        if not atendimentos:
            return {"error": "Atendimentos não encontrados"}, 404
        
        result = [
            {
                "id_atendimento": atendimento.id_atendimento,
                "id_cliente": atendimento.id_cliente,
                "angel": atendimento.angel,
                "polo": atendimento.polo,
                "data_limite": atendimento.data_limite.strftime('%Y-%m-%d'),
                "data_de_atendimento": atendimento.data_de_atendimento.strftime('%Y-%m-%d')
            }
            for atendimento in atendimentos
        ]
        
        return {"atendimentos": result}, 200

    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc()) 
        return {"error": "Ocorreu um erro inesperado"}, 500
    
@app.route('/atendimentos/atualizar/<int:id_atendimento>', methods=['PUT'])
def put_atendimento(id_atendimento):
    """
    Atualiza um atendimento existente.
    ---
    tags:
      - Atendimentos
    operationId: put_atendimento 
    parameters:
      - in: path
        name: id_cliente
        required: true
        description: ID do cliente
        type: integer
      - in: path
        name: angel
        required: true
        description: angel
        type: string
        - in: path
        name: polo
        required: true
        description: polo
        type: integer
      - in: path
        name: data_limite
        required: true
        description: data_limite
        type: string
      - in: path
        name: data_de_atendimento
        required: true
        description: data_de_atendimento
        type: string
    responses:
      200:
        description: Atendimento atualizado
    """
    data = request.get_json()
    
    # Verifica se id_atendimento está no corpo da requisição e remove-o, pois já vem da URL
    if 'id_atendimento' in data:
        del data['id_atendimento']

    required_fields = ["id_cliente", "angel", "polo", "data_limite", "data_de_atendimento"]
    for field in required_fields:
        if field not in data:
            return {"error": f"'{field}' is required"}, 400

    try:
        # Agora, somente o id_atendimento da URL é passado, sem conflitos
        input_dto = PutAtendimentoInputDto(id_atendimento=id_atendimento, **data)

        use_case = PutAtendimentoUseCaseFactory.create()
        output_dto = use_case.execute(input_dto)

        # Retorno dos dados atualizados
        return {
            "id_atendimento": output_dto.id_atendimento,
            "id_cliente": output_dto.id_cliente,
            "angel": output_dto.angel,
            "polo": output_dto.polo,
            "data_limite": output_dto.data_limite.strftime('%Y-%m-%d'),
            "data_de_atendimento": output_dto.data_de_atendimento.strftime('%Y-%m-%d')
        }, 200

    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc())
        return {"error": "An unexpected error occurred"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
