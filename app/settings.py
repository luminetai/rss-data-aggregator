import logging
import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Settings:
    ENV: str
    APP_NAME: str
    APP_VERSION: str
    APP_PORT: int
    LOG_DIR: str
    LOG_LEVEL: int
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @classmethod
    def from_config(cls, config_dict: dict):
        env = os.getenv("ENV", config_dict.get("ENV", "prod"))

        if env == "dev":
            load_dotenv()

        return cls(
            ENV=env,
            APP_NAME=config_dict.get("APP_NAME", "app"),
            APP_VERSION=config_dict.get("APP_VERSION", "1.0.0"),
            APP_PORT=config_dict.get("APP_PORT", 8080),
            LOG_DIR=config_dict.get("LOG_DIR", "./logs"),
            LOG_LEVEL=logging.DEBUG if env == "dev" else logging.INFO,
            POSTGRES_HOST=os.getenv("POSTGRES_HOST", "postgres"),
            POSTGRES_USER=os.getenv("POSTGRES_USER", "admin"),
            POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "pass"),
            POSTGRES_DB=os.getenv("POSTGRES_DB", "db-name"),
            POSTGRES_PORT=int(os.getenv("POSTGRES_PORT", "5432")),
        )