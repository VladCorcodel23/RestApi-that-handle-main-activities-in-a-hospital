import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.api.routes_treatment import create, get_all, get_one, update, delete
from app.schemas.treatment import TreatmentCreate, TreatmentUpdate
from app.models.treatment import Treatment
from app.models.user import User
from app.models.doctor import Doctor

# ---------- CREATE ----------

def test_create_treatment_as_manager():
    db = MagicMock()
    current_user = User(role="manager")
    treatment_data = TreatmentCreate(name="Therapy", description="Desc", doctor_id=1, patient_id=10)

    mock_treatment = Treatment(id=1, name="Therapy", doctor_id=1, patient_id=10)
    db.return_value = mock_treatment

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.create_treatment", lambda db, t: mock_treatment)
        result = create(treatment_data, db, current_user)

        assert result.name == "Therapy"
        assert result.doctor_id == 1
        assert result.patient_id == 10


def test_create_treatment_as_doctor_with_profile():
    db = MagicMock()
    current_user = User(role="doctor", doctor=Doctor(id=5))  # Asigură-te că doctorul are un ID valid
    treatment_data = TreatmentCreate(
        name="Checkup",  # Numele tratamentului
        description="Routine check-up",  # Descrierea tratamentului
        doctor_id=5,  # ID-ul doctorului valid
        patient_id=1  # ID-ul pacientului valid
    )

    mock_treatment = Treatment(id=2, name="Checkup", doctor_id=5, patient_id=1)  # Simulează un tratament valid
    db.return_value = mock_treatment

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.create_treatment", lambda db, t: mock_treatment)
        result = create(treatment_data, db, current_user)

        assert result.doctor_id == 5
        assert result.patient_id == 1


# ---------- GET ALL ----------

def test_get_all_treatments_as_manager():
    db = MagicMock()
    current_user = User(role="manager")
    mock_result = [Treatment(id=1, name="A", doctor_id=1)]

    db.return_value = mock_result
    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_all_treatments", lambda db: mock_result)
        result = get_all(db, current_user)
        assert len(result) == 1

def test_get_all_treatments_as_doctor_with_profile():
    db = MagicMock()
    current_user = User(role="doctor", doctor=Doctor(id=4))
    mock_result = [Treatment(id=2, name="B", doctor_id=4)]

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_treatments_by_doctor", lambda db, doctor_id: mock_result)
        result = get_all(db, current_user)
        assert result[0].doctor_id == 4

def test_get_all_treatments_as_doctor_without_profile():
    db = MagicMock()
    current_user = User(role="doctor", doctor=None)

    with pytest.raises(HTTPException) as exc:
        get_all(db, current_user)
    assert exc.value.status_code == 400

def test_get_all_treatments_as_unauthorized():
    db = MagicMock()
    current_user = User(role="assistant")

    with pytest.raises(HTTPException) as exc:
        get_all(db, current_user)
    assert exc.value.status_code == 403


# ---------- GET ONE ----------

def test_get_treatment_by_id_as_manager():
    db = MagicMock()
    current_user = User(role="manager")
    treatment = Treatment(id=1, doctor_id=1)
    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_treatment_by_id", lambda db, id: treatment)
        result = get_one(1, db, current_user)
        assert result.id == 1

def test_get_treatment_by_id_as_doctor_authorized():
    db = MagicMock()
    current_user = User(role="doctor", doctor=Doctor(id=2))
    treatment = Treatment(id=2, doctor_id=2)

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_treatment_by_id", lambda db, id: treatment)
        result = get_one(2, db, current_user)
        assert result.id == 2

def test_get_treatment_by_id_as_doctor_unauthorized():
    db = MagicMock()
    current_user = User(role="doctor", doctor=Doctor(id=3))
    treatment = Treatment(id=2, doctor_id=5)

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_treatment_by_id", lambda db, id: treatment)
        with pytest.raises(HTTPException) as exc:
            get_one(2, db, current_user)
        assert exc.value.status_code == 403

def test_get_treatment_by_id_not_found():
    db = MagicMock()
    current_user = User(role="manager")

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_treatment_by_id", lambda db, id: None)
        with pytest.raises(HTTPException) as exc:
            get_one(99, db, current_user)
        assert exc.value.status_code == 404


# ---------- UPDATE ----------

def test_update_treatment_success_as_manager():
    db = MagicMock()
    current_user = User(role="manager")
    treatment = Treatment(id=1, doctor_id=1)
    data = TreatmentUpdate(name="New Name")

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_treatment_by_id", lambda db, id: treatment)
        m.setattr("app.crud.treatment.update_treatment", lambda db, id, d: Treatment(id=1, name=d.name, doctor_id=1))
        result = update(1, data, db, current_user)
        assert result.name == "New Name"

def test_update_treatment_as_unauthorized_role():
    db = MagicMock()
    current_user = User(role="assistant")
    treatment = Treatment(id=1, doctor_id=2)
    data = TreatmentUpdate(name="Blocked")

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_treatment_by_id", lambda db, id: treatment)
        with pytest.raises(HTTPException) as exc:
            update(1, data, db, current_user)
        assert exc.value.status_code == 403


# ---------- DELETE ----------

def test_delete_treatment_success_as_manager():
    db = MagicMock()
    current_user = User(role="manager")
    treatment = Treatment(id=1, doctor_id=1)

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_treatment_by_id", lambda db, id: treatment)
        m.setattr("app.crud.treatment.delete_treatment", lambda db, id: {"msg": "Treatment deleted"})
        result = delete(1, db, current_user)
        assert result["msg"] == "Treatment deleted"

def test_delete_treatment_not_found():
    db = MagicMock()
    current_user = User(role="manager")

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.treatment.get_treatment_by_id", lambda db, id: None)
        with pytest.raises(HTTPException) as exc:
            delete(404, db, current_user)
        assert exc.value.status_code == 404
