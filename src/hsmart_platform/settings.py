"""Environment-backed settings with explicit production safety checks."""
from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "HSMART Platform"
    environment: str = "development"
    database_url: str = "sqlite:///./hsmart-dev.db"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("HSMART_APP_NAME", "HSMART Platform"),
            environment=os.getenv("HSMART_ENV", "development").lower(),
            database_url=os.getenv("DATABASE_URL", "sqlite:///./hsmart-dev.db"),
            log_level=os.getenv("HSMART_LOG_LEVEL", "INFO").upper(),
        )

    def validate(self) -> None:
        if self.environment in {"production", "prod"} and not self.database_url.startswith(
            ("postgresql+psycopg://", "postgresql://")
        ):
            raise ValueError("Production requires PostgreSQL; SQLite is development/test only")
