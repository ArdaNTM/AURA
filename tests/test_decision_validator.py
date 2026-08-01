from aura.brain.capability import CapabilityRegistry
from aura.brain.decision_validator import DecisionValidator
from aura.brain.models import Decision
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_validator_accepts_valid_tool():

    tools = ToolRegistry()

    tools.register(
        CalculatorTool(),
    )

    validator = DecisionValidator(
        CapabilityRegistry(
            tools,
        ),
    )

    decision = Decision(
        intent="calculation",
        target="calculator",
        requires_tool=True,
    )

    result = validator.validate(
        decision,
    )

    assert result.valid


def test_validator_rejects_wrong_tool():

    validator = DecisionValidator(
        CapabilityRegistry(),
    )

    decision = Decision(
        intent="calculation",
        target="filesystem",
        requires_tool=True,
    )

    result = validator.validate(
        decision,
    )

    assert not result.valid
