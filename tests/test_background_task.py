from aura.brain.background_task import BackgroundTask
from aura.brain.task_store import TaskStore


def test_background_task_lifecycle():

    task = BackgroundTask(
        "Research AI papers",
    )

    assert task.status == "pending"

    task.start()

    assert task.status == "running"

    task.update_progress(
        0.5,
        "Collect sources",
    )

    assert task.progress == 0.5

    task.complete()

    assert task.status == "completed"

    assert task.progress == 1.0


def test_task_store_persistence(tmp_path):

    store = TaskStore(
        str(tmp_path / "tasks.db"),
    )

    task = BackgroundTask(
        "Build game",
    )

    store.save(
        task,
    )

    loaded = store.get(
        task.task_id,
    )

    assert loaded is not None

    assert loaded.description == "Build game"
