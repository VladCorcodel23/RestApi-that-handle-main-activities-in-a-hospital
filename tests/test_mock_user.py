import pytest
from unittest.mock import patch, MagicMock
from app.api.routes_user import add_user
from app.schemas.user import UserCreate
from app.models.user import User

def test_add_user_success():
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password="hashed",
        role="doctor"
    )

    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="secret",
        role="doctor"
    )

    mock_db = MagicMock()
    mock_current_manager = MagicMock()

    with patch("app.api.routes_user.create_user", return_value=mock_user):
        result = add_user(user=user_data, db=mock_db, current_user=mock_current_manager)

        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.role == "doctor"
