from datetime import datetime,timedelta,timezone
from typing import Any
from jose import JWTError,jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_cotext = CryptContext(schemes=["bycrpt"],deprecated="auto")

def hashed_password(password : str) -> str:
    return pwd_cotext.hash(password)

def verify_password(plain_password : str,hashed_password : str) -> bool:
    return pwd_cotext.verify(plain_password,hashed_password)