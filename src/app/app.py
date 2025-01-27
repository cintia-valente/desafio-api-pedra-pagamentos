import os
import psycopg2
from venv import logger
from flask import Flask, jsonify, request

from infrastructure.db.database import connect_to_database
from usecases.atendimento.dtos.get_atendimentos_dto.get_atendimentos_by_cliente_input_dto import GetAtendimentosByClienteInputDto
from usecases.atendimento.dtos.get_atendimentos_dto.get_atendimentos_cliente_by_angel_input_dto import GetAtendimentosClienteByAngelInputDto
from usecases.atendimento.dtos.post_atendimentos_dto.post_atendimento_input_dto import PostAtendimentoInputDto
from usecases.atendimento.dtos.put_atendimentos_dto.put_atendimento_input_dto import PutAtendimentoInputDto
from usecases.factories.post_atendimento_usecase_factory import PostAtendimentoUseCaseFactory
from usecases.factories.get_atendimentos_cliente_by_angel_usecase_factory import  GetAtendimentosClienteByAngelUseCaseFactory
from usecases.factories.get_atendimentos_by_id_cliente_usecase_factory import GetAtendimentosByIdClienteUseCaseFactory
from usecases.factories.put_atendimento_usecase_factory import PutAtendimentoUseCaseFactory
from dotenv import load_dotenv
from flasgger import Swagger
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from utils.auth import check_password, hash_password

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('TOKEN')
jwt = JWTManager(app)

load_dotenv()

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API com JWT",
        "description": "Exemplo de autenticação JWT no Swagger",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Token JWT no formato 'Bearer <seu-token>'"
        }
    },
    "security": [
        {"BearerAuth": []}
    ]
})

@app.route('/usuarios/registrar', methods=['POST'])
def post_usuario():
    """
    Cria um usuário.
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            usuario:
              type: string
              description: usuário
            senha:
              type: string
              description: senha
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            access_token:
              type: string
      400:
        description: Username and password are required
      409:
        description: Invalid credentials
      500:
        description: Internal server error
    """
    
    username = request.json.get('usuario', None)
    password = request.json.get('senha', None)

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400
    
    hashed_pw = hash_password(password)

    try:
      database_url = os.getenv('DATABASE_URL')
      conn = connect_to_database(database_url)

      with conn.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", (username, hashed_pw))
      
      conn.commit()
      
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({"msg": "Username already exists"}), 409
    
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        return jsonify({"msg": "Internal server error"}), 500

    finally:
        if conn:
          conn.close()

    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Realiza o login de um usuário.
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            usuario:
              type: string
            senha:
              type: string
    responses:
      200:
        description: Login successfully
        schema:
          type: object
          properties:
            access_token:
              type: string
      400:
        description: Username and password are required
      401:
        description: Invalid credentials
      500:
        description: Internal server error
    """
    
    username = request.json.get('usuario', None)
    password = request.json.get('senha', None)

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    try:
        database_url = os.getenv('DATABASE_URL')
        conn = connect_to_database(database_url)

        with conn.cursor() as cursor:
            cursor.execute("SELECT senha FROM usuarios WHERE usuario = %s", (username,))
            result = cursor.fetchone()

        if not result:
            return jsonify({"msg": "Unauthorized"}), 401

        hashed_password = result[0]

        if not check_password(hashed_password, password):
            return jsonify({"msg": "Invalid username or password"}), 400

        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        logger.error(f"Error during login: {e}")
        return jsonify({"msg": "Internal server error"}), 500

    finally:
        conn.close()

@app.route('/atendimentos/registrar', methods=['POST'])
@jwt_required()
def post_atendimento():
    """
    Cria um novo atendimento.
    ---
    tags:
      - Atendimentos
    operationId: post_atendimento 
    parameters:
      - in: body
        name: atendimento
        required: true
        schema:
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
    responses:
      201:
        description: Successfully created service
    """

    data = request.get_json()

    try:
        
        input_dto = PostAtendimentoInputDto(**data)
        post_use_case_factory = PostAtendimentoUseCaseFactory.create()
        atendimento = post_use_case_factory.execute(input_dto)

        return jsonify({"id_atendimento": atendimento.id_atendimento}), 201
  
    except Exception as e:
        return {"error": "Existing id_atendimento"}, 500
    
@app.route('/atendimentos/<int:id_cliente>', methods=['GET'])
@jwt_required()
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
        type: integer
    responses:
      200:
        description: Customer service list
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
        description: Service not found
    """
    
    try:
        get_atendimentos_by_cliente_use_case_factory = GetAtendimentosByIdClienteUseCaseFactory.create()
        atendimentos_dto = GetAtendimentosByClienteInputDto(id_cliente=id_cliente)
        atendimentos = get_atendimentos_by_cliente_use_case_factory.execute(atendimentos_dto)
        
        return jsonify(atendimentos), 201

    except Exception as e:
        logger.exception(f"An unexpected error occurred while retrieving atendimento for {id_cliente}")
        return {"error": "An unexpected error occurred"}, 500
    
@app.route('/atendimentos/<int:id_cliente>/<string:angel>', methods=['GET'])
@jwt_required()
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
        type: integer
      - in: path
        name: angel
        required: true
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
        description: Service not found
    """
    try:
        get_cliente_by_angel_use_case_factory = GetAtendimentosClienteByAngelUseCaseFactory.create()
        atendimentos_dto = GetAtendimentosClienteByAngelInputDto(id_cliente=id_cliente, angel=angel)
        atendimentos = get_cliente_by_angel_use_case_factory.execute(atendimentos_dto)
        
        return jsonify(atendimentos), 201

    except Exception as e:
        logger.exception(f"An unexpected error occurred while retrieving atendiemnto for {id_cliente} and angel {angel}")
        return {"error": "An unexpected error occurred"}, 500
    
@app.route('/atendimentos/atualizar/<int:id_atendimento>', methods=['PUT'])
@jwt_required()
def put_atendimento(id_atendimento):
    """
    Atualiza um atendimento.
    ---
    tags:
      - Atendimentos
    operationId: put_atendimento 
    parameters:
      - in: path
        name: id_atendimento
        required: true
        type: integer
      - in: body
        name: body
        required: true
        description: Atendimento (não inclui o campo id_atendimento no corpo)
        schema:
          type: object
          properties:
            id_cliente:
              type: integer
              description: ID do cliente
            angel:
              type: string
              description: Angel
            polo:
              type: string
              description: Polo
            data_limite:
              type: string
              format: date
              description: Data limite
            data_de_atendimento:
              type: string
              format: date
              description: Data do atendimento
    responses:
      200:
        description: Successfully updated service
    """

    data = request.get_json()

    if 'id_atendimento' in data:
        del data['id_atendimento']

    try:
        input_dto = PutAtendimentoInputDto(id_atendimento=id_atendimento, **data)
        put_use_case_factory = PutAtendimentoUseCaseFactory.create()
        atendimento = put_use_case_factory.execute(input_dto)

        return jsonify(atendimento), 201

    except Exception as e:
        return {"error": "Existing id_atendimento"}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True) 
