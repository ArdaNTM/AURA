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
