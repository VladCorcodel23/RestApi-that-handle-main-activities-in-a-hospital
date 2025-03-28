from sqlalchemy.orm import Session
from app.models.treatment import Treatment
from app.schemas.treatment import TreatmentCreate

def create_treatment(db: Session, treatment: TreatmentCreate):
    new_treatment = Treatment(**treatment.dict())
    db.add(new_treatment)
    db.commit()
    db.refresh(new_treatment)
    return new_treatment

def get_treatments(db: Session):
    return db.query(Treatment).all()
