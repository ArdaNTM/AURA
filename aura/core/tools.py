"""Tool abstractions and registry."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from aura.core.tool_result import ToolResult


class Tool(ABC):
    """Base class for executable tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name."""

    @property
    def description(self) -> str:
        """Human-readable tool description."""
        return ""

    @property
    def capability(self) -> str:
        """Capability provided by this tool."""
        return "unknown"

    @property
    def risk_level(self) -> str:
        """Execution risk level."""
        return "low"

    @property
    def requires_permission(self) -> bool:
        """Whether execution requires permission."""
        return False

    @property
    def parameters(self) -> dict[str, Any]:
        """Tool parameter schema."""
        return {}

    def schema(self) -> dict[str, Any]:
        """Return AURA internal tool schema."""

        return {
            "name": self.name,
            "description": self.description,
            "capability": self.capability,
            "risk_level": self.risk_level,
            "requires_permission": self.requires_permission,
            "parameters": self.parameters,
        }

    def openai_schema(self) -> dict[str, Any]:
        """Return OpenAI function tool schema."""

        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self.parameters,
                "required": list(
                    self.parameters.keys(),
                ),
            },
        }

    @abstractmethod
    def execute(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute the tool."""


class ToolRegistry:
    """Registry of executable tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(
        self,
        tool: Tool,
    ) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")

        self._tools[tool.name] = tool

    def unregister(
        self,
        name: str,
    ) -> None:
        self._tools.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ) -> Tool:
        try:
            return self._tools[name]

        except KeyError as exc:
            raise KeyError(f"Unknown tool '{name}'.") from exc

    def execute(
        self,
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> ToolResult:
        """Execute a tool and return standardized result."""

        try:
            output = self.get(name).execute(
                *args,
                **kwargs,
            )

            if isinstance(
                output,
                ToolResult,
            ):
                return output

            return ToolResult(
                name=name,
                output=str(output),
            )

        except KeyError as exc:
            return ToolResult(
                name=name,
                output="",
                success=False,
                error=exc.args[0],
            )

        except Exception as exc:
            return ToolResult(
                name=name,
                output="",
                success=False,
                error=str(exc),
            )

        except KeyError as exc:
            return ToolResult(
                name=name,
                output="",
                success=False,
                error=exc.args[0],
            )

        except Exception as exc:
            return ToolResult(
                name=name,
                output="",
                success=False,
                error=str(exc),
            )

    def list_tools(self) -> list[str]:
        """Return registered tool names."""

        return sorted(
            self._tools,
        )

    def has(
        self,
        name: str,
    ) -> bool:
        """Check whether a tool exists."""

        return name in self._tools

    def descriptions(
        self,
    ) -> list[dict[str, str]]:
        """Return available tool descriptions."""

        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in self._tools.values()
        ]

    def schemas(self) -> list[dict[str, Any]]:
        """Return AURA schemas."""

        return [self._tools[name].schema() for name in sorted(self._tools)]

    def openai_schemas(self) -> list[dict[str, Any]]:
        """Return OpenAI compatible schemas."""

        return [self._tools[name].openai_schema() for name in sorted(self._tools)]

    def clear(self) -> None:
        """Remove all registered tools."""

        self._tools.clear()
