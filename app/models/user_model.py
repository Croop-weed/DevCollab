import uuid
from datetime import datetime
from sqlalchemy import String,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base

class User_model(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    email : Mapped[str] = mapped_column(String(225),unique=True,nullable=False)
    username : Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    hashed_password : Mapped[str] = mapped_column(String,nullable=False)
    is_active : Mapped[bool] = mapped_column(default=True)
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()    
    )
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )