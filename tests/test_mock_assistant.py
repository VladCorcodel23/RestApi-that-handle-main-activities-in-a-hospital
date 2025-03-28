import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.api.routes_assistant import (
    create_assistant,
    read_assistants,
    read_assistant,
    update_assistant,
    delete_assistant
)
from app.schemas.assistant import AssistantCreate, AssistantUpdate
from app.models.assistant import Assistant



def test_add_assistant_success():
    mock_assistant = Assistant(id=1, user_id=5)
    assistant_data = AssistantCreate(user_id=5, department="Cardiology")

    mock_db = MagicMock()
    mock_user = MagicMock()

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.assistant.create_assistant", lambda db, user_id, department: mock_assistant)

        result = create_assistant(assistant=assistant_data, db=mock_db, current_user=mock_user)

        assert result.user_id == 5



def test_get_all_assistants_success():
    mock_db = MagicMock()
    mock_user = MagicMock()
    assistants = [
        Assistant(id=1, user_id=5),
        Assistant(id=2, user_id=6)
    ]

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.assistant.get_assistants", lambda db: assistants)

        result = read_assistants(db=mock_db, current_user=mock_user)
        assert len(result) == 2
        assert result[0].user_id == 5



def test_get_assistant_by_id_success():
    mock_db = MagicMock()
    mock_user = MagicMock()
    assistant = Assistant(id=1, user_id=5)

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.assistant.get_assistant_by_id", lambda db, id: assistant)

        result = read_assistant(assistant_id=1, db=mock_db, current_user=mock_user)
        assert result.user_id == 5



def test_update_assistant_success():
    mock_db = MagicMock()
    mock_user = MagicMock()
    assistant = Assistant(id=1, user_id=7)

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.assistant.update_assistant", lambda db, id, department: assistant)

        update_data = AssistantUpdate(department="Neurology")
        result = update_assistant(1, update_data, db=mock_db, current_user=mock_user)

        assert result.user_id == 7


def test_update_assistant_not_found():
    mock_db = MagicMock()
    mock_user = MagicMock()

    def raise_exception(db, id, department):
        raise HTTPException(status_code=404, detail="Assistant not found")

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.assistant.update_assistant", raise_exception)

        update_data = AssistantUpdate(department="Neurology")

        with pytest.raises(HTTPException) as exc:
            update_assistant(1, update_data, db=mock_db, current_user=mock_user)

        assert exc.value.status_code == 404



def test_delete_assistant_success():
    mock_db = MagicMock()
    mock_user = MagicMock()

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.assistant.delete_assistant", lambda db, id: {"message": "Assistant deleted successfully"})

        result = delete_assistant(1, db=mock_db, current_user=mock_user)
        assert result == {"message": "Assistant deleted successfully"}


def test_delete_assistant_not_found():
    mock_db = MagicMock()
    mock_user = MagicMock()

    def raise_exception(db, id):
        raise HTTPException(status_code=404, detail="Assistant not found")

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.crud.assistant.delete_assistant", raise_exception)

        with pytest.raises(HTTPException) as exc:
            delete_assistant(1, db=mock_db, current_user=mock_user)

        assert exc.value.status_code == 404
        assert exc.value.detail == "Assistant not found"
