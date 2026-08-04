from aura.agent.autonomous_task import AutonomousTask
from aura.agent.task_store import TaskStore


def test_task_store_persists_tasks(tmp_path):

    store = TaskStore(
        str(tmp_path / "tasks.db"),
    )

    task = AutonomousTask(
        description="run backup",
        interval=60,
    )

    store.save(task)

    tasks = store.load_all()

    assert len(tasks) == 1
    assert tasks[0].description == "run backup"


def test_task_store_persists_execution_state(tmp_path):

    store = TaskStore(
        str(tmp_path / "tasks.db"),
    )

    task = AutonomousTask(
        description="health check",
        interval=60,
    )

    task.status = "completed"
    task.result = "system ok"
    task.error = None
    task.run_count = 5

    store.save(task)

    tasks = store.load_all()

    assert tasks[0].status == "completed"
    assert tasks[0].result == "system ok"
    assert tasks[0].run_count == 5


def test_task_store_persists_retry_state(tmp_path):

    store = TaskStore(
        str(tmp_path / "tasks.db"),
    )

    task = AutonomousTask(
        description="retry backup",
        interval=60,
        max_retries=5,
    )

    task.retry_count = 2
    task.schedule_retry(
        delay=120,
    )

    store.save(task)

    tasks = store.load_all()

    loaded = tasks[0]

    assert loaded.retry_count == 3

    assert loaded.max_retries == 5

    assert loaded.next_retry is not None
