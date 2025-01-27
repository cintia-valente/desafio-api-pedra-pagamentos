import datetime
import os
import bcrypt
import jwt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt() 
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
    return hashed_password.decode('utf-8')  

def check_password(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
