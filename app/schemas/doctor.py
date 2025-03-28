from pydantic import BaseModel
from typing import Optional


class DoctorBase(BaseModel):
    specialization: Optional[str] = None

class DoctorCreate(DoctorBase):
    user_id: int

class DoctorOut(DoctorBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class DoctorResponse(BaseModel):
    id: int
    user_id: int
    specialization: str

    class Config:
        orm_mode = True

class DoctorUpdate(BaseModel):
    specialization: Optional[str] = None

    class Config:
        orm_mode = True