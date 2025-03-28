from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.patient_assignment import PatientAssignment
from app.schemas.patient_assignment import PatientAssignmentCreate, PatientAssignmentUpdate

def get_all_patient_assignments(db: Session):
    return db.query(PatientAssignment).all()

def get_patient_assignment_by_id(db: Session, assignment_id: int):
    assignment = db.query(PatientAssignment).filter(PatientAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

def create_patient_assignment(db: Session, data: PatientAssignmentCreate):
    assignment = PatientAssignment(
        patient_id=data.patient_id,
        assistant_id=data.assistant_id,
        assigned_at=datetime.utcnow()
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

def update_patient_assignment(db: Session, assignment_id: int, update_data: PatientAssignmentUpdate):
    assignment = get_patient_assignment_by_id(db, assignment_id)
    if update_data.assistant_id is not None:
        assignment.assistant_id = update_data.assistant_id
    db.commit()
    db.refresh(assignment)
    return assignment

#def delete_patient_assignment(db: Session, assignment_id: int):
 #   assignment = get_patient_assignment_by_id(db, assignment_id)
  #  db.delete(assignment)
   # db.commit()
    #return {"msg": "Assignment deleted successfully"}
