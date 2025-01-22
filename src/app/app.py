from flask import Flask, request
import psycopg2
from infrastructure.data.atendimento_repository import AtendimentoRepository
from usecases.atendimento.post_atendimento.post_atendimento_input_dto import PostAtendimentoInputDto
from usecases.factories.post_atendimento_usecase_factory import PostAtendimentoUseCaseFactory
from dotenv import load_dotenv
import os
from flasgger import Swagger

app = Flask(__name__)

swagger = Swagger(app)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def db_connection():
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        conn = psycopg2.connect(database_url)
        return conn

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def create_post_atendimento_usecase():
    conn = db_connection()
    atendimento_repository = AtendimentoRepository(conn)
    return PostAtendimentoUseCaseFactory.create(atendimento_repository)

@app.route('/atendimentos', methods=['POST'])
def postAtendimento():
    """
    This is the POST API endpoint.
    ---
    responses:
      200:
        description: A hello world message
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Hello, World!"
    """
    data = request.get_json()

    input_dto = PostAtendimentoInputDto(**data)
    use_case = create_post_atendimento_usecase()
    output_dto = use_case.execute(input_dto)

    return {"id_atendimento": output_dto.id_atendimento}, 201

if __name__ == '__main__':
    app.run(host='0.0.0.0')
