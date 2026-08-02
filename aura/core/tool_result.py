from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ToolResult:
    """Result produced by a tool execution."""

    name: str

    output: str

    success: bool = True

    error: str | None = None

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
