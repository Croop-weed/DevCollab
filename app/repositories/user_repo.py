import uuid 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserRepository:
    def __init__(self,db : AsyncSession):
        self.db = db

    async def get_by_mail(self,email : str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_id(self,user_id : uuid.UUID) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self,email : str,username : str,hased_password: str) -> User:
        user = User(email = email,username = username,password = hased_password)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
        
