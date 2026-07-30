"""Standardized tool execution result."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ToolResult:
    """Result produced by a tool execution."""

    name: str
    output: str
    success: bool = True
    error: str | None = None
