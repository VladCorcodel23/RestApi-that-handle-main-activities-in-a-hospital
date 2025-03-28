from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_manager, get_current_user
from app.crud import report
from app.crud import report as report_crud
from app.models.patient import Patient
from app.models.user import User


router = APIRouter()

@router.get("/doctors-report")
def generate_doctors_report(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_manager)
):
    return report.get_doctors_with_patients_and_stats(db)


@router.get("/patient-treatments/{patient_id}")
def get_patient_treatments(
        patient_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role == "manager":
        pass


    elif current_user.role == "doctor":
        patient = db.query(Patient).filter(
            Patient.id == patient_id,
            Patient.doctor_id == current_user.doctor.id
        ).first()
        if not patient:
            raise HTTPException(status_code=403, detail="You can only access reports for your own patients.")

    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

    results = report_crud.get_patient_treatments_report(db, patient_id)
    if not results:
        raise HTTPException(status_code=404, detail="No treatments found for this patient.")
    return results