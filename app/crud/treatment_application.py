from sqlalchemy.orm import Session
from app.models.treatment_application import TreatmentApplication
from app.schemas.treatment_application import TreatmentApplicationCreate

def create_treatment_application(db: Session, data: TreatmentApplicationCreate):
    new_app = TreatmentApplication(
        treatment_id=data.treatment_id,
        assistant_id=data.assistant_id
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

def get_all_treatment_applications(db: Session):
    return db.query(TreatmentApplication).all()
