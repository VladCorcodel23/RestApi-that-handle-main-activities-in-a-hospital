from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdate
from app.crud.doctor import create_doctor, get_doctors, get_doctor_by_id
from app.database.session import get_db
from app.auth.dependencies import get_current_manager

router = APIRouter()

@router.post("/doctors/", response_model=DoctorResponse)
def add_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return create_doctor(db, doctor.user_id, doctor.specialization)

@router.get("/doctors/", response_model=list[DoctorResponse])
def read_doctors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    return get_doctors(db)

@router.get("/doctors/{doctor_id}", response_model=DoctorResponse)
def read_doctor_by_id(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.put("/doctors/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    updated_doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if updated_doctor.specialization:
        doctor.specialization = updated_doctor.specialization

    db.commit()
    db.refresh(doctor)
    return doctor

@router.delete("/doctors/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_manager)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"msg": "Doctor deleted successfully"}
