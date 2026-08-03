from aura.brain.task_graph import TaskGraph


def test_task_graph_dependency_flow():

    graph = TaskGraph()

    concept = graph.add_task(
        "Concept",
    )

    code = graph.add_task(
        "Code",
    )

    test = graph.add_task(
        "Test",
    )

    graph.add_dependency(
        code,
        concept,
    )

    graph.add_dependency(
        test,
        code,
    )

    available = graph.next_available()

    assert len(available) == 1

    assert available[0].task == "Concept"


def test_completed_dependency_unlocks_task():

    graph = TaskGraph()

    first = graph.add_task(
        "Design",
    )

    second = graph.add_task(
        "Code",
    )

    graph.add_dependency(
        second,
        first,
    )

    graph.complete(
        first,
    )

    available = graph.next_available()

    assert available[0].task == "Code"