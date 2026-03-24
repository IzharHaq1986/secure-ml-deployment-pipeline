"""
Application configuration for the Secure ML Deployment Pipeline service.

This module centralizes environment-backed settings so startup behavior
is predictable, validated, and easy to test.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Strongly typed application settings loaded from environment variables.
    """

    port: int = Field(default=8000, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")
    model_name: str = Field(alias="MODEL_NAME")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, value: int) -> int:
        """
        Ensure the application port is within the valid TCP range.
        """
        if not 1 <= value <= 65535:
            raise ValueError("PORT must be between 1 and 65535.")
        return value

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, value: str) -> str:
        """
        Ensure the model name is present and not blank.
        """
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("MODEL_NAME cannot be empty.")

        return cleaned_value


def get_settings() -> Settings:
    """
    Load and validate application settings.

    Raises:
        ValidationError: If required configuration is missing or invalid.
    """
    return Settings()
