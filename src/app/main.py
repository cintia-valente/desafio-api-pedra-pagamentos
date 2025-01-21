from flask import Flask, request
import psycopg2
from infrastructure.data.atendimento_repository import AtendimentoRepository
from usecases.atendimento.post_atendimento.post_atendimento_input_dto import PostAtendimentoInputDto
from usecases.factories.post_atendimento_usecase_factory import PostAtendimentoUseCaseFactory
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def create_post_atendimento_usecase():
    conn = db_connection()
    atendimento_repository = AtendimentoRepository(conn)
    return PostAtendimentoUseCaseFactory.create(atendimento_repository)

@app.route('/atendimentos', methods=['POST'])
def postAtendimento():
    data = request.get_json()

    input_dto = PostAtendimentoInputDto(**data)
    use_case = create_post_atendimento_usecase()
    output_dto = use_case.execute(input_dto)

    return {"id_atendimento": output_dto.id_atendimento}, 201

if __name__ == '__main__':
    app.run(host='0.0.0.0')
