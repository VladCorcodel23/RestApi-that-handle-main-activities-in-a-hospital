from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    name: str
    age: int
    address: str
    doctor_id: int

class PatientRead(BaseModel):
    id: int
    name: str
    age: int
    address: str
    doctor_id: Optional[int] = None

    class Config:
        orm_mode = True

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    doctor_id: Optional[int] = None
