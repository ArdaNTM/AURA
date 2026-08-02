from aura.brain.planner import Planner


def test_decision_tracks_outcome():

    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.outcome == {}
