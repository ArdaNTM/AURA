from aura.ai.llm_provider import LLMProvider
from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.llm_reasoner import LLMReasoner
from aura.brain.llm_validator import LLMValidator
from aura.brain.permission import PermissionManager
from aura.brain.permission_gate import PermissionGate
from aura.brain.planner import Planner
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry


class ComputerLLMProvider(LLMProvider):
    """Return computer capability reasoning."""

    def complete(
        self,
        prompt: str,
    ) -> str:
        return """
        {
            "intent": "computer",
            "capability": "computer",
            "confidence": 0.9,
            "risk_level": "high",
            "entities": {}
        }
        """


def test_llm_reasoning_respects_permission_gate():

    registry = ToolRegistry()

    reasoner = LLMReasoner(
        ComputerLLMProvider(),
    )

    planner = Planner(
        tools=registry,
        llm_reasoner=reasoner,
        llm_validator=LLMValidator(
            Planner().capabilities,
        ),
    )

    runtime = AgentRuntime(
        Brain(
            planner=planner,
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        permission_gate=PermissionGate(
            PermissionManager(),
        ),
    )

    state = runtime.run(
        "bilgisayarı kontrol et",
    )

    assert state.permission_request is not None

    assert state.permission_request.capability == "computer"

    assert not state.permission_request.approved
