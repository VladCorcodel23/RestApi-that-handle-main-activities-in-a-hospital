import pytest
from unittest.mock import MagicMock, patch
from app.api.routes_auth import login
from app.schemas.user_login import UserLogin
from app.models.user import User
from fastapi import HTTPException


def test_login_success():
    mock_user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        password="hashedpass",
        role="manager"
    )

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    with patch("app.api.routes_auth.verify_password", return_value=True), \
         patch("app.api.routes_auth.create_access_token", return_value="token123"):

        user_cred = UserLogin(username="testuser", password="test123")
        result = login(user_cred, db=mock_db)

        assert result["access_token"] == "token123"
        assert result["token_type"] == "bearer"

def test_login_wrong_password():
    mock_user = User(username="testuser", password="hashedpass", role="manager")

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    with patch("app.api.routes_auth.verify_password", return_value=False):
        user_cred = UserLogin(username="testuser", password="wrongpass")

        with pytest.raises(HTTPException) as exc:
            login(user_cred, db=mock_db)
        assert exc.value.status_code == 401
        assert exc.value.detail == "Invalid credentials"

def test_login_user_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    user_cred = UserLogin(username="nouser", password="pass")

    with pytest.raises(HTTPException) as exc:
        login(user_cred, db=mock_db)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid credentials"
