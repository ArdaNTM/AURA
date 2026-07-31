from aura.brain.models import Decision
from aura.brain.observation import Observation
from aura.brain.state import AgentState


def test_agent_state_stores_observation():
    state = AgentState(
        goal="2+2 hesapla",
    )

    state.decision = Decision(
        intent="calculation",
    )

    observation = Observation(
        source="calculator",
        output="4",
    )

    state.add_observation(
        observation,
    )

    assert len(state.observations) == 1

    assert state.observations[0].output == "4"
