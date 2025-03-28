from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)

    doctor = relationship("Doctor", back_populates="user", cascade="all, delete", uselist=False)
    assistant = relationship("Assistant", back_populates="user", uselist=False, cascade="all, delete", passive_deletes=True)



