from pydantic import BaseModel
from typing import Optional

class AssistantBase(BaseModel):
    department: Optional[str] = None

class AssistantCreate(AssistantBase):
    user_id: int

class AssistantOut(AssistantBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class AssistantUpdate(AssistantBase):
    pass
