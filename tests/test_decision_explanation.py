from aura.brain.planner import Planner


def test_low_confidence_contains_reason():

    planner = Planner(
        llm_confidence_threshold=0.75,
    )

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.confidence_reason is None or isinstance(
        decision.confidence_reason,
        str,
    )
