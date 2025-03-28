from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.base import Base

class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    doctor = relationship("Doctor", back_populates="treatments")
    patient = relationship("Patient", back_populates="treatments")
    applications = relationship("TreatmentApplication", back_populates="treatment", cascade="all, delete")


