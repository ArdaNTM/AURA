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
