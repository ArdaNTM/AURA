from aura.config.settings import Settings


def test_settings_have_safe_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.aura_name == "AURA"
    assert settings.model_provider == "dummy"
    assert settings.log_level == "INFO"
