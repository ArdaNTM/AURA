"""AURA agent runtime orchestration."""

from __future__ import annotations

from aura.brain.brain import Brain
from aura.brain.evaluator import Evaluator
from aura.brain.execution_plan import ExecutionPlan
from aura.brain.executor import PlanExecutor
from aura.brain.goal import Goal
from aura.brain.improvement import ImprovementPlan
from aura.brain.learning_profile import LearningProfile
from aura.brain.learning_profile_store import LearningProfileStore
from aura.brain.memory_policy import MemoryPolicy
from aura.brain.performance_engine import PerformanceEngine
from aura.brain.permission_gate import PermissionGate
from aura.brain.permission_request import PermissionRequest
from aura.brain.reflection_engine import ReflectionEngine
from aura.brain.state import AgentState
from aura.memory.base import Memory


class AgentRuntime:
    """Coordinate brain decisions and execution state."""

    def __init__(
        self,
        brain: Brain,
        executor: PlanExecutor,
        memory: Memory | None = None,
        memory_policy: MemoryPolicy | None = None,
        evaluator: Evaluator | None = None,
        reflection_engine: ReflectionEngine | None = None,
        performance_engine: PerformanceEngine | None = None,
        learning_profile: LearningProfile | None = None,
        learning_profile_store: LearningProfileStore | None = None,
        permission_gate: PermissionGate | None = None,
    ) -> None:
        self._brain = brain
        self._executor = executor
        self._memory = memory
        self._memory_policy = memory_policy or MemoryPolicy()
        self._evaluator = evaluator or Evaluator()
        self._reflection_engine = reflection_engine or ReflectionEngine()
        self._performance_engine = performance_engine or PerformanceEngine()
        self._learning_profile_store = learning_profile_store or LearningProfileStore()
        self._permission_gate = permission_gate or PermissionGate()

        if learning_profile is None:
            self._learning_profile = self._learning_profile_store.load()
        else:
            self._learning_profile = learning_profile

    @property
    def brain(
        self,
    ) -> Brain:
        """Return brain instance."""

        return self._brain

    @property
    def executor(
        self,
    ) -> PlanExecutor:
        """Return executor instance."""

        return self._executor

    @property
    def memory(
        self,
    ) -> Memory | None:
        """Return memory instance."""

        return self._memory

    @property
    def memory_policy(
        self,
    ) -> MemoryPolicy:
        """Return memory policy."""

        return self._memory_policy

    @property
    def evaluator(
        self,
    ) -> Evaluator:
        """Return evaluator."""

        return self._evaluator

    @property
    def reflection_engine(
        self,
    ) -> ReflectionEngine:
        """Return reflection engine."""

        return self._reflection_engine

    @property
    def performance_engine(
        self,
    ) -> PerformanceEngine:
        """Return performance engine."""

        return self._performance_engine

    @property
    def learning_profile(
        self,
    ) -> LearningProfile:
        """Return learning profile."""

        return self._learning_profile

    @property
    def learning_profile_store(
        self,
    ) -> LearningProfileStore:
        """Return learning profile store."""

        return self._learning_profile_store

    def run(
        self,
        user_message: str,
    ) -> AgentState:
        """Run one agent cycle."""

        goal = Goal(
            description=user_message,
        )

        state = AgentState(
            goal=goal,
        )

        memories = []

        if self._memory:
            memories = self._memory.search(
                user_message,
            )

        state.metadata["memory_count"] = len(
            memories,
        )

        decision, action = self._brain.think(
            user_message,
            memories=memories,
        )

        state.decision = decision
        state.action = action

        if (
            decision
            and decision.requires_permission
            and not self._permission_gate.can_execute(
                decision,
            )
        ):
            capability = decision.metadata.get(
                "capability",
                "unknown",
            )

            state.set_permission_request(
                PermissionRequest(
                    capability=str(capability),
                    reason=decision.explanation or "Permission required",
                    risk_level=decision.risk_level,
                ),
            )

            state.metadata["permission_required"] = True

            state.completed = True

            return state

        if state.execution_plan:
            while not state.execution_plan.completed:
                state.execution_plan.advance()

        observations = self._executor.execute_with_observation(
            decision,
        )

        evaluated_observations = []

        for observation in observations:
            evaluated = self._evaluator.evaluate(
                observation,
            )

            reflection = self._reflection_engine.reflect(
                evaluated,
                decision=state.decision,
            )

            state.add_observation(
                evaluated,
            )

            state.set_reflection(
                reflection,
            )

            evaluated_observations.append(
                evaluated,
            )

            if decision:
                self._learning_profile.register_task(
                    success=reflection.success,
                    strategy=decision.strategy,
                )

                self._learning_profile_store.save(
                    self._learning_profile,
                )

            self._store_observation(
                evaluated,
                reflection,
                decision,
            )

        report = self._performance_engine.evaluate(
            evaluated_observations,
        )

        state.metadata["goal"] = {
            "description": state.goal.description,
        }

        if decision:
            execution_plan = ExecutionPlan(
                goal=goal.description,
                steps=decision.plan,
            )

            state.set_execution_plan(
                execution_plan,
            )

            state.metadata["intent"] = decision.intent
            state.metadata["confidence"] = decision.confidence

            state.metadata["execution_plan"] = {
                "total_steps": len(
                    execution_plan.steps,
                ),
                "completed_steps": execution_plan.completed_steps,
                "is_complete": execution_plan.is_complete(),
            }

            self._apply_improvement_plan(
                state,
                decision,
            )

        state.metadata["performance"] = {
            "success_rate": report.success_rate,
            "average_score": report.average_score,
            "retry_rate": report.retry_rate,
            "performance_score": report.performance_score,
        }

        state.metadata["learning_profile"] = {
            "total_tasks": self._learning_profile.total_tasks,
            "successful_tasks": self._learning_profile.successful_tasks,
            "failed_tasks": self._learning_profile.failed_tasks,
            "success_rate": self._learning_profile.success_rate,
        }

        state.metadata["observation_count"] = len(
            observations,
        )

        state.completed = True

        return state

    def _apply_improvement_plan(
        self,
        state: AgentState,
        decision,
    ) -> None:
        """Apply improvement recommendation from learning."""

        learning = decision.metadata.get(
            "learning",
        )

        if not isinstance(
            learning,
            dict,
        ):
            return

        improvement_data = learning.get(
            "improvement_plan",
        )

        if not isinstance(
            improvement_data,
            dict,
        ):
            return

        state.set_improvement_plan(
            ImprovementPlan(
                suggestions=improvement_data.get(
                    "suggestions",
                    [],
                ),
                target_strategy=improvement_data.get(
                    "target_strategy",
                ),
                confidence_change=improvement_data.get(
                    "confidence_change",
                    0.0,
                ),
                risk_adjustment=improvement_data.get(
                    "risk_adjustment",
                ),
            ),
        )

    def _store_observation(
        self,
        observation,
        reflection,
        decision,
    ) -> None:
        """Store approved observations in memory."""

        if not self._memory:
            return

        if not self._memory_policy.should_store(
            observation,
        ):
            return

        content = (
            f"intent={decision.intent}; "
            f"strategy={decision.strategy}; "
            f"confidence={decision.confidence}; "
            f"success={reflection.success}; "
            f"output={observation.output}"
        )

        self._memory.add(
            "assistant",
            content,
        )
