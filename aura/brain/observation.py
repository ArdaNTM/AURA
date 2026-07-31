"""Observation models for AURA agent loop."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Observation:
    """Result observed after executing an action."""

    source: str

    output: str

    success: bool = True

    metadata: dict[str, object] | None = None
