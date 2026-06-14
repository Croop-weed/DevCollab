import uuid 
from datetime import datetime
from pydantic import BaseModel,EmailStr,field_validator

class UserCreator(BaseModel):
    email : EmailStr
    username : str
    password : str
    age : datetime

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str :
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must contain only letters, numbers, and underscores")
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        return v.lower()

    @field_validator("age")
    @classmethod
    def user_age(cls,d : datetime) -> datetime:
        min_age = datetime.now().year - d.year
        if min_age < 18:
            raise ValueError("USER must be 18 or above")

class UserResponse(BaseModel):
    id : uuid
    email : EmailStr
    username : str
    is_active : bool 
    created_at : datetime

    model_config = {"from_attribute": True}