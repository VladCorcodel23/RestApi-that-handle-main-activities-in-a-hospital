from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class Assistant(Base):
    __tablename__ = "assistants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department = Column(String(10), nullable=True)

    user = relationship("User", back_populates="assistant")
    assignments = relationship("PatientAssignment", back_populates="assistant")
    applications = relationship("TreatmentApplication", back_populates="assistant", cascade="all, delete")



