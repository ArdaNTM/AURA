import json

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
from aura.tools import CalculatorTool


class CalculationLLMProvider(LLMProvider):
    """Return valid calculation reasoning."""

    def complete(
        self,
        prompt: str,
    ) -> str:
        return json.dumps(
            {
                "intent": "calculation",
                "goal": "calculate expression",
                "capability": "calculation",
                "confidence": 0.95,
                "risk_level": "low",
                "entities": {
                    "expression": "5+5",
                },
            }
        )


def create_llm_runtime() -> AgentRuntime:
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    planner = Planner(
        tools=registry,
        llm_reasoner=LLMReasoner(
            CalculationLLMProvider(),
        ),
    )

    return AgentRuntime(
        Brain(
            planner=planner,
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
    )


def test_llm_full_execution_flow():

    runtime = create_llm_runtime()

    state = runtime.run(
        "5+5 hesapla",
    )

    assert state.completed

    assert state.decision is not None

    assert state.decision.intent == "calculation"

    assert state.output == "10"


class InvalidLLMProvider(LLMProvider):
    """Return invalid reasoning."""

    def complete(
        self,
        prompt: str,
    ) -> str:
        return json.dumps(
            {
                "intent": "unknown_action",
                "confidence": 0.9,
                "risk_level": "low",
            }
        )


def test_llm_invalid_reasoning_recovers():

    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    planner = Planner(
        tools=registry,
        llm_reasoner=LLMReasoner(
            InvalidLLMProvider(),
        ),
        llm_validator=LLMValidator(
            Planner(
                tools=registry,
            ).capabilities,
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
    )

    state = runtime.run(
        "5+5 hesapla",
    )

    assert state.completed

    assert state.decision.intent == "calculation"


def test_llm_high_risk_requires_permission():

    class ComputerProvider(LLMProvider):

        def complete(
            self,
            prompt: str,
        ) -> str:
            return json.dumps(
                {
                    "intent": "computer",
                    "goal": "control computer",
                    "capability": "computer",
                    "confidence": 0.95,
                    "risk_level": "high",
                    "entities": {},
                }
            )

    registry = ToolRegistry()

    planner = Planner(
        tools=registry,
        llm_reasoner=LLMReasoner(
            ComputerProvider(),
        ),
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
