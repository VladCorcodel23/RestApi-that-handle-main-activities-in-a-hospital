from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorBase


def create_doctor(db: Session, user_id: int, specialization: str):
    doctor = Doctor(user_id=user_id, specialization=specialization)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def get_doctors(db: Session):
    return db.query(Doctor).all()

def get_doctor_by_id(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def update_doctor(db: Session, doctor_id: int, doctor_data: DoctorBase):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor:
        for key, value in doctor_data.dict(exclude_unset=True).items():
            setattr(doctor, key, value)
        db.commit()
        db.refresh(doctor)
    return doctor


def delete_doctor(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor:
        db.delete(doctor)
        db.commit()
    return doctor
