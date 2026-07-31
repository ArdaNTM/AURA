from aura.brain.planner import Planner


def test_planner_detects_calculation():
    planner = Planner()

    decision = planner.decide(
        "5 + 5 hesapla",
    )

    assert decision.intent == "calculation"

    assert decision.requires_tool

    assert decision.confidence == 0.9

    assert decision.priority == "normal"

    assert decision.risk_level == "low"

    assert decision.strategy == "tool_execution"

    assert decision.explanation is not None

    assert len(decision.plan) == 2

    assert decision.metadata["expression"] == "5+5"


def test_planner_detects_conversation():
    planner = Planner()

    decision = planner.decide(
        "Merhaba AURA",
    )

    assert decision.intent == "conversation"

    assert not decision.requires_tool

    assert decision.confidence == 0.7

    assert decision.priority == "normal"

    assert decision.risk_level == "low"

    assert decision.strategy == "direct_answer"

    assert decision.explanation is not None


def test_planner_uses_safe_strategy_after_failure():
    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
        learning={
            "has_failures": True,
        },
    )

    assert decision.strategy == "safe_tool_execution"

    assert decision.risk_level == "medium"


def test_planner_keeps_normal_strategy_without_failure():
    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
        learning={
            "has_failures": False,
        },
    )

    assert decision.strategy == "tool_execution"

    assert decision.risk_level == "low"


def test_planner_prefers_successful_strategy():
    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
        learning={
            "successful_strategies": [
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True; "
                    "output=10"
                ),
            ],
        },
    )

    assert decision.strategy == "safe_tool_execution"

    assert decision.risk_level == "medium"


def test_planner_prefers_normal_strategy_from_success_history():
    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
        learning={
            "successful_strategies": [
                (
                    "intent=calculation; "
                    "strategy=tool_execution; "
                    "success=True; "
                    "output=10"
                ),
            ],
        },
    )

    assert decision.strategy == "tool_execution"

    assert decision.risk_level == "low"


def test_planner_switches_to_safe_strategy_when_learning_quality_is_low():
    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
        learning={
            "learning_quality": 0.3,
            "preferred_strategy": "tool_execution",
            "strategy_confidence": 0.9,
        },
    )

    assert decision.strategy == "safe_tool_execution"

    assert decision.risk_level == "medium"

    assert decision.confidence == 0.75


def test_planner_keeps_preferred_strategy_when_learning_quality_is_high():
    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
        learning={
            "learning_quality": 0.9,
            "preferred_strategy": "tool_execution",
            "strategy_confidence": 0.8,
        },
    )

    assert decision.strategy == "tool_execution"

    assert decision.risk_level == "low"

    assert decision.confidence == 0.9
