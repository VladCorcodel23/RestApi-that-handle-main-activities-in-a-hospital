from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.treatment import Treatment
from app.schemas.treatment import TreatmentCreate, TreatmentUpdate

def get_all_treatments(db: Session):
    return db.query(Treatment).all()

def get_treatments_by_doctor(db: Session, doctor_id: int):
    return db.query(Treatment).filter(Treatment.doctor_id == doctor_id).all()

def get_treatment_by_id(db: Session, treatment_id: int):
    return db.query(Treatment).filter(Treatment.id == treatment_id).first()

def create_treatment(db: Session, treatment_data: TreatmentCreate):
    treatment = Treatment(**treatment_data.dict())
    db.add(treatment)
    db.commit()
    db.refresh(treatment)
    return treatment

def update_treatment(db: Session, treatment_id: int, data: TreatmentUpdate):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(treatment, field, value)

    db.commit()
    db.refresh(treatment)
    return treatment

def delete_treatment(db: Session, treatment_id: int):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    db.delete(treatment)
    db.commit()
    return {"msg": "Treatment deleted successfully"}
