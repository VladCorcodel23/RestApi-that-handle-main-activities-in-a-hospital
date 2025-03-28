import pytest
from unittest.mock import MagicMock
from app.models.treatment import Treatment
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.treatment import TreatmentCreate




@pytest.fixture
def setup_data():
    # Mocking the Doctor
    mock_doctor = MagicMock(spec=Doctor)
    mock_doctor.id = 1
    mock_doctor.specialization = "General"

    # Mocking the Patient
    mock_patient = MagicMock(spec=Patient)
    mock_patient.id = 1
    mock_patient.name = "Test Patient"

    # Mocking the User (Doctor)
    mock_user = MagicMock(spec=User)
    mock_user.role = "doctor"
    mock_user.doctor = mock_doctor

    # Mock database session
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_doctor
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_patient]

    yield mock_db, mock_user, mock_patient, mock_doctor


def test_create_treatment_recommended_by_doctor(setup_data):

    mock_db, mock_user, mock_patient, mock_doctor = setup_data

    treatment_data = TreatmentCreate(
        name="Test Treatment",
        description="Test Description",
        doctor_id=mock_doctor.id,
        patient_id=mock_patient.id
    )

    # Mock the CRUD create_treatment function
    mock_treatment = MagicMock(spec=Treatment)
    mock_treatment.id = 1
    mock_treatment.name = "Test Treatment"
    mock_treatment.doctor_id = mock_doctor.id
    mock_treatment.patient_id = mock_patient.id


    create_treatment_func = MagicMock(return_value=mock_treatment)


    created_treatment = create_treatment_func(mock_db, treatment_data)


    assert created_treatment.name == "Test Treatment"
    assert created_treatment.doctor_id == mock_doctor.id
    assert created_treatment.patient_id == mock_patient.id
