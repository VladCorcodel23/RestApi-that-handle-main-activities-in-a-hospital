from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    specialization = Column(String(100))

    user = relationship("User", back_populates="doctor")
    patients = relationship("Patient", back_populates="doctor")
    treatments = relationship("Treatment", back_populates="doctor")

