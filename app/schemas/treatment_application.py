from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TreatmentApplicationCreate(BaseModel):
    treatment_id: int
    assistant_id: Optional[int] = None  # poate fi null, deci e opțional

class TreatmentApplicationRead(BaseModel):
    id: int
    treatment_id: int
    assistant_id: Optional[int] = None
    applied_at: datetime

    class Config:
        orm_mode = True
