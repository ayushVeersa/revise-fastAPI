import bcrypt
from fastapi import Depends

from app.db.database import get_db

def hash_password(password: str) -> str:
    encoded_pw = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(encoded_pw, salt)
    return hashed_pw.decode("utf-8")

def verify_password(hash_psswd: str, psswd: str) -> bool:
    encoded_pw = psswd.encode("utf-8")
    encoded_hash_pw = hash_psswd.encode("utf-8")
    return bcrypt.checkpw(encoded_pw, encoded_hash_pw)
