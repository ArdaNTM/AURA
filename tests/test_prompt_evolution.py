from aura.brain.learning import LearningContext
from aura.brain.prompt_evolution import PromptEvolution


def test_prompt_evolution_learns_strategy():

    context = LearningContext(
        [
            (
                "assistant",
                ("strategy=safe_tool_execution;" "success=True;"),
            )
        ]
    )

    result = PromptEvolution().evolve(
        context,
    )

    assert result["preferred_strategy"] == "safe_tool_execution"


def test_prompt_evolution_detects_failures():

    context = LearningContext(
        [
            (
                "assistant",
                ("strategy=tool_execution;" "success=False;" "error=hata"),
            )
        ]
    )

    result = PromptEvolution().evolve(
        context,
    )

    assert "Analyze previous failures before deciding." in result["instructions"]
