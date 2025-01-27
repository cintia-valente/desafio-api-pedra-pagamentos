import random
import requests
import uuid
import requests

BASE_URL = "http://api:8080"

def generate_id_random():
    return random.randint(1000000, 9999999) 

def check_id_exists(id_atendimento):
    response = requests.get(f"{BASE_URL}/atendimentos/{id_atendimento}")
    return response.status_code == 200 
