from fastapi import Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from app.models.user import User

def get_current_manager(current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Requires manager role"
        )
    return current_user

def get_current_doctor(current_user: User = Depends(get_current_user)):
    if current_user.role != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Requires doctor role"
        )
    return current_user

def get_current_assistant(current_user: User = Depends(get_current_user)):
    if current_user.role != "assistant":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Requires assistant role"
        )
    return current_user
