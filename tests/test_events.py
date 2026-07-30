from aura.core.events import Event, EventBus


class SampleEvent(Event):
    def __init__(self, value: int) -> None:
        self.value = value


def test_publish():
    bus = EventBus()
    received: list[int] = []

    def handler(event: SampleEvent) -> None:
        received.append(event.value)

    bus.subscribe(SampleEvent, handler)

    bus.publish(SampleEvent(42))

    assert received == [42]


def test_unsubscribe():
    bus = EventBus()
    received: list[int] = []

    def handler(event: SampleEvent) -> None:
        received.append(event.value)

    bus.subscribe(SampleEvent, handler)
    bus.unsubscribe(SampleEvent, handler)

    bus.publish(SampleEvent(1))

    assert received == []


def test_clear():
    bus = EventBus()
    received: list[int] = []

    def handler(event: SampleEvent) -> None:
        received.append(event.value)

    bus.subscribe(SampleEvent, handler)

    bus.clear()

    bus.publish(SampleEvent(1))

    assert received == []
