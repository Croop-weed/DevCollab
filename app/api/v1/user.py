import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.service.user_service import UserService
from app.core.deps import get_current_active_user
from app.models.user_model import User_model

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.registry_user(data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.get_user(user_id=user_id)

@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User_model = Depends(get_current_active_user)
):
    return current_user