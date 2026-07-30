from aura.core.ai_events import (
    AIResponseCompleted,
    AIResponseStarted,
    ToolCompleted,
    ToolFailed,
    ToolStarted,
)
from aura.core.event_logger import EventLogger
from aura.core.events import EventBus


class FakeLogger:
    """Capture log calls for testing."""

    def __init__(self) -> None:
        self.messages = []

    def info(
        self,
        message: str,
        *args,
    ) -> None:
        self.messages.append(
            (
                "info",
                message,
                args,
            )
        )

    def error(
        self,
        message: str,
        *args,
    ) -> None:
        self.messages.append(
            (
                "error",
                message,
                args,
            )
        )


def test_event_logger_receives_ai_events() -> None:
    bus = EventBus()
    logger = FakeLogger()

    EventLogger(
        bus,
        logger,
    )

    bus.publish(
        AIResponseStarted(
            "Merhaba",
        )
    )

    bus.publish(
        AIResponseCompleted(
            "Selam",
        )
    )

    assert len(logger.messages) == 2

    assert logger.messages[0] == (
        "info",
        "AI started: %s",
        ("Merhaba",),
    )

    assert logger.messages[1] == (
        "info",
        "AI completed: %s",
        ("Selam",),
    )


def test_event_logger_receives_tool_events() -> None:
    bus = EventBus()
    logger = FakeLogger()

    EventLogger(
        bus,
        logger,
    )

    bus.publish(
        ToolStarted(
            "calculator",
        )
    )

    bus.publish(
        ToolCompleted(
            "calculator",
            "4",
        )
    )

    bus.publish(
        ToolFailed(
            "calculator",
            "invalid expression",
        )
    )

    assert len(logger.messages) == 3

    assert logger.messages[0] == (
        "info",
        "Tool started: %s",
        ("calculator",),
    )

    assert logger.messages[1] == (
        "info",
        "Tool completed: %s -> %s",
        (
            "calculator",
            "4",
        ),
    )

    assert logger.messages[2] == (
        "error",
        "Tool failed: %s -> %s",
        (
            "calculator",
            "invalid expression",
        ),
    )