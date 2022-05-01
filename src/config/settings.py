import os
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseSettings, Field, PostgresDsn, validator


class LogLevels(str, Enum):
    """Enum of permitted log levels."""

    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


class UvicornSettings(BaseSettings):
    """Settings for uvicorn server"""

    host: str
    port: int = Field(ge=0, le=65535)
    log_level: LogLevels
    reload: bool


class DatabaseConnectionSettings(BaseSettings):
    """Settings for database connection"""

    postgres_user: str
    postgres_password: str
    postgres_database: str
    postgres_server: str
    postgres_uri: Optional[PostgresDsn] = None

    @validator("postgres_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("postgres_user"),
            password=values.get("postgres_password"),
            host=values.get("postgres_server"),
            path=f"/{values.get('postgres_database')}",
        )


class Settings(BaseSettings):
    uvicorn: UvicornSettings
    db_connection: DatabaseConnectionSettings


def load_from_yaml() -> Any:
    yaml_path = (
        Path("appsettings.yaml")
        if os.getenv("SERVER_ENV")
        else Path("appsettings-local.yaml")
    )
    with open(yaml_path) as fp:
        config = yaml.safe_load(fp)
    return config


@lru_cache()
def get_settings() -> Settings:
    yaml_config = load_from_yaml()
    settings = Settings(**yaml_config)
    return settings
