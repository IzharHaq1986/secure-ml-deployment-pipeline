import pytest
from pydantic import ValidationError

from app.config import get_settings


def clear_config_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Remove configuration-related environment variables so each test
    starts from a clean and predictable state.
    """

    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.delenv("DEBUG", raising=False)
    monkeypatch.delenv("MODEL_NAME", raising=False)


def test_valid_config_loads(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Valid configuration should load successfully and return typed values.
    """

    clear_config_env(monkeypatch)

    monkeypatch.setenv("PORT", "8000")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("MODEL_NAME", "fraud-model-v1")

    settings = get_settings()

    assert settings.port == 8000
    assert settings.debug is True
    assert settings.model_name == "fraud-model-v1"


def test_missing_model_name_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Missing MODEL_NAME should fail validation because it is required.
    """

    clear_config_env(monkeypatch)

    monkeypatch.setenv("PORT", "8000")
    monkeypatch.setenv("DEBUG", "false")

    with pytest.raises(ValidationError) as error_info:
        get_settings()

    assert "MODEL_NAME" in str(error_info.value)


def test_invalid_port_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Non-numeric PORT should fail validation.
    """

    clear_config_env(monkeypatch)

    monkeypatch.setenv("PORT", "invalid-port")
    monkeypatch.setenv("DEBUG", "false")
    monkeypatch.setenv("MODEL_NAME", "fraud-model-v1")

    with pytest.raises(ValidationError) as error_info:
        get_settings()

    assert "PORT" in str(error_info.value)


def test_empty_model_name_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Blank MODEL_NAME should fail validation.
    """

    clear_config_env(monkeypatch)

    monkeypatch.setenv("PORT", "8000")
    monkeypatch.setenv("DEBUG", "false")
    monkeypatch.setenv("MODEL_NAME", "   ")

    with pytest.raises(ValidationError) as error_info:
        get_settings()

    assert "MODEL_NAME cannot be empty" in str(error_info.value)
