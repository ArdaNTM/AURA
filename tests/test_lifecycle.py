from aura.core.lifecycle import Lifecycle, LifecycleManager


class Dummy(Lifecycle):
    def __init__(self, log: list[str], name: str):
        self.log = log
        self.name = name

    def startup(self):
        self.log.append(f"{self.name}:start")

    def shutdown(self):
        self.log.append(f"{self.name}:stop")


def test_startup_order():
    log = []

    manager = LifecycleManager()

    manager.register(Dummy(log, "a"))
    manager.register(Dummy(log, "b"))

    manager.startup()

    assert log == [
        "a:start",
        "b:start",
    ]


def test_shutdown_reverse_order():
    log = []

    manager = LifecycleManager()

    manager.register(Dummy(log, "a"))
    manager.register(Dummy(log, "b"))

    manager.shutdown()

    assert log == [
        "b:stop",
        "a:stop",
    ]