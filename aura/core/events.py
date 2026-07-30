"""Simple publish/subscribe event bus."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T", bound="Event")


class Event:
    """Base class for all events."""


class EventBus:
    """Simple synchronous event bus."""

    def __init__(self) -> None:
        self._subscribers: dict[
            type[Event],
            list[Callable[[Event], None]],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: type[T],
        handler: Callable[[T], None],
    ) -> None:
        self._subscribers[event_type].append(handler)

    def unsubscribe(
        self,
        event_type: type[T],
        handler: Callable[[T], None],
    ) -> None:
        handlers = self._subscribers.get(event_type)
        if handlers and handler in handlers:
            handlers.remove(handler)

    def publish(self, event: Event) -> None:
        for handler in self._subscribers[type(event)]:
            handler(event)

    def clear(self) -> None:
        self._subscribers.clear()
