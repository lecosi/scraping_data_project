from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    username = Column(String)
    password = Column(String)

    def verify_password(self, password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.password)
