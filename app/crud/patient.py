from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

def create_patient(db: Session, patient_data: PatientCreate):
    patient = Patient(**patient_data.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_all_patients(db: Session):
    return db.query(Patient).all()

def get_patients_by_doctor(db: Session, doctor_id: int):
    return db.query(Patient).filter(Patient.doctor_id == doctor_id).all()


def get_patient_by_id(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

def update_patient(db: Session, patient_id: int, updated_data: PatientUpdate):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return {"msg": "Patient deleted successfully"}
