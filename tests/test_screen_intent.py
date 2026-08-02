from aura.brain.intent import IntentEngine


def test_detects_screen_intent():
    engine = IntentEngine()

    result = engine.classify(
        "ekran görüntüsü al",
    )

    assert result.intent == "screen"
