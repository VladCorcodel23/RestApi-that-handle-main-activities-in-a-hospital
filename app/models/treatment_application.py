from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class TreatmentApplication(Base):
    __tablename__ = "treatment_applications"

    id = Column(Integer, primary_key=True, index=True)
    treatment_id = Column(Integer, ForeignKey("treatments.id"), nullable=False)
    assistant_id = Column(Integer, ForeignKey("assistants.id"), nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow)

    treatment = relationship("Treatment", back_populates="applications")
    assistant = relationship("Assistant", back_populates="applications")
