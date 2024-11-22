from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.sqlite import CHAR
import uuid
from passlib.context import CryptContext
from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(15), index=True)
    email = Column(String(100), unique=True, index=True)
    surname = Column(String(100))
    password = Column(String(255))
    is_deleted = Column(Boolean, default=False)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)
