from aura.agent.autonomous_task import AutonomousTask
from aura.agent.scheduler import Scheduler
from aura.agent.task_store import TaskStore


def test_scheduler_adds_tasks():

    scheduler = Scheduler()

    task = AutonomousTask(
        "system check",
        60,
    )

    scheduler.add(
        task,
    )

    assert (
        len(
            scheduler.tasks,
        )
        == 1
    )


def test_scheduler_returns_pending_tasks():

    scheduler = Scheduler()

    task = AutonomousTask(
        "system check",
        60,
    )

    scheduler.add(
        task,
    )

    pending = scheduler.pending()

    assert task in pending


def test_scheduler_removes_task():

    scheduler = Scheduler()

    task = AutonomousTask(
        "system check",
        60,
    )

    scheduler.add(
        task,
    )

    assert scheduler.remove(
        task.task_id,
    )

    assert (
        len(
            scheduler.tasks,
        )
        == 0
    )


def test_scheduler_restores_tasks_from_store(tmp_path):

    store = TaskStore(
        str(tmp_path / "tasks.db"),
    )

    task = AutonomousTask(
        "persistent check",
        60,
    )

    store.save(task)

    scheduler = Scheduler(
        store,
    )

    assert len(scheduler.tasks) == 1

    assert scheduler.tasks[0].description == "persistent check"
