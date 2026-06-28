from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status
from app.repositories.user_repo import UserRepository
from app.core.security import verify_password,create_access_token
from app.schemas.auth import Token

class AuthService:

    def __init__(self,db: AsyncSession):
        self.repo = UserRepository(db = db)

    async def login(self,email : str,password : str) -> Token:
        user = await self.repo.get_by_mail(email=email)

        if not user or not verify_password(plain_password=password,hashed_password=user.hashed_password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Incorrect password or email",headers={"WWW-Authenticate" : "Bearer"})

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )
        
        access_token = create_access_token(subject=str(user.id))
        return Token(access_token,"bearer")