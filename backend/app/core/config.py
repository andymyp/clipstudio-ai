"""Typed configuration loading with YAML defaults and environment overrides."""

from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = PROJECT_ROOT / "config"


class AppConfig(BaseModel):
    """Application runtime settings."""

    name: str = "ClipStudio AI"
    version: str = "0.1.0"
    environment: Literal["development", "testing", "production"] = "development"
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)


class DatabaseConfig(BaseModel):
    """Local database settings."""

    url: str = "sqlite+aiosqlite:///./storage/clipstudio.db"
    echo: bool = False
    pool_size: int = Field(default=5, ge=1)


class ModelsConfig(BaseModel):
    """AI model defaults; providers remain replaceable."""

    provider: str = "local"
    llm: str = "disabled"
    speech: str = "faster-whisper-small"
    embeddings: str = "sentence-transformers"


class StorageConfig(BaseModel):
    """Runtime storage locations and limits."""

    path: Path = PROJECT_ROOT / "storage"
    log_path: Path = PROJECT_ROOT / "logs"
    max_cache_mb: int = Field(default=2048, ge=1)

    @field_validator("path", "log_path", mode="before")
    @classmethod
    def expand_path(cls, value: Any) -> Path:
        return Path(value).expanduser()


class Settings(BaseSettings):
    """Complete application settings assembled from files and environment."""

    model_config = SettingsConfigDict(
        env_file=(".env",), env_prefix="CLIPSTUDIO_", extra="ignore"
    )

    app: AppConfig = Field(default_factory=AppConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    models: ModelsConfig = Field(default_factory=ModelsConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)

    @classmethod
    def load(cls, config_dir: Path = CONFIG_DIR) -> "Settings":
        """Load YAML defaults, then apply supported environment overrides."""
        raw: dict[str, Any] = {}
        for name in ("app", "database", "models", "storage"):
            config_file = config_dir / f"{name}.yaml"
            if config_file.exists():
                with config_file.open("r", encoding="utf-8") as stream:
                    values = yaml.safe_load(stream) or {}
                if not isinstance(values, dict):
                    raise ValueError(
                        f"Configuration file must contain an object: {config_file}"
                    )
                raw[name] = values

        settings = cls(**raw)
        settings._apply_environment_overrides()
        return settings

    def _apply_environment_overrides(self) -> None:
        """Apply explicit nested environment variables without exposing secrets."""
        import os

        mappings: dict[str, tuple[str, str]] = {
            "CLIPSTUDIO_ENVIRONMENT": ("app", "environment"),
            "CLIPSTUDIO_DEBUG": ("app", "debug"),
            "CLIPSTUDIO_HOST": ("app", "host"),
            "CLIPSTUDIO_PORT": ("app", "port"),
            "CLIPSTUDIO_DATABASE_URL": ("database", "url"),
            "CLIPSTUDIO_STORAGE_PATH": ("storage", "path"),
            "CLIPSTUDIO_LOG_PATH": ("storage", "log_path"),
        }
        for env_name, (section_name, field_name) in mappings.items():
            value = os.getenv(env_name)
            if value is None:
                continue
            section = getattr(self, section_name)
            raw_value: str | bool | int = value
            if field_name == "debug":
                raw_value = value.lower() in {"1", "true", "yes", "on"}
            elif field_name == "port":
                raw_value = int(value)
            setattr(
                self, section_name, section.model_copy(update={field_name: raw_value})
            )

    def public_dict(self) -> dict[str, Any]:
        """Return diagnostics-safe configuration without credentials."""
        return {
            "app": self.app.model_dump(mode="json"),
            "database": {"driver": self.database.url.split(":", 1)[0]},
            "models": self.models.model_dump(mode="json"),
            "storage": {
                "path": str(self.storage.path),
                "log_path": str(self.storage.log_path),
                "max_cache_mb": self.storage.max_cache_mb,
            },
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide validated settings instance."""
    return Settings.load()
