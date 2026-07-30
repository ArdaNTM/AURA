from aura.core.container import Container


class Service:
    pass


def test_register_instance():
    container = Container()
    service = Service()

    container.register_instance(Service, service)

    assert container.resolve(Service) is service


def test_register_factory():
    container = Container()

    container.register_factory(Service, lambda c: Service())

    first = container.resolve(Service)
    second = container.resolve(Service)

    assert first is second


def test_has():
    container = Container()

    assert not container.has(Service)

    container.register_instance(Service, Service())

    assert container.has(Service)


def test_clear():
    container = Container()

    container.register_instance(Service, Service())

    container.clear()

    assert not container.has(Service)
    assert container.resolve(Container) is container


def test_unknown_service():
    container = Container()

    try:
        container.resolve(Service)
        assert False
    except KeyError:
        pass
