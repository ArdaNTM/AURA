from aura.ai.factory import ProviderFactory
from aura.ai.providers.dummy_provider import DummyProvider
from aura.ai.providers.openai_provider import OpenAIProvider
from aura.config.settings import Settings


def test_factory_creates_dummy_provider() -> None:
    settings = Settings(
        _env_file=None,
        model_provider="dummy",
    )

    provider = ProviderFactory.create(settings)

    assert isinstance(provider, DummyProvider)


def test_factory_creates_openai_provider() -> None:
    settings = Settings(
        _env_file=None,
        model_provider="openai",
        openai_api_key="test-key",
    )

    provider = ProviderFactory.create(settings)

    assert isinstance(provider, OpenAIProvider)


def test_register_custom_provider() -> None:
    class CustomProvider(DummyProvider):
        @property
        def name(self) -> str:
            return "custom"

    ProviderFactory.register(
        "custom",
        lambda settings: CustomProvider(),
    )

    settings = Settings(
        _env_file=None,
        model_provider="dummy",
    )

    settings.model_provider = "custom"  # type: ignore

    provider = ProviderFactory.create(settings)

    assert isinstance(provider, CustomProvider)