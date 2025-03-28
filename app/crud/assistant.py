from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.assistant import Assistant
from app.models.user import User

def create_assistant(db: Session, user_id: int, department: str):
    assistant = Assistant(user_id=user_id, department=department)
    db.add(assistant)
    db.commit()
    db.refresh(assistant)
    return assistant

def get_assistants(db: Session):
    return db.query(Assistant).all()

def get_assistant_by_id(db: Session, assistant_id: int):
    return db.query(Assistant).filter(Assistant.id == assistant_id).first()

def update_assistant(db: Session, assistant_id: int, department: str):
    assistant = db.query(Assistant).filter(Assistant.id == assistant_id).first()
    if assistant:
        assistant.department = department
        db.commit()
        db.refresh(assistant)
    return assistant


def delete_assistant(db: Session, assistant_id: int):
    assistant = db.query(Assistant).filter(Assistant.id == assistant_id).first()
    if assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")

    db.delete(assistant)
    db.commit()

    return {"msg": "Assistant deleted"}

