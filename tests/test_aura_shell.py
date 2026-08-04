from aura.ui.aura_shell import AuraShell


class FakeAgent:

    def execute(
        self,
        message,
    ):
        class State:
            output = f"received: {message}"
            metadata = {}

        return State()


def test_aura_shell_agent_execution():

    shell = AuraShell(
        FakeAgent(),
    )

    state = shell._agent.execute(
        "hello",
    )

    assert state.output == "received: hello"
