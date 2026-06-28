import uuid
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.repositories.user_repo import UserRepository
from app.models.user_model import User_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token : str = Depends(oauth2_scheme),db : AsyncSession = Depends(get_db)) -> User:

    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    payload = decode_access_token(token=token)
    if not payload :
        raise credential_exception

    user_id : str = payload.get("sub")
    if not user_id:
        raise credential_exception 
    
    repo = UserRepository(db)

    user = await repo.get_by_id(uuid.UUID(user_id))
    if not user:
        raise credential_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user
