# app/schemas/user.py
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must contain only letters, numbers, and underscores")
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        return v.lower()

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}