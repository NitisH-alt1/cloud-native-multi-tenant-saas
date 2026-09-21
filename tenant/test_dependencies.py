import pytest

from fastapi import HTTPException

from auth.dependencies import get_current_user


def test_missing_authorization_header():
    with pytest.raises(HTTPException) as error:
        get_current_user(
            authorization=None,
            db=None
        )

    assert error.value.status_code == 401
    assert error.value.detail == "Authorization header is required"


def test_invalid_authorization_header():
    with pytest.raises(HTTPException) as error:
        get_current_user(
            authorization="InvalidToken",
            db=None
        )

    assert error.value.status_code == 401
    assert error.value.detail == "Invalid authorization header"


def test_empty_bearer_token():
    with pytest.raises(HTTPException) as error:
        get_current_user(
            authorization="Bearer ",
            db=None
        )

    assert error.value.status_code == 401
    assert error.value.detail == "Access token is required"
