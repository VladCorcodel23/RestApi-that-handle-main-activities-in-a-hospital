from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.treatment_application import TreatmentApplicationCreate, TreatmentApplicationRead
from app.crud import treatment_application as crud
from app.database.session import get_db
from app.auth.dependencies import get_current_doctor_or_manager, get_current_assistant
from app.models.treatment_application import TreatmentApplication
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=TreatmentApplicationRead)
def create_ta(
    data: TreatmentApplicationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor_or_manager)
):
    return crud.create_treatment_application(db, data)

@router.get("/", response_model=list[TreatmentApplicationRead])
def get_all_tas(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor_or_manager)
):
    return crud.get_all_treatment_applications(db)

@router.get("/my", response_model=list[TreatmentApplicationRead])
def get_my_applied_treatments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_assistant)
):
    return db.query(TreatmentApplication).filter(
        TreatmentApplication.assistant_id == current_user.assistant.id
    ).all()
