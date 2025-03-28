# schemas/user_login.py
from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str
