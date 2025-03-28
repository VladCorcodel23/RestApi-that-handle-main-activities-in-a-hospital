from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.auth.utils import SECRET_KEY, ALGORITHM
from app.crud.user import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Returneaza utilizatorul curent dupa decodarea tokenului JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user

#  Functie reutilzabila pentru verificarea rolurilor
def require_role(required_role: str):
    def role_dependency(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires {required_role} role."
            )
        return current_user
    return role_dependency

#  Shortcut pentru doctor SAU manager
def get_current_doctor_or_manager(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["doctor", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Requires doctor or manager role."
        )
    return current_user

#  Shortcuturi utile pentru roluri specifice
get_current_manager = require_role("manager")
get_current_doctor = require_role("doctor")
get_current_assistant = require_role("assistant")
