"""AURA agent runtime orchestration."""

from __future__ import annotations

from aura.brain.background_task import BackgroundTask
from aura.brain.brain import Brain
from aura.brain.decision_validator import DecisionValidator
from aura.brain.evaluator import Evaluator
from aura.brain.execution_guard import ExecutionGuard
from aura.brain.execution_plan import ExecutionPlan
from aura.brain.executor import PlanExecutor
from aura.brain.goal import Goal
from aura.brain.goal_manager import GoalManager
from aura.brain.improvement import ImprovementPlan
from aura.brain.improvement_evaluator import ImprovementEvaluator
from aura.brain.initiative_engine import InitiativeEngine
from aura.brain.learning_profile import LearningProfile
from aura.brain.learning_profile_store import LearningProfileStore
from aura.brain.memory_policy import MemoryPolicy
from aura.brain.models import Decision
from aura.brain.performance_engine import PerformanceEngine
from aura.brain.permission_gate import PermissionGate
from aura.brain.permission_request import PermissionRequest
from aura.brain.permission_service import PermissionService
from aura.brain.reflection_engine import ReflectionEngine
from aura.brain.self_evaluation_engine import SelfEvaluationEngine
from aura.brain.state import AgentState
from aura.brain.task_decomposer import TaskDecomposer
from aura.brain.task_graph import TaskGraph
from aura.brain.task_memory import TaskMemory
from aura.brain.task_scheduler import TaskScheduler
from aura.brain.vision_controller import VisionController
from aura.memory.base import Memory
from aura.memory.consolidation import MemoryConsolidator
from aura.memory.optimization import MemoryOptimizer
from aura.vision.memory import VisionMemory


class AgentRuntime:
    """Coordinate brain decisions and execution state."""

    def __init__(
        self,
        brain: Brain,
        executor: PlanExecutor,
        memory: Memory | None = None,
        memory_policy: MemoryPolicy | None = None,
        task_memory: TaskMemory | None = None,
        evaluator: Evaluator | None = None,
        reflection_engine: ReflectionEngine | None = None,
        performance_engine: PerformanceEngine | None = None,
        permission_service: PermissionService | None = None,
        self_evaluation_engine: SelfEvaluationEngine | None = None,
        learning_profile: LearningProfile | None = None,
        learning_profile_store: LearningProfileStore | None = None,
        permission_gate: PermissionGate | None = None,
        decision_validator: DecisionValidator | None = None,
        execution_guard: ExecutionGuard | None = None,
        memory_consolidator: MemoryConsolidator | None = None,
        memory_optimizer: MemoryOptimizer | None = None,
        improvement_evaluator: ImprovementEvaluator | None = None,
        goal_manager: GoalManager | None = None,
        task_decomposer: TaskDecomposer | None = None,
        vision_controller: VisionController | None = None,
        vision_memory: VisionMemory | None = None,
    ) -> None:
        self._brain = brain
        self._executor = executor
        self._memory = memory
        self._memory_policy = memory_policy or MemoryPolicy()
        self._memory_consolidator = memory_consolidator or MemoryConsolidator()
        self._memory_optimizer = memory_optimizer or MemoryOptimizer()
        self._task_memory = task_memory
        self._task_decomposer = task_decomposer or TaskDecomposer()

        if self._task_memory is None and memory:
            self._task_memory = TaskMemory(
                memory,
            )
        self._evaluator = evaluator or Evaluator()
        self._reflection_engine = reflection_engine or ReflectionEngine()
        self._performance_engine = performance_engine or PerformanceEngine()
        self._permission_service = permission_service or PermissionService()
        self._self_evaluation_engine = self_evaluation_engine or SelfEvaluationEngine()
        self._learning_profile_store = learning_profile_store or LearningProfileStore()
        self._permission_gate = permission_gate or PermissionGate()
        self._decision_validator = decision_validator or DecisionValidator(
            brain.planner.capabilities,
        )
        self._execution_guard = execution_guard or ExecutionGuard(
            brain.tools,
        )
        self._improvement_evaluator = improvement_evaluator or ImprovementEvaluator()
        if learning_profile is None:
            self._learning_profile = self._learning_profile_store.load()
        else:
            self._learning_profile = learning_profile
        self._goal_manager = goal_manager or GoalManager()
        self._initiative_engine = InitiativeEngine()
        self._vision_controller = vision_controller or VisionController()
        self._vision_memory = vision_memory

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
    def memory_optimizer(
        self,
    ) -> MemoryOptimizer:
        """Return memory optimizer."""

        return self._memory_optimizer

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
    def permission_service(
        self,
    ) -> PermissionService:
        """Return permission service."""

        return self._permission_service

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

    @property
    def improvement_evaluator(
        self,
    ) -> ImprovementEvaluator:
        """Return improvement evaluator."""

        return self._improvement_evaluator

    @property
    def goal_manager(
        self,
    ) -> GoalManager:
        """Return goal manager."""

        return self._goal_manager

    @property
    def initiative_engine(
        self,
    ) -> InitiativeEngine:
        """Return initiative engine."""

        return self._initiative_engine

    @property
    def vision_controller(
        self,
    ) -> VisionController:
        """Return vision controller."""

        return self._vision_controller

    @property
    def vision_memory(
        self,
    ) -> VisionMemory | None:
        """Return vision memory."""

        return self._vision_memory

    @property
    def task_decomposer(
        self,
    ) -> TaskDecomposer:
        return self._task_decomposer

    def run(
        self,
        user_message: str,
        agent_context: dict[str, object] | None = None,
    ) -> AgentState:
        """Run one agent cycle."""

        goal = self._goal_manager.create_goal(
            user_message,
        )

        task = BackgroundTask(
            description=user_message,
        )

        task.start()

        state = AgentState(
            goal=goal,
            background_task=task,
        )

        memories = []
        vision_memories = []

        if self._vision_memory:
            vision_memories = self._vision_memory.recall(
                user_message,
            )

            memories.extend(
                vision_memories,
            )
        vision = None

        try:
            vision_result = self._vision_controller.observe()

            vision = {
                "description": vision_result.description,
                "objects": vision_result.objects,
                "confidence": vision_result.confidence,
                "text": vision_result.text,
                "regions": vision_result.regions,
                "elements": [
                    {
                        "name": element.name,
                        "type": element.type,
                        "confidence": element.confidence,
                        "coordinates": {
                            "x": element.x,
                            "y": element.y,
                        },
                    }
                    for element in vision_result.elements
                ],
                "metadata": vision_result.metadata,
            }

        except Exception as error:
            vision = {
                "error": str(error),
                "confidence": 0.0,
            }

        state.metadata["memory_count"] = len(
            memories,
        )
        state.metadata["vision"] = vision

        if self._vision_memory and vision_result:
            self._vision_memory.store(
                vision_result,
                context=user_message,
            )

            state.metadata["vision_memory"] = True

        decision, action = self._brain.think(
            user_message,
            memories=memories,
            agent_context=agent_context,
            vision=vision,
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

            permission_request = PermissionRequest(
                capability=str(capability),
                reason=decision.explanation or "Permission required",
                risk_level=decision.risk_level,
            )

            self._permission_service.create(
                permission_request,
                decision,
            )

            state.set_permission_request(
                permission_request,
            )

            state.metadata["permission_required"] = True

            state.completed = True

            return state

        if state.execution_plan:
            while not state.execution_plan.completed:
                state.execution_plan.advance()

        validation = self._decision_validator.validate(
            decision,
        )

        if not validation.valid:
            state.metadata["decision_validation"] = {
                "valid": False,
                "reason": validation.reason,
            }

            if state.background_task:
                state.background_task.fail(
                    "Decision validation failed",
                )

                state.metadata["task"] = {
                    "task_id": state.background_task.task_id,
                    "status": state.background_task.status,
                    "progress": state.background_task.progress,
                }

            state.completed = True

            return state

        if not self._execution_guard.can_execute(
            decision,
        ):
            state.completed = True

            state.metadata["execution_blocked"] = True

            return state

        if state.background_task:
            state.background_task.update_progress(
                0.5,
                step="Executing plan",
            )

        evaluated_observations = self._execute_decision(
            decision,
            state,
        )

        report = self._performance_engine.evaluate(
            evaluated_observations,
        )

        if decision.strategy:

            previous_score = self._learning_profile.skill_scores.get(
                decision.intent,
                0.0,
            )

            allowed = self._learning_profile.validate_improvement(
                "strategy",
                f"Improve strategy {decision.strategy}",
            )

            if allowed:

                self._learning_profile.register_improvement(
                    strategy=decision.strategy,
                    before_score=previous_score,
                    after_score=report.performance_score,
                    success=report.performance_score >= previous_score,
                    notes=("Autonomous improvement feedback"),
                )

        self_evaluation = self._self_evaluation_engine.evaluate(
            self._learning_profile,
            report,
        )

        state.metadata["self_evaluation"] = {
            "overall_score": self_evaluation.overall_score,
            "strongest_skill": self_evaluation.strongest_skill,
            "weakest_skill": self_evaluation.weakest_skill,
            "best_strategy": self_evaluation.best_strategy,
            "recommendations": self_evaluation.recommendations,
        }
        self._learning_profile.self_evaluation = {
            "overall_score": self_evaluation.overall_score,
            "strongest_skill": self_evaluation.strongest_skill,
            "weakest_skill": self_evaluation.weakest_skill,
            "best_strategy": self_evaluation.best_strategy,
            "recommendations": self_evaluation.recommendations,
        }
        initiative = self._initiative_engine.create(
            self_evaluation,
        )

        if initiative:

            state.metadata["initiative"] = {
                "reason": initiative.reason,
                "task": initiative.task,
                "priority": initiative.priority,
                "strategy": initiative.strategy,
            }
        self._learning_profile_store.save(
            self._learning_profile,
        )

        state.metadata["goal"] = {
            "description": state.goal.description,
        }

        if decision:

            execution_plan = self._task_decomposer.decompose(
                goal,
            )

            state.set_execution_plan(
                execution_plan,
            )

            graph = TaskGraph()

            previous_task_id = None

            for step in execution_plan.steps:
                task_id = graph.add_task(
                    step.description,
                )

                if previous_task_id:
                    graph.add_dependency(
                        task_id,
                        previous_task_id,
                    )

                previous_task_id = task_id

            scheduler = TaskScheduler(
                graph,
            )

            state.task_graph = graph
            state.task_scheduler = scheduler

            scheduler = self._build_scheduler(
                execution_plan,
            )

            state.set_scheduler(
                scheduler,
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
            state.metadata["task_graph"] = {
                "tasks": len(graph.nodes),
                "available": len(graph.next_available()),
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
            "confidence_accuracy": self._learning_profile.confidence_accuracy,
            "confidence_error": self._learning_profile.confidence_error,
            "average_quality": self._learning_profile.average_quality,
            "strategy_usage": self._learning_profile.strategy_usage,
            "strategy_success": self._learning_profile.strategy_success,
            "skill_scores": self._learning_profile.skill_scores,
        }

        state.metadata["observation_count"] = len(
            evaluated_observations,
        )

        if state.goal:
            self._goal_manager.complete_goal(
                state.goal.goal_id,
            )

        if state.background_task:
            state.background_task.complete()

            state.metadata["task"] = {
                "task_id": state.background_task.task_id,
                "status": state.background_task.status,
                "progress": state.background_task.progress,
            }

        state.completed = True

        return state

    def resume(
        self,
    ) -> AgentState:
        """Resume execution after permission approval."""

        request = self._permission_service.pending
        decision = self._permission_service.decision

        if request is None:
            raise RuntimeError(
                "No pending permission request.",
            )

        if not request.approved:
            raise PermissionError(
                "Permission request is not approved.",
            )

        if decision is None:
            raise RuntimeError(
                "No stored decision.",
            )

        self._permission_service.clear()

        state = AgentState(
            goal=Goal(
                description=f"Approved permission: {request.capability}",
            ),
        )

        state.decision = decision

        self._execute_decision(
            decision,
            state,
        )

        state.completed = True

        return state

    def _execute_decision(
        self,
        decision: Decision,
        state: AgentState,
    ) -> list:
        """Execute decision pipeline."""

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

            decision.outcome = {
                "success": reflection.success,
                "strategy": decision.strategy,
                "confidence": decision.confidence,
                "intent": decision.intent,
                "output": evaluated.output,
            }

            state.add_observation(
                evaluated,
            )

            state.set_reflection(
                reflection,
            )

            evaluated_observations.append(
                evaluated,
            )

            self._learning_profile.register_task(
                success=reflection.success,
                strategy=decision.strategy,
            )

            self._learning_profile.register_confidence(
                confidence=decision.confidence,
                success=reflection.success,
            )

            self._learning_profile.register_skill_reflection(
                decision.intent,
                evaluated.score,
                reflection,
            )
            tool_snapshot = self._executor.tool_runner.reliability_tracker.snapshot()

            for name, stats in tool_snapshot.items():
                self._learning_profile.register_tool_reliability(
                    name,
                    stats["success_rate"],
                    stats["average_duration"],
                    int(stats["runs"]),
                )
            self._learning_profile_store.save(
                self._learning_profile,
            )

            self._store_observation(
                evaluated,
                reflection,
                decision,
            )
            if self._task_memory and self._memory_policy.should_store(
                evaluated,
            ):
                if reflection.success:
                    self._task_memory.store_success(
                        decision.intent,
                        evaluated.output,
                    )

                else:
                    self._task_memory.store_failure(
                        decision.intent,
                        reflection.summary,
                    )

        return evaluated_observations

    def _build_scheduler(
        self,
        execution_plan: ExecutionPlan,
    ) -> TaskScheduler:
        """Create dependency graph from execution plan."""

        graph = TaskGraph()

        previous = None

        for step in execution_plan.steps:

            task_id = graph.add_task(
                step.description,
            )

            if previous:
                graph.add_dependency(
                    task_id,
                    previous,
                )

            previous = task_id

        return TaskScheduler(
            graph,
        )

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

        self._memory_consolidator.consolidate(
            self._memory,
        )

        expired = self._memory_optimizer.find_expired(
            self._memory,
        )

        if expired:
            self._remove_expired_memories(
                expired,
            )

        self._memory_optimizer.compress(
            self._memory,
        )

    def _remove_expired_memories(
        self,
        memories: list[tuple[str, str]],
    ) -> None:
        """Remove expired low value memories."""

        if not self._memory:
            return

        remaining = [item for item in self._memory.history() if item not in memories]

        self._memory.clear()

        for role, content in remaining:
            self._memory.add(
                role,
                content,
            )

    def _create_task_scheduler(
        self,
        execution_plan: ExecutionPlan,
    ) -> TaskScheduler:

        graph = TaskGraph()

        previous = None

        for step in execution_plan.steps:

            task_id = graph.add_task(
                step.description,
            )

            if previous:
                graph.add_dependency(
                    task_id,
                    previous,
                )

            previous = task_id

        return TaskScheduler(
            graph,
        )
