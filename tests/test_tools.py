from aura.core.tools import Tool, ToolRegistry


class EchoTool(Tool):
    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Echo the provided value."

    @property
    def parameters(self) -> dict:
        return {
            "value": {
                "type": "string",
                "description": "Value to echo.",
            }
        }

    def execute(
        self,
        value: str,
    ) -> str:
        return value


class FailingTool(Tool):

    @property
    def name(self) -> str:
        return "failing"

    def execute(self) -> str:
        raise ValueError("Tool failed.")


def test_register() -> None:
    registry = ToolRegistry()

    registry.register(
        EchoTool(),
    )

    assert registry.list_tools() == [
        "echo",
    ]


def test_execute_returns_tool_result() -> None:
    registry = ToolRegistry()

    registry.register(
        EchoTool(),
    )

    result = registry.execute(
        "echo",
        "hello",
    )

    assert result.success
    assert result.name == "echo"
    assert result.output == "hello"
    assert result.error is None


def test_execute_failure_returns_tool_result() -> None:
    registry = ToolRegistry()

    registry.register(
        FailingTool(),
    )

    result = registry.execute(
        "failing",
    )

    assert not result.success
    assert result.name == "failing"
    assert result.output == ""
    assert result.error == "Tool failed."


def test_unregister() -> None:
    registry = ToolRegistry()

    registry.register(
        EchoTool(),
    )

    registry.unregister(
        "echo",
    )

    assert registry.list_tools() == []


def test_duplicate_registration() -> None:
    registry = ToolRegistry()

    registry.register(
        EchoTool(),
    )

    try:
        registry.register(
            EchoTool(),
        )

        assert False

    except ValueError:
        pass


def test_unknown_tool() -> None:
    registry = ToolRegistry()

    result = registry.execute(
        "missing",
    )

    assert not result.success
    assert result.name == "missing"
    assert result.output == ""
    assert result.error == "Unknown tool 'missing'."


def test_tool_schema() -> None:
    tool = EchoTool()

    assert tool.schema() == {
        "name": "echo",
        "description": "Echo the provided value.",
        "parameters": {
            "value": {
                "type": "string",
                "description": "Value to echo.",
            }
        },
    }


def test_registry_schemas() -> None:
    registry = ToolRegistry()

    registry.register(
        EchoTool(),
    )

    assert registry.schemas() == [
        {
            "name": "echo",
            "description": "Echo the provided value.",
            "parameters": {
                "value": {
                    "type": "string",
                    "description": "Value to echo.",
                }
            },
        }
    ]


def test_openai_tool_schema() -> None:
    tool = EchoTool()

    assert tool.openai_schema() == {
        "type": "function",
        "name": "echo",
        "description": "Echo the provided value.",
        "parameters": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "description": "Value to echo.",
                }
            },
            "required": [
                "value",
            ],
        },
    }


def test_registry_openai_schemas() -> None:
    registry = ToolRegistry()

    registry.register(
        EchoTool(),
    )

    assert registry.openai_schemas() == [
        {
            "type": "function",
            "name": "echo",
            "description": "Echo the provided value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "string",
                        "description": "Value to echo.",
                    }
                },
                "required": [
                    "value",
                ],
            },
        }
    ]
