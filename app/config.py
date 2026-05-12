from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =========================================================
    # DATABASE
    # =========================================================
    database_url: str


    # =========================================================
    # JWT
    # =========================================================
    secret_key: str
    algorithm: str = "HS256"

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


    # =========================================================
    # APP
    # =========================================================
    environment: str = "development"
    debug: bool = True


    # =========================================================
    # CORS
    # =========================================================
    allowed_origins: str = "http://localhost:3000"


    # =========================================================
    # STRING → LIST
    # =========================================================
    @property
    def origins_list(self) -> List[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
        ]


    # =========================================================
    # ENVIRONMENT CHECK
    # =========================================================
    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


    # =========================================================
    # ENV CONFIG
    # =========================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()