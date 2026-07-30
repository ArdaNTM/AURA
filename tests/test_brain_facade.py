from aura.brain.brain import Brain


def test_brain_thinks_about_tool_request():
    brain = Brain()

    decision, action = brain.think(
        "5 + 5 hesapla",
    )

    assert decision.intent == "calculation"

    assert decision.requires_tool

    assert action.name == "execute_tool"


def test_brain_thinks_about_conversation():
    brain = Brain()

    decision, action = brain.think(
        "Merhaba AURA",
    )

    assert decision.intent == "conversation"

    assert not decision.requires_tool

    assert action.name == "generate_response"