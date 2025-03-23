from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


project_root = Path(__file__).resolve().parents[2]
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path)


class DatabaseSettings(BaseSettings):
    hostname: str
    port: int
    name: str
    username: str
    password: str

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}@"
            f"{self.hostname}:{self.port}/{self.name}"
        )


class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    @property
    def auth_data(self) -> dict[str, str]:
        return {"secret_key": self.secret_key, "algorithm": self.algorithm}


class RedisSettings(BaseSettings):
    host: str
    port: int
    db: int
    password: str


class Settings(BaseSettings):
    database: DatabaseSettings
    auth: AuthSettings
    redis: RedisSettings

    class Config:
        env_file = dotenv_path
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()
