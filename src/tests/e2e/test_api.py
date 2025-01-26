import requests
import uuid
import requests
from venv import logger
from utils.test_helpers import check_id_exists, generate_id_random

BASE_URL = "http://api:5000"
TEST_USER = {
    "usuario": f"user_{str(uuid.uuid4())}",
    "senha": "password123",
}

def test_post_usuario():
    """Must register a new 'usuario'"""
    response = requests.post(f"{BASE_URL}/usuarios/registrar", json=TEST_USER)

    if response.status_code == 409:
        logger.info("User already exists, using a different name")
      
    assert response.status_code in [201, 409], response.text 

def test_login():
    """Must login and check if the token is returned"""
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
   
    assert response.status_code == 200, response.text
    data = response.json()
   
    assert "access_token" in data, "Token not found"
    token = data["access_token"]
    assert token, "Token cannot be empty"

def test_post_atendimento():
    """Must register 'atendimento' after logging in and verifying the unique id"""
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
    assert response.status_code == 200, response.text
    data = response.json()

    assert "access_token" in data, "Token not found"
    token = data["access_token"]
    assert token, "Token cannot be empty"

    headers = {"Authorization": f"Bearer {token}"}

    id_atendimento = generate_id_random()
    while check_id_exists(id_atendimento):
        logger.info(f"Id {id_atendimento} already exists, generating another one...")
        id_atendimento = generate_id_random()
    
    atendimento_data = {
        "id_atendimento": id_atendimento,
        "id_cliente": 77226365,
        "angel": "Angel1",
        "polo": "São Paulo",
        "data_limite": "2025-01-30T00:00:00",
        "data_de_atendimento": "2025-01-25T00:00:00",
    }

    response = requests.post(
        f"{BASE_URL}/atendimentos/registrar", json=atendimento_data, headers=headers
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert "id_atendimento" in data, "Atendimento ID not found"


def test_get_atendimentos_by_cliente():
    """Must query 'atendimento' using id_cliente"""
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
    assert response.status_code == 200, response.text
    data = response.json()

    assert "access_token" in data, "Token not foundo"
    token = data["access_token"]
    assert token, "Token cannot be empty"

    headers = {"Authorization": f"Bearer {token}"}

    id_cliente = 77226365
    response = requests.get(
        f"{BASE_URL}/atendimentos/{id_cliente}", headers=headers
    )

    assert response.status_code == 201, response.text
    atendimentos = response.json()
    assert isinstance(atendimentos, list)

def test_get_atendimentos_by_cliente_and_angel():
    """Must consult 'cliente' 'atendimento' provided by an 'angel''"""
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
    assert response.status_code == 200, response.text
    data = response.json()

    assert "access_token" in data, "Token not found"
    token = data["access_token"]
    assert token, "Token cannot be empty"

    headers = {"Authorization": f"Bearer {token}"}

    id_cliente = 77226365
    
    angel = "Angel1"
    response = requests.get(
        f"{BASE_URL}/atendimentos/{id_cliente}/{angel}", headers=headers
    )

    assert response.status_code == 201, response.text
    atendimentos = response.json()
    assert isinstance(atendimentos, list)


def test_put_atendimento():
    """Must update a 'atendimento'"""
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
    assert response.status_code == 200, response.text
    data = response.json()

    assert "access_token" in data, "Token not found"
    token = data["access_token"]
    assert token, "Token cannot be empty"

    headers = {"Authorization": f"Bearer {token}"}

    id_atendimento = 667

    put_data = {
        "id_cliente": 968422633,
        "angel": "João Bandoli",
        "polo": "PR - CURITIBA",
        "data_limite": "2021-06-30T00:00:00",
        "data_de_atendimento": "2021-06-28T09:01:19",
    }
    response = requests.put(
        f"{BASE_URL}/atendimentos/atualizar/{id_atendimento}",
        json=put_data,
        headers=headers,
    )
    assert response.status_code == 201, response.text
    put_atendimento = response.json()
    
    atendimento = put_atendimento[0]["atendimento"][0]
    assert atendimento["angel"] == "João Bandoli"

if __name__ == "__main__":
    test_post_usuario()
    test_login()
    test_post_atendimento()
    test_get_atendimentos_by_cliente()
    test_get_atendimentos_by_cliente_and_angel()
    test_put_atendimento()