from aura.brain.task_graph import TaskGraph
from aura.brain.task_scheduler import TaskScheduler


def test_scheduler_selects_available_task():

    graph = TaskGraph()

    first = graph.add_task(
        "Research",
    )

    second = graph.add_task(
        "Code",
    )

    graph.add_dependency(
        second,
        first,
    )

    scheduler = TaskScheduler(
        graph,
    )

    task = scheduler.next_task()

    assert task is not None

    assert task.task == "Research"


def test_scheduler_unlocks_next_task():

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

    scheduler = TaskScheduler(
        graph,
    )

    scheduler.complete(
        first,
    )

    task = scheduler.next_task()

    assert task is not None

    assert task.task == "Code"
