"""Simple dependency injection container."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


class Container:
    """Simple dependency injection container."""

    def __init__(self) -> None:
        self._instances: dict[type[Any], Any] = {}
        self._factories: dict[type[Any], Callable[[Container], Any]] = {}

        self.register_instance(Container, self)

    def register_instance(self, service_type: type[T], instance: T) -> None:
        """Register an existing singleton instance."""
        self._instances[service_type] = instance

    def register_factory(
        self,
        service_type: type[T],
        factory: Callable[[Container], T],
    ) -> None:
        """Register a lazy singleton factory."""
        self._factories[service_type] = factory

    def resolve(self, service_type: type[T]) -> T:
        """Resolve a service."""
        if service_type in self._instances:
            return self._instances[service_type]

        if service_type in self._factories:
            instance = self._factories[service_type](self)
            self._instances[service_type] = instance
            return instance

        raise KeyError(f"{service_type.__name__} is not registered.")

    def has(self, service_type: type[Any]) -> bool:
        """Return True if a service is registered."""
        return (
            service_type in self._instances
            or service_type in self._factories
        )

    def clear(self) -> None:
        """Remove all registrations."""
        self._instances.clear()
        self.register_instance(Container, self)