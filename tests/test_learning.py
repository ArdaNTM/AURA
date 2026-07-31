from aura.brain.learning import LearningContext


def test_learning_context_stores_memories():
    context = LearningContext(
        [
            (
                "assistant",
                "Previous calculation failed.",
            ),
        ],
    )

    assert (
        len(
            context.memories,
        )
        == 1
    )


def test_learning_context_creates_summary():
    context = LearningContext(
        [
            (
                "assistant",
                "Previous calculation failed.",
            ),
            (
                "assistant",
                "Retry succeeded.",
            ),
        ],
    )

    summary = context.summarize()

    assert summary["memory_count"] == 2

    assert summary["previous_experience"] == context.memories


def test_learning_context_calculates_strategy_scores():
    context = LearningContext(
        [
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=tool_execution; "
                    "success=True; "
                    "output=10"
                ),
            ),
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True; "
                    "output=10"
                ),
            ),
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True; "
                    "output=20"
                ),
            ),
        ],
    )

    scores = context.strategy_scores()

    assert scores["tool_execution"] == 1

    assert scores["safe_tool_execution"] == 2


def test_learning_context_finds_preferred_strategy():
    context = LearningContext(
        [
            (
                "assistant",
                ("strategy=tool_execution; " "success=True"),
            ),
            (
                "assistant",
                ("strategy=safe_tool_execution; " "success=True"),
            ),
            (
                "assistant",
                ("strategy=safe_tool_execution; " "success=True"),
            ),
        ],
    )

    assert context.preferred_strategy() == "safe_tool_execution"


def test_learning_context_calculates_strategy_confidence():
    context = LearningContext(
        [
            (
                "assistant",
                ("strategy=tool_execution; " "success=True"),
            ),
            (
                "assistant",
                ("strategy=safe_tool_execution; " "success=True"),
            ),
            (
                "assistant",
                ("strategy=safe_tool_execution; " "success=True"),
            ),
            (
                "assistant",
                ("strategy=safe_tool_execution; " "success=True"),
            ),
        ],
    )

    assert context.strategy_confidence() == 0.75


def test_learning_context_calculates_success_rate():
    context = LearningContext(
        [
            (
                "assistant",
                "success=True",
            ),
            (
                "assistant",
                "success=True",
            ),
            (
                "assistant",
                "success=False",
            ),
            (
                "assistant",
                "success=True",
            ),
        ],
    )

    assert context.success_rate() == 0.75


def test_learning_context_calculates_learning_quality():
    context = LearningContext(
        [
            (
                "assistant",
                ("strategy=safe_tool_execution; " "success=True"),
            ),
            (
                "assistant",
                ("strategy=safe_tool_execution; " "success=True"),
            ),
            (
                "assistant",
                ("strategy=tool_execution; " "success=True"),
            ),
            (
                "assistant",
                ("strategy=tool_execution; " "success=False"),
            ),
        ],
    )

    assert (
        round(
            context.learning_quality(),
            3,
        )
        == 0.717
    )
