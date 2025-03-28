from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.treatment import TreatmentCreate, TreatmentUpdate, TreatmentRead
from app.crud import treatment as crud_treatment
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[TreatmentRead])
def get_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == "manager":
        return crud_treatment.get_all_treatments(db)
    elif current_user.role == "doctor":
        if not current_user.doctor:
            raise HTTPException(status_code=400, detail="Doctor profile not found")
        return crud_treatment.get_treatments_by_doctor(db, doctor_id=current_user.doctor.id)
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

@router.get("/{treatment_id}", response_model=TreatmentRead)
def get_one(treatment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    treatment = crud_treatment.get_treatment_by_id(db, treatment_id)
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    if current_user.role == "manager":
        return treatment
    elif current_user.role == "doctor":
        if not current_user.doctor or treatment.doctor_id != current_user.doctor.id:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return treatment
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

@router.post("/", response_model=TreatmentRead)
def create(treatment: TreatmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == "manager":
        return crud_treatment.create_treatment(db, treatment)
    elif current_user.role == "doctor":
        if not current_user.doctor:
            raise HTTPException(status_code=400, detail="Doctor profile not found")
        treatment.doctor_id = current_user.doctor.id
        return crud_treatment.create_treatment(db, treatment)
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

@router.put("/{treatment_id}", response_model=TreatmentRead)
def update(treatment_id: int, data: TreatmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    treatment = crud_treatment.get_treatment_by_id(db, treatment_id)
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    if current_user.role == "manager":
        return crud_treatment.update_treatment(db, treatment_id, data)
    elif current_user.role == "doctor":
        if not current_user.doctor or treatment.doctor_id != current_user.doctor.id:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return crud_treatment.update_treatment(db, treatment_id, data)
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

@router.delete("/{treatment_id}")
def delete(treatment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    treatment = crud_treatment.get_treatment_by_id(db, treatment_id)
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    if current_user.role == "manager":
        return crud_treatment.delete_treatment(db, treatment_id)
    elif current_user.role == "doctor":
        if not current_user.doctor or treatment.doctor_id != current_user.doctor.id:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return crud_treatment.delete_treatment(db, treatment_id)
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")
