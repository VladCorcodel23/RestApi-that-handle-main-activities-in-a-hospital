from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.crud.user import create_user, get_users
from app.database.session import get_db
from app.auth.dependencies import get_current_user, get_current_manager
from app.models.user import User



router = APIRouter()

# Doar managerul poate crea utilizatori
@router.post("/users/")
def add_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return create_user(db, user.username, user.email, user.password, user.role)

@router.get("/users/")
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager)
):
    return get_users(db)

# Route protejata (oricine cu token JWT valid)
@router.get("/protected/")
def protected_route(current_user=Depends(get_current_user)):
    return {"message": f"Bine ai venit, {current_user.username}!"}

# Test pentru manager
@router.get("/only-manager/")
def only_manager(current_user=Depends(get_current_manager)):
    return {"msg": f"Acces permis pentru managerul {current_user.username}"}

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_manager)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
