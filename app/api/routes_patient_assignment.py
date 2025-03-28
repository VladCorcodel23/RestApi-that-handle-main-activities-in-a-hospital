from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.patient import Patient
from app.models.patient_assignment import PatientAssignment
from app.schemas.patient_assignment import PatientAssignmentCreate, PatientAssignmentRead, PatientAssignmentUpdate

router = APIRouter()

# GET - toate asignarile (doar pentru manager)
@router.get("/", response_model=list[PatientAssignmentRead])
def get_all_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return db.query(PatientAssignment).all()

# POST - adaugare asignare (doctor doar pt pacientii lui, manager pt toti)
@router.post("/", response_model=PatientAssignmentRead)
def create_assignment(
    assignment: PatientAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "doctor":
        # doctorul poate asigna doar pacientii lui
        patient = db.query(Patient).filter(
            Patient.id == assignment.patient_id,
            Patient.doctor_id == current_user.doctor.id
        ).first()
        if not patient:
            raise HTTPException(status_code=403, detail="You can only assign assistants to your own patients.")

    elif current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Access forbidden")

    db_assignment = PatientAssignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

# PUT - actualizare asignare (doctor doar pt pacientii lui, manager pt toti)
@router.put("/{assignment_id}", response_model=PatientAssignmentRead)
def update_assignment(
    assignment_id: int,
    update_data: PatientAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignment = db.query(PatientAssignment).filter(PatientAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if current_user.role == "doctor":
        patient = db.query(Patient).filter(
            Patient.id == assignment.patient_id,
            Patient.doctor_id == current_user.doctor.id
        ).first()
        if not patient:
            raise HTTPException(status_code=403, detail="You can only update assignments for your own patients.")

    elif current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Access forbidden")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(assignment, key, value)

    db.commit()
    db.refresh(assignment)
    return assignment

@router.get("/{assignment_id}", response_model=PatientAssignmentRead)
def get_assignment_by_id(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignment = db.query(PatientAssignment).join(Patient).filter(PatientAssignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if current_user.role == "manager":
        return assignment

    if current_user.role == "doctor":
        # verificăm dacă pacientul aparține doctorului curent
        if assignment.patient.doctor_id == current_user.doctor.id:
            return assignment
        else:
            raise HTTPException(status_code=403, detail="Access forbidden")

    raise HTTPException(status_code=403, detail="Access forbidden")

