"""Event based logging for AURA."""

from __future__ import annotations

import logging

from aura.core.ai_events import (
    AIResponseCompleted,
    AIResponseStarted,
    ToolCompleted,
    ToolFailed,
    ToolStarted,
)
from aura.core.events import EventBus


class EventLogger:
    """Subscribe to AURA events and write logs."""

    def __init__(
        self,
        event_bus: EventBus,
        logger: logging.Logger,
    ) -> None:
        self._logger = logger

        event_bus.subscribe(
            AIResponseStarted,
            self.on_ai_started,
        )

        event_bus.subscribe(
            AIResponseCompleted,
            self.on_ai_completed,
        )

        event_bus.subscribe(
            ToolStarted,
            self.on_tool_started,
        )

        event_bus.subscribe(
            ToolCompleted,
            self.on_tool_completed,
        )

        event_bus.subscribe(
            ToolFailed,
            self.on_tool_failed,
        )

    def on_ai_started(
        self,
        event: AIResponseStarted,
    ) -> None:
        self._logger.info(
            "AI started: %s",
            event.message,
        )

    def on_ai_completed(
        self,
        event: AIResponseCompleted,
    ) -> None:
        self._logger.info(
            "AI completed: %s",
            event.response,
        )

    def on_tool_started(
        self,
        event: ToolStarted,
    ) -> None:
        self._logger.info(
            "Tool started: %s",
            event.name,
        )

    def on_tool_completed(
        self,
        event: ToolCompleted,
    ) -> None:
        self._logger.info(
            "Tool completed: %s -> %s",
            event.name,
            event.output,
        )

    def on_tool_failed(
        self,
        event: ToolFailed,
    ) -> None:
        self._logger.error(
            "Tool failed: %s -> %s",
            event.name,
            event.error,
        )
