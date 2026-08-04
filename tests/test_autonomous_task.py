from datetime import datetime, timedelta

from aura.agent.autonomous_task import AutonomousTask


def test_autonomous_task_runs_first_time():

    task = AutonomousTask(
        "check system",
        60,
    )

    assert task.should_run()


def test_autonomous_task_waits_for_interval():

    task = AutonomousTask(
        "check system",
        60,
    )

    task.mark_completed(
        datetime.now(),
    )

    assert not task.should_run(datetime.now() + timedelta(seconds=30))


def test_autonomous_task_runs_after_interval():

    task = AutonomousTask(
        "check system",
        60,
    )

    task.mark_completed(
        datetime.now(),
    )

    assert task.should_run(datetime.now() + timedelta(seconds=61))
