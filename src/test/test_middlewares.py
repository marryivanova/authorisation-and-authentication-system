import pytest
from jose import jwt, JWTError
from fastapi import HTTPException, status
from unittest.mock import patch


from src.app.middlewares import verify_token, create_refresh_token
from src.app.redis_client import redis_config

from src.app.config import settings
from src.app.middlewares import (
    pwd_context,
    get_password_hash,
    verify_password,
    create_token,
)


def test_password_hash():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert pwd_context.verify(password, hashed_password) == True
    assert pwd_context.verify("wrongpassword", hashed_password) == False
    assert get_password_hash("wrongpassword") != hashed_password


def test_verify_password():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) == True
    assert verify_password("wrongpassword", hashed_password) == False


def test_create_token():
    data = {"username": "testuser", "role": "user"}
    token = create_token(data)
    jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])


def test_verify_token_expired_token():
    expired_token = "expired.jwt.token"
    with patch("src.app.middlewares.jwt.decode") as mock_decode:
        mock_decode.side_effect = JWTError("Token is expired")
        with patch("src.app.middlewares.redis_config.get", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                verify_token(expired_token)
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Could not validate credentials"


def test_verify_token_invalid_secret_key():
    token_data = {"sub": "testuser", "role": "user"}
    invalid_secret_key = "invalidsecret"

    # Create a token with an invalid secret key
    token = jwt.encode(
        token_data, invalid_secret_key, algorithm=settings.auth.algorithm
    )

    with patch.object(redis_config, "get", return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"


def test_verify_token_missing_sub_field():
    token_data = {"role": "user"}
    token = jwt.encode(
        token_data, settings.auth.secret_key, algorithm=settings.auth.algorithm
    )

    with patch.object(redis_config, "get", return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"


def test_create_refresh_token_raises_error_when_data_is_not_dict():
    with pytest.raises(AttributeError):
        create_refresh_token(data="not_a_dict")
