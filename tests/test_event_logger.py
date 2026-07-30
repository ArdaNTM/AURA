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
    def __init__(self) -> None:
        self.messages = []

    def info(self, message, *args):
        self.messages.append(
            ("info", message, args)
        )

    def error(self, message, *args):
        self.messages.append(
            ("error", message, args)
        )


def test_event_logger_subscribes_events() -> None:
    bus = EventBus()
    logger = FakeLogger()

    EventLogger(
        bus,
        logger,
    )

    bus.publish(
        AIResponseStarted(
            "hello",
        )
    )

    bus.publish(
        ToolStarted(
            "echo",
        )
    )

    bus.publish(
        ToolCompleted(
            "echo",
            "hello",
        )
    )

    bus.publish(
        ToolFailed(
            "missing",
            "not found",
        )
    )

    bus.publish(
        AIResponseCompleted(
            "done",
        )
    )

    assert len(logger.messages) == 5