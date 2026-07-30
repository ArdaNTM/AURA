"""Application lifecycle management."""

from __future__ import annotations

from abc import ABC
from collections.abc import Iterable


class Lifecycle(ABC):
    """Base lifecycle interface."""

    def startup(self) -> None:
        pass

    def shutdown(self) -> None:
        pass


class LifecycleManager:
    """Coordinates application startup and shutdown."""

    def __init__(self) -> None:
        self._services: list[Lifecycle] = []

    def register(self, service: Lifecycle) -> None:
        self._services.append(service)

    def startup(self) -> None:
        for service in self._services:
            service.startup()

    def shutdown(self) -> None:
        for service in reversed(self._services):
            service.shutdown()

    def services(self) -> Iterable[Lifecycle]:
        return tuple(self._services)
