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
    oidc_issuer: str | None = None
    oidc_audience: str | None = None
    oidc_jwks_url: str | None = None
    oidc_public_key_file: str | None = None
    oidc_algorithms: str = "EdDSA,RS256,ES256"
    artifact_store_path: str = "./.hsmart-artifacts"
    pilot_host_id: str = "hsmart-local-mcp-host-v1"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("HSMART_APP_NAME", "HSMART Platform"),
            environment=os.getenv("HSMART_ENV", "development").lower(),
            database_url=os.getenv("DATABASE_URL", "sqlite:///./hsmart-dev.db"),
            log_level=os.getenv("HSMART_LOG_LEVEL", "INFO").upper(),
            oidc_issuer=os.getenv("HSMART_OIDC_ISSUER"),
            oidc_audience=os.getenv("HSMART_OIDC_AUDIENCE"),
            oidc_jwks_url=os.getenv("HSMART_OIDC_JWKS_URL"),
            oidc_public_key_file=os.getenv("HSMART_OIDC_PUBLIC_KEY_FILE"),
            oidc_algorithms=os.getenv("HSMART_OIDC_ALGORITHMS", "EdDSA,RS256,ES256"),
            artifact_store_path=os.getenv("HSMART_ARTIFACT_STORE", "./.hsmart-artifacts"),
            pilot_host_id=os.getenv("HSMART_PILOT_HOST_ID", "hsmart-local-mcp-host-v1"),
        )

    def validate(self) -> None:
        if self.environment in {"production", "prod"}:
            if not self.database_url.startswith(("postgresql+psycopg://", "postgresql://")):
                raise ValueError("Production requires PostgreSQL; SQLite is development/test only")
            if not self.oidc_issuer or not self.oidc_audience:
                raise ValueError("Production requires an OIDC issuer and audience")
            if not self.oidc_jwks_url or not self.oidc_jwks_url.startswith("https://"):
                raise ValueError("Production requires an HTTPS OIDC JWKS URL")
            if self.oidc_public_key_file:
                raise ValueError("Production must use an external OIDC JWKS issuer, not a local test key")
