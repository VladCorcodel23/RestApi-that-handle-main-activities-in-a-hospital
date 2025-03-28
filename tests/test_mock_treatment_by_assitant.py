import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.models.treatment_application import TreatmentApplication
from app.models.user import User
from app.models.treatment import Treatment
from app.schemas.treatment_application import TreatmentApplicationCreate
from app.api.routes_treatment_application import create_ta



def test_create_treatment_application_by_assistant():
    db = MagicMock()

    current_user = User(role="assistant", assistant=MagicMock(id=1))


    treatment = Treatment(id=1, name="Therapy", description="Desc", doctor_id=2, patient_id=1)
    db.query.return_value.filter.return_value.first.return_value = treatment


    application_data = TreatmentApplicationCreate(
        treatment_id=1,
        assistant_id=1
    )

    # Mock pentru crearea aplicatiei de tratament
    mock_treatment_application = TreatmentApplication(id=1, treatment_id=1, assistant_id=1)
    db.return_value = mock_treatment_application

    with pytest.MonkeyPatch().context() as m:
        # Mock pt functia de creare a aplicatiei de tratament
        m.setattr("app.crud.treatment_application.create_treatment_application",
                  lambda db, data: mock_treatment_application)

        result = create_ta(application_data, db, current_user)

        # Verific ca tratamentul si asistentul sunt corect aplicate
        assert result.treatment_id == 1
        assert result.assistant_id == 1
        assert result.id == 1




