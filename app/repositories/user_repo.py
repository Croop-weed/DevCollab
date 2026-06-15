import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import User_model


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_mail(self, email: str) -> User_model | None:
        result = await self.db.execute(
            select(User_model).where(User_model.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> User_model | None:
        result = await self.db.execute(
            select(User_model).where(User_model.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, email: str, username: str, hashed_password: str) -> User_model:
        user = User_model(email=email, username=username, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user