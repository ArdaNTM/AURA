from aura.ai.manager import AIManager
from aura.ai.providers.dummy_provider import DummyProvider


def test_dummy_provider_answers_greeting() -> None:
    manager = AIManager(DummyProvider())

    assert manager.provider.name == "dummy"

    assert (
        manager.respond("Merhaba")
        == "Merhaba! Ben AURA. Şimdilik çekirdek modundayım."
    )


def test_dummy_provider_echoes_other_messages() -> None:
    manager = AIManager(DummyProvider())

    assert (
        manager.respond("Bugün ne yapıyoruz?")
        == "Mesajını aldım: Bugün ne yapıyoruz?"
    )