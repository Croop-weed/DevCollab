from datetime import datetime,timedelta,timezone
from typing import Any
from jose import JWTError,jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_cotext = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hashed_password(password : str) -> str:
    return pwd_cotext.hash(password)

def verify_password(plain_password : str,hashed_password : str) -> bool:
    return pwd_cotext.verify(plain_password,hashed_password)

def create_access_token(subject : str | Any,expires_delta : timedelta | None = None) -> str:
    expires = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub" : str(subject),
        "exp" : expires,
        "iat" : datetime.now(timezone.utc)
    }
    return jwt.encode(payload,settings.SECRET_KEY,algorithm=[settings.ALGORITHM])

def decode_access_token(token : str) -> str:
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return {}