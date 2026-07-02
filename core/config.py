from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    API_V1_PREFIX: str = "/api/v1"

    # auth
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE_MINUTES: timedelta = timedelta(days=7)


settings = Settings()
