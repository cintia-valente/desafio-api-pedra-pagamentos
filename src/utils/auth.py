import datetime
import bcrypt
import jwt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt() 
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
    return hashed_password.decode('utf-8')  

def check_password(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_jwt(user_id: int, username: str) -> str:
    SECRET_KEY = "sua_chave_secreta_aqui"
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expira em 1 hora
    }
   
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print("Token JWT:", token)
    return token