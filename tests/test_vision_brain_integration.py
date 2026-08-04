from aura.brain.brain import Brain


def test_brain_receives_vision_context():

    brain = Brain()

    decision, action = brain.think(
        "ekranda ne var",
        vision={
            "objects": [
                "window",
            ],
            "confidence": 0.8,
        },
    )

    assert decision is not None

    assert decision.metadata["vision"]["confidence"] == 0.8
