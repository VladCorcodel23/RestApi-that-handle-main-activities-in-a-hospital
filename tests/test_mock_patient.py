import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.api.routes_patient import (
    create_patient,
    read_all_patients,
    read_patient_by_id,
    update_patient,
    delete_patient
)
from app.schemas.patient import PatientCreate, PatientUpdate
from app.models.patient import Patient


def test_add_patient_success():
    mock_patient = Patient(
        id=1,
        name="John Doe",
        age=35,
        address="Strada X",
        doctor_id=5
    )

    patient_data = PatientCreate(
        name="John Doe",
        age=35,
        address="Strada X",
        doctor_id=5
    )

    mock_db = MagicMock()
    mock_current_user = MagicMock()
    mock_current_user.role = "manager"  # 👈 evită HTTP 403

    with patch("app.crud.patient.create_patient", return_value=mock_patient):
        result = create_patient(patient=patient_data, db=mock_db, current_user=mock_current_user)

        assert result.name == "John Doe"
        assert result.age == 35
        assert result.doctor_id == 5


def test_get_patients_success():
    mock_db = MagicMock()
    mock_user = MagicMock()

    patients = [
        Patient(id=1, name="John", age=30, address="A", doctor_id=10),
        Patient(id=2, name="Ana", age=25, address="B", doctor_id=11)
    ]
    mock_db.query.return_value.all.return_value = patients

    result = read_all_patients(db=mock_db, current_user=mock_user)
    assert len(result) == 2
    assert result[0].name == "John"
    assert result[1].name == "Ana"


def test_get_patient_by_id_success():
    mock_db = MagicMock()
    mock_user = MagicMock()
    patient = Patient(id=1, name="Elena", age=40, address="Calea X", doctor_id=8)
    mock_db.query.return_value.filter.return_value.first.return_value = patient

    result = read_patient_by_id(patient_id=1, db=mock_db, current_user=mock_user)
    assert result.name == "Elena"


def test_get_patient_by_id_not_found():
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        read_patient_by_id(999, db=mock_db, current_user=mock_user)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Patient not found"


def test_update_patient_success():
    mock_db = MagicMock()
    mock_user = MagicMock()
    patient = Patient(id=1, name="Ion", age=60, address="Veche", doctor_id=4)
    mock_db.query.return_value.filter.return_value.first.return_value = patient

    update_data = PatientUpdate(age=65, address="Noua")

    result = update_patient(patient_id=1, updated_data=update_data, db=mock_db, current_user=mock_user)
    assert result.age == 65
    assert result.address == "Noua"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(patient)


def test_update_patient_not_found():
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    update_data = PatientUpdate(age=40)

    with pytest.raises(HTTPException) as exc:
        update_patient(patient_id=404, updated_data=update_data, db=mock_db, current_user=mock_user)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Patient not found"


def test_delete_patient_success():
    mock_db = MagicMock()
    mock_user = MagicMock()
    patient = Patient(id=1, name="Mihai", age=50, address="X", doctor_id=9)
    mock_db.query.return_value.filter.return_value.first.return_value = patient

    result = delete_patient(patient_id=1, db=mock_db, current_user=mock_user)
    assert result == {"msg": "Patient deleted successfully"}  #
    mock_db.delete.assert_called_once_with(patient)
    mock_db.commit.assert_called_once()


def test_delete_patient_not_found():
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        delete_patient(patient_id=404, db=mock_db, current_user=mock_user)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Patient not found"
