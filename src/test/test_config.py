import pytest
from pydantic import ValidationError

from src.app.config import AuthSettings
from src.app.config import DatabaseSettings
from src.app.config import RedisSettings


def test_database_settings_url_generation():
    db_settings = DatabaseSettings(
        hostname="localhost",
        port=5432,
        name="test_db",
        username="user",
        password="pass",
    )
    expected_url = "postgresql+asyncpg://user:pass@localhost:5432/test_db"
    assert db_settings.url == expected_url


def test_database_settings_negative_port():
    try:
        DatabaseSettings(
            hostname="localhost",
            port=-5432,
            name="test_db",
            username="user",
            password="pass",
        )
    except ValueError as e:
        assert str(e) == "Port must be a positive integer"


def test_auth_settings_initialization():
    auth_settings = AuthSettings(
        secret_key="mysecretkey", algorithm="HS256", access_token_expire_minutes=30
    )
    assert auth_settings.secret_key == "mysecretkey"
    assert auth_settings.algorithm == "HS256"
    assert auth_settings.access_token_expire_minutes == 30
    assert auth_settings.auth_data == {
        "secret_key": "mysecretkey",
        "algorithm": "HS256",
    }


def test_auth_settings_with_non_string_secret_key():
    with pytest.raises(ValidationError):
        AuthSettings(
            secret_key=12345, algorithm="HS256", access_token_expire_minutes=30
        )


def test_auth_settings_with_non_string_algorithm():
    with pytest.raises(ValidationError):
        AuthSettings(
            secret_key="mysecret", algorithm=123, access_token_expire_minutes=30
        )


def test_redis_settings_initialization():
    redis_settings = RedisSettings(
        host="localhost", port=6379, db=0, password="securepassword"
    )
    assert redis_settings.host == "localhost"
    assert redis_settings.port == 6379
    assert redis_settings.db == 0
    assert redis_settings.password == "securepassword"
