from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ToolResult:
    """Result produced by a tool execution."""

    name: str

    output: str

    success: bool = True

    error: str | None = None

    duration: float = 0.0

    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat(),
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
