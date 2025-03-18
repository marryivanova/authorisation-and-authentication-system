from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    class Config:
        env_file = ".env"


settings = Settings()


def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@"
        f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
    )


def get_auth_data():
    return {"secret_key": settings.secret_key, "algorithm": settings.algorithm}
