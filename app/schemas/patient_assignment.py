from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PatientAssignmentCreate(BaseModel):
    patient_id: int
    assistant_id: int

class PatientAssignmentUpdate(BaseModel):
    assistant_id: Optional[int] = None

class PatientAssignmentRead(BaseModel):
    id: int
    patient_id: int
    assistant_id: int
    assigned_at: datetime

    class Config:
        orm_mode = True
