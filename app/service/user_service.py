from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status
from app.repositories.user_repo import UserRepository
from app.models.user_model import User_model
from app.schemas.user_schema import UserCreator

class UserService:
    def __init__(self,db : AsyncSession):
        self.repo = UserRepository(db)

    async def registry_user(self, data : UserCreator) -> User_model:
        existing = await self.repo.get_by_mail(data.email)
        if existing:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail= "Email already registered"
            )
        
        fake_hashed = f"hashed_{data.password}"

        return await self.repo.create(
            email=data.email,
            username=data.username,
            hashed_password=fake_hash
        )

    async def get_user(self,user_id) -> User_model:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail = "User not fund"
            )
        return User_model

