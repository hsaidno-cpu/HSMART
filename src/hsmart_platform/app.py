"""HTTP process entry point for the HSMART modular-monolith foundation."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine

from .database import build_engine
from .settings import Settings


def create_app(settings: Settings | None = None, engine: Engine | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    settings.validate()
    db_engine = engine or build_engine(settings.database_url)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="HSMART application foundation. Business domains are introduced only after KM 1 exit.",
    )
    app.state.settings = settings
    app.state.engine = db_engine

    @app.get("/v1/health", tags=["Operations"])
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "hsmart-api", "environment": settings.environment}

    @app.get("/v1/ready", tags=["Operations"])
    def readiness() -> dict[str, str]:
        try:
            with db_engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=503, detail="database_not_ready") from exc
        return {"status": "ready", "database": "reachable"}

    return app


app = create_app()
