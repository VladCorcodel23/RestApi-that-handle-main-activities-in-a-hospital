from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.crud import patient as patient_crud
from app.database.session import get_db
from app.auth.dependencies import get_current_doctor, get_current_manager, get_current_user

router = APIRouter()

# GET - Manager: toti pacienții
@router.get("/", response_model=list[PatientRead])
def read_all_patients(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return patient_crud.get_all_patients(db)

# GET - Doctor: propriii pacienti
@router.get("/my", response_model=list[PatientRead])
def read_my_patients(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_doctor)
):
    return patient_crud.get_patients_by_doctor(db, current_user.id)


# GET - Un pacient dupa ID (manager doar)
@router.get("/{patient_id}", response_model=PatientRead)
def read_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return patient_crud.get_patient_by_id(db, patient_id)

# POST - Adauga pacient (doctor sau manager)
@router.post("/", response_model=PatientRead)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role not in ["doctor", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    return patient_crud.create_patient(db, patient)

# PUT - Actualizeaza pacient (doar manager)
@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int,
    updated_data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return patient_crud.update_patient(db, patient_id, updated_data)

# DELETE - sterge pacient (doar manager)
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return patient_crud.delete_patient(db, patient_id)
