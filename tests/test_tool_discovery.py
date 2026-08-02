from aura.brain.tool_discovery import ToolDiscovery
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_discovers_registered_tools():
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    discovery = ToolDiscovery(
        registry,
    )

    assert discovery.available_tools() == [
        "calculator",
    ]


def test_discovers_tool_metadata():
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    discovery = ToolDiscovery(
        registry,
    )

    schemas = discovery.available_schemas()

    assert schemas[0]["capability"] == "calculation"
