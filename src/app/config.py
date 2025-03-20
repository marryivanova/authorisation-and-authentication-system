from pydantic_settings import BaseSettings


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
        env_file = ".env"


settings = Settings()
