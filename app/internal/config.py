import secrets
import warnings
from typing import Literal

from pydantic import PostgresDsn, computed_field, model_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_TIME: int = 60 * 24 * 7  # 7 days
    API_V1_STR: str = "/api/v1"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "secret"
    POSTGRES_DB: str = "db"

    @computed_field
    @property
    def POSTGRES_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "secret":
            message = (
                f'The value of {var_name} has not been changed from "secret", '
                "please change it for security reasons"
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("JWT_SECRET_KEY", self.JWT_SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        return self


settings = Settings()
