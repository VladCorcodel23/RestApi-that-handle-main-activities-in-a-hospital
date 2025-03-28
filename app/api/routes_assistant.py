from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.assistant import AssistantCreate, AssistantOut, AssistantUpdate
from app.crud import assistant as assistant_crud
from app.database.session import get_db
from app.auth.dependencies import get_current_manager

router = APIRouter()

@router.post("/", response_model=AssistantOut)
def create_assistant(
    assistant: AssistantCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return assistant_crud.create_assistant(db, assistant.user_id, assistant.department)

@router.get("/", response_model=list[AssistantOut])
def read_assistants(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return assistant_crud.get_assistants(db)

@router.get("/{assistant_id}", response_model=AssistantOut)
def read_assistant(
    assistant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return assistant_crud.get_assistant_by_id(db, assistant_id)

@router.put("/{assistant_id}", response_model=AssistantOut)
def update_assistant(
    assistant_id: int,
    assistant: AssistantUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return assistant_crud.update_assistant(db, assistant_id, assistant.department)

@router.delete("/{assistant_id}")
def delete_assistant(
    assistant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return assistant_crud.delete_assistant(db, assistant_id)
