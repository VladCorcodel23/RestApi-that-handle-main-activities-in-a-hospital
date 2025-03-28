from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.utils import get_password_hash


def create_user(db: Session, username: str, email: str, password: str, role: str):
    user = User(username=username, email=email, password=get_password_hash(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def get_users(db: Session):
    return db.query(User).all()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")


    if user.role == "doctor":
        doctor = db.query(Doctor).filter(Doctor.user_id == user.id).first()
        if doctor:
            db.delete(doctor)

    elif user.role == "assistant":
        assistant = db.query(Assistant).filter(Assistant.user_id == user.id).first()
        if assistant:
            db.delete(assistant)

    db.delete(user)
    db.commit()
    return {"msg": "User and associated role deleted"}

