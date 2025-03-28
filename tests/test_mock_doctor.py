import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from app.api.routes_doctor import (
    add_doctor,
    get_doctors,
    get_doctor_by_id,
    update_doctor,
    delete_doctor
)
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.models.doctor import Doctor


def test_add_doctor_success():
    mock_doctor = Doctor(
        id=1,
        user_id=10,
        specialization="Cardiology"
    )

    doctor_data = DoctorCreate(
        user_id=10,
        specialization="Cardiology"
    )

    mock_db = MagicMock()
    mock_current_manager = MagicMock()

    with patch("app.api.routes_doctor.create_doctor", return_value=mock_doctor):
        result = add_doctor(doctor=doctor_data, db=mock_db, current_user=mock_current_manager)

        assert result.user_id == 10
        assert result.specialization == "Cardiology"


def test_get_doctors_success():
    mock_db = MagicMock()

    doctors = [
        Doctor(id=1, user_id=10, specialization="Cardiology"),
        Doctor(id=2, user_id=11, specialization="Neurology")
    ]
    mock_db.query.return_value.all.return_value = doctors

    result = get_doctors(db=mock_db)
    assert len(result) == 2
    assert result[0].specialization == "Cardiology"


def test_get_doctor_by_id_success():
    mock_db = MagicMock()

    doctor = Doctor(id=1, user_id=10, specialization="Cardiology")
    mock_db.query.return_value.filter.return_value.first.return_value = doctor

    result = get_doctor_by_id(doctor_id=1, db=mock_db)
    assert result.user_id == 10
    assert result.specialization == "Cardiology"


def test_update_doctor_success():
    mock_db = MagicMock()
    doctor = Doctor(id=1, user_id=10, specialization="Old")

    mock_filter = MagicMock()
    mock_filter.first.return_value = doctor
    mock_db.query.return_value.filter.return_value = mock_filter

    update_data = DoctorUpdate(specialization="Updated")

    result = update_doctor(1, update_data, mock_db)
    assert result.specialization == "Updated"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(doctor)


def test_update_doctor_not_found():
    mock_db = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = None
    mock_db.query.return_value.filter.return_value = mock_filter

    update_data = DoctorUpdate(specialization="Anything")

    with pytest.raises(HTTPException) as exc:
        update_doctor(99, update_data, mock_db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Doctor not found"


def test_delete_doctor_success():
    mock_db = MagicMock()
    doctor = Doctor(id=1, user_id=10, specialization="Cardiology")

    mock_filter = MagicMock()
    mock_filter.first.return_value = doctor
    mock_db.query.return_value.filter.return_value = mock_filter

    result = delete_doctor(1, mock_db)
    assert result == {"msg": "Doctor deleted successfully"}
    mock_db.delete.assert_called_once_with(doctor)
    mock_db.commit.assert_called_once()


def test_delete_doctor_not_found():
    mock_db = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = None
    mock_db.query.return_value.filter.return_value = mock_filter

    with pytest.raises(HTTPException) as exc:
        delete_doctor(999, mock_db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Doctor not found"
