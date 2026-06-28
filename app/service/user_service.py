from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status
from app.repositories.user_repo import UserRepository
from app.models.user_model import User_model
from app.schemas.user_schema import UserCreate
from app.core.security import hashed_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def registry_user(self, data: UserCreate) -> User_model:
        existing = await self.repo.get_by_mail(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        
        hashed = hashed_password(data.password)

        return await self.repo.create_user(
            email=data.email,
            username=data.username,
            hashed_password=fake_hashed
        )

    async def get_user(self, user_id) -> User_model:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

