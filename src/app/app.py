from flask import Flask, request
from usecases.atendimento.post_atendimento.post_atendimento_input_dto import PostAtendimentoInputDto
from usecases.factories.post_atendimento_usecase_factory import PostAtendimentoUseCaseFactory
from dotenv import load_dotenv
from flasgger import Swagger

app = Flask(__name__)

load_dotenv()

swagger = Swagger(app)

def create_post_atendimento_usecase():
    return PostAtendimentoUseCaseFactory.create()

@app.route('/atendimentos', methods=['POST'])
def postAtendimento():
    """
    Cria um novo atendimento.
    ---
    tags:
      - Atendimentos
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
        print(traceback.format_exc())  # Exibe a pilha de erros
        return {"error": "An unexpected error occurred"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
