import pytest

from aura.config.settings import Settings


def test_settings_have_safe_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.aura_name == "AURA"
    assert settings.model_provider == "dummy"
    assert settings.log_level == "INFO"


def test_provider_name_is_normalized() -> None:
    settings = Settings(
        _env_file=None,
        model_provider="OPENAI",
        openai_api_key="test-key",
    )

    assert settings.model_provider == "openai"


def test_log_level_is_normalized() -> None:
    settings = Settings(
        _env_file=None,
        log_level="debug",
    )

    assert settings.log_level == "DEBUG"


def test_invalid_log_level_raises_error() -> None:
    with pytest.raises(ValueError):
        Settings(
            _env_file=None,
            log_level="INVALID",
        )


def test_openai_provider_requires_api_key() -> None:
    with pytest.raises(ValueError):
        Settings(
            _env_file=None,
            model_provider="openai",
        )


def test_openai_provider_accepts_api_key() -> None:
    settings = Settings(
        _env_file=None,
        model_provider="openai",
        openai_api_key="test-key",
    )

    assert settings.model_provider == "openai"
    assert settings.openai_api_key is not None