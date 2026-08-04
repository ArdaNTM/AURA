from aura.agent.autonomous_task import AutonomousTask
from aura.agent.background_worker import BackgroundWorker
from aura.agent.scheduler import Scheduler


class FakeAgentLoop:
    def __init__(self):
        self.messages = []

    def run(
        self,
        message: str,
    ):
        self.messages.append(
            message,
        )

        return "done"


class FailingAgentLoop:
    def run(
        self,
        message: str,
    ):
        raise RuntimeError("boom")


def test_background_worker_executes_pending_tasks():

    scheduler = Scheduler()

    task = AutonomousTask(
        "check system",
        60,
    )

    scheduler.add(
        task,
    )

    agent = FakeAgentLoop()

    worker = BackgroundWorker(
        scheduler,
        agent,
    )

    count = worker.run_pending()

    assert count == 1

    assert agent.messages == [
        "check system",
    ]

    assert task.run_count == 1


def test_background_worker_handles_failure():

    scheduler = Scheduler()

    task = AutonomousTask(
        "fail task",
        60,
    )

    scheduler.add(
        task,
    )

    worker = BackgroundWorker(
        scheduler,
        FailingAgentLoop(),
    )

    count = worker.run_pending()

    assert count == 1

    assert task.status == "pending"

    assert task.retry_count == 1


def test_background_worker_retries_failed_tasks():

    scheduler = Scheduler()

    task = AutonomousTask(
        "retry task",
        60,
        max_retries=2,
    )

    scheduler.add(
        task,
    )

    worker = BackgroundWorker(
        scheduler,
        FailingAgentLoop(),
    )

    count = worker.run_pending()

    assert count == 1

    assert task.status == "pending"

    assert task.retry_count == 1


def test_background_worker_marks_failed_after_retry_limit():

    scheduler = Scheduler()

    task = AutonomousTask(
        "fail forever",
        60,
        max_retries=0,
    )

    scheduler.add(
        task,
    )

    worker = BackgroundWorker(
        scheduler,
        FailingAgentLoop(),
    )

    count = worker.run_pending()

    assert count == 1

    assert task.status == "failed"
