from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class UserProfile:
    """Persistent user personalization data."""

    preferences: dict[str, str] = field(
        default_factory=dict,
    )

    coding_style: dict[str, str] = field(
        default_factory=dict,
    )

    workflow: dict[str, str] = field(
        default_factory=dict,
    )

    favorite_tools: list[str] = field(
        default_factory=list,
    )

    communication_style: dict[str, str] = field(
        default_factory=dict,
    )

    def set_preference(
        self,
        key: str,
        value: str,
    ) -> None:
        """Store user preference."""

        self.preferences[key] = value

    def set_coding_style(
        self,
        key: str,
        value: str,
    ) -> None:
        """Store coding preference."""

        self.coding_style[key] = value

    def add_tool(
        self,
        tool: str,
    ) -> None:
        """Remember preferred tool."""

        if tool not in self.favorite_tools:
            self.favorite_tools.append(
                tool,
            )

    def set_workflow(
        self,
        key: str,
        value: str,
    ) -> None:
        """Store workflow preference."""

        self.workflow[key] = value

    def set_communication_style(
        self,
        key: str,
        value: str,
    ) -> None:
        """Store communication preference."""

        self.communication_style[key] = value
