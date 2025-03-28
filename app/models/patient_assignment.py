from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class PatientAssignment(Base):
    __tablename__ = "patient_assignments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    assistant_id = Column(Integer, ForeignKey("assistants.id"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")
    assistant = relationship("Assistant")
