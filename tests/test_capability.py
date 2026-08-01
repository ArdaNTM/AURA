from aura.brain.capability import CapabilityRegistry
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_calculation_capability_available_when_tool_exists():
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    capabilities = CapabilityRegistry(
        registry,
    )

    assert capabilities.is_available(
        "calculation",
    )


def test_calculation_capability_unavailable_without_tool():
    capabilities = CapabilityRegistry()

    assert not capabilities.is_available(
        "calculation",
    )
