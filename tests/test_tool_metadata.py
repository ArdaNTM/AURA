from aura.tools import CalculatorTool


def test_calculator_tool_metadata():
    tool = CalculatorTool()

    assert tool.name == "calculator"

    assert tool.capability == "calculation"

    assert tool.risk_level == "low"

    assert not tool.requires_permission


def test_tool_schema_contains_metadata():
    tool = CalculatorTool()

    schema = tool.schema()

    assert schema["capability"] == "calculation"

    assert schema["risk_level"] == "low"

    assert schema["requires_permission"] is False
