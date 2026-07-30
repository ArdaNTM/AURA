from aura.tools.calculator import CalculatorTool


def test_calculator_addition() -> None:
    tool = CalculatorTool()

    assert tool.execute("2 + 3") == "5"


def test_calculator_multiplication() -> None:
    tool = CalculatorTool()

    assert tool.execute("4 * 5") == "20"


def test_calculator_parentheses() -> None:
    tool = CalculatorTool()

    assert tool.execute("(2 + 3) * 4") == "20"


def test_calculator_schema() -> None:
    tool = CalculatorTool()

    assert tool.schema() == {
        "name": "calculator",
        "description": "Evaluate basic mathematical expressions.",
        "parameters": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to evaluate.",
            }
        },
    }


def test_calculator_rejects_invalid_expression() -> None:
    tool = CalculatorTool()

    try:
        tool.execute("import os")
        assert False
    except ValueError:
        pass