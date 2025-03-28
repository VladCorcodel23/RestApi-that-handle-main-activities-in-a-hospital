from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String, nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    doctor = relationship("Doctor", back_populates="patients")
    assignments = relationship("PatientAssignment", back_populates="patient")
    treatments = relationship("Treatment", back_populates="patient", cascade="all, delete")
