from aura.brain.task_graph import TaskGraph
from aura.brain.task_progress import TaskProgressTracker


def test_task_progress_summary():

    graph = TaskGraph()

    design = graph.add_task(
        "Design",
    )

    code = graph.add_task(
        "Code",
    )

    graph.add_dependency(
        code,
        design,
    )

    tracker = TaskProgressTracker(
        graph,
    )

    summary = tracker.summary()

    assert summary["total"] == 2

    assert summary["completed"] == 0

    assert summary["percentage"] == 0.0

    assert summary["current"] == "Design"


def test_progress_after_completion():

    graph = TaskGraph()

    task = graph.add_task(
        "Build",
    )

    tracker = TaskProgressTracker(
        graph,
    )

    graph.complete(
        task,
    )

    assert tracker.completed_tasks() == 1

    assert tracker.percentage() == 1.0
