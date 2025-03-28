from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TreatmentCreate(BaseModel):
    name: str
    description: Optional[str]
    doctor_id: Optional[int] = None
    patient_id: int

class TreatmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None

class TreatmentRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    doctor_id: int
    patient_id: int
    created_at: datetime

    class Config:
        orm_mode = True
