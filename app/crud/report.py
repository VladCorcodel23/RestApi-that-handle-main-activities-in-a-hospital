from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.models.treatment_application import TreatmentApplication
from app.models.treatment import Treatment

def get_doctors_with_patients_and_stats(db: Session):
    doctors = db.query(Doctor).all()

    data = []
    total_patients = 0

    for doctor in doctors:
        patients = doctor.patients  # relația trebuie să fie definită corect în model
        total_patients += len(patients)

        data.append({
            "doctor_id": doctor.id,
            "doctor_name": doctor.user.username,  # presupunem că user e legat
            "patients": [{"id": p.id, "name": p.name, "age": p.age} for p in patients]
        })

    stats = {
        "total_doctors": len(doctors),
        "total_patients": total_patients,
        "average_patients_per_doctor": round(total_patients / len(doctors), 2) if doctors else 0
    }

    return {
        "report": data,
        "statistics": stats
    }

def get_patient_treatments_report(db: Session, patient_id: int):
    # Join între tratamente și aplicațiile lor pentru un anumit pacient
    results = (
        db.query(
            TreatmentApplication.id.label("application_id"),
            Treatment.name.label("treatment_name"),
            TreatmentApplication.applied_at,
            TreatmentApplication.assistant_id
        )
        .join(Treatment, Treatment.id == TreatmentApplication.treatment_id)
        .filter(Treatment.patient_id == patient_id)
        .all()
    )

    return [
        {
            "application_id": r.application_id,
            "treatment_name": r.treatment_name,
            "applied_at": r.applied_at,
            "assistant_id": r.assistant_id
        }
        for r in results
    ]