from aura.brain.planner import Planner
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


def test_empty_discovery_without_registry():
    discovery = ToolDiscovery()

    assert discovery.available_tools() == []

    assert discovery.available_schemas() == []


def test_planner_creates_tool_execution_for_capability():
    planner = Planner()

    decision = planner.decide(
        "internette ara",
    )

    assert decision.strategy == "tool_execution"

    assert decision.intent == "search"

    assert decision.requires_tool


def test_finds_tool_by_capability():
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    discovery = ToolDiscovery(
        registry,
    )

    assert (
        discovery.find_tool(
            "calculation",
        )
        == "calculator"
    )
