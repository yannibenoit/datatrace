"""DataTrace Settings Configuration.

Centralized configuration management using Pydantic Settings.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BigQuerySettings(BaseSettings):
    """BigQuery connection settings."""

    model_config = SettingsConfigDict(env_prefix="BIGQUERY_")

    project_id: str = ""
    credentials_path: Optional[str] = None
    location: str = "US"
    timeout: int = 30
    max_results: int = 10000


class PowerBISettings(BaseSettings):
    """Power BI connection settings."""

    model_config = SettingsConfigDict(env_prefix="POWERBI_")

    client_id: str = ""
    tenant_id: str = ""
    client_secret: Optional[str] = None
    scope: str = "https://analysis.windows.net/powerbi/api/.default"
    authority: str = "https://login.microsoftonline.com/{tenant_id}"


class dbtSettings(BaseSettings):
    """dbt connection settings."""

    model_config = SettingsConfigDict(env_prefix="DBT_")

    project_dir: str = "./dbt"
    profiles_yml: str = "./dbt/profiles.yml"
    target_path: str = "./dbt/target"


class MetadataSettings(BaseSettings):
    """Metadata storage settings."""

    model_config = SettingsConfigDict(env_prefix="METADATA_")

    dataset_id: str = "datatrace_metadata"
    location: str = "US"
    partition_expiration_days: int = 3650  # 10 years


class APISettings(BaseSettings):
    """API server settings."""

    model_config = SettingsConfigDict(env_prefix="API_")

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    workers: int = 4


class Settings(BaseSettings):
    """Main DataTrace settings.

    Aggregates all configuration settings from environment variables
    and configuration files.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application settings
    app_name: str = "DataTrace"
    environment: str = "development"
    log_level: str = "INFO"

    # Sub-settings
    bigquery: BigQuerySettings = BigQuerySettings()
    powerbi: PowerBISettings = PowerBISettings()
    dbt: dbtSettings = dbtSettings()
    metadata: MetadataSettings = MetadataSettings()
    api: APISettings = APISettings()


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance with all configuration loaded
    """
    return Settings()
