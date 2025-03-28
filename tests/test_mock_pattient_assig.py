import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.api.routes_patient_assignment import create_assignment
from app.models.user import User
from app.models.patient import Patient
from app.models.patient_assignment import PatientAssignment
from app.schemas.patient_assignment import PatientAssignmentCreate
from app.models.doctor import Doctor


# Testeaza eroarea daca un asistent incearca sa asigneze un pacient
def test_create_patient_assignment_by_assistant():
    db = MagicMock()
    current_user = User(role="assistant")

    assignment_data = PatientAssignmentCreate(
        patient_id=1,
        assistant_id=2
    )

    with pytest.raises(HTTPException) as exc:
        create_assignment(assignment_data, db, current_user)

    assert exc.value.status_code == 403
    assert "Access forbidden" in str(exc.value.detail)

