"""AURA cognitive brain facade."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aura.brain.decision import Action, DecisionEngine
from aura.brain.decision_context import DecisionContext
from aura.brain.goal import Goal
from aura.brain.learning import LearningContext
from aura.brain.learning_profile import LearningProfile
from aura.brain.meta_learner import MetaLearner
from aura.brain.models import Decision
from aura.brain.planner import Planner
from aura.brain.self_evaluation_engine import SelfEvaluationEngine
from aura.brain.user_profile import UserProfile
from aura.memory.recall import RecallEngine

if TYPE_CHECKING:
    from aura.core.tools import ToolRegistry
    from aura.memory.base import Memory


class Brain:
    """High level interface for AURA reasoning."""

    def __init__(
        self,
        planner: Planner | None = None,
        decision_engine: DecisionEngine | None = None,
        tools: ToolRegistry | None = None,
        memory: Memory | None = None,
        learning_context: LearningContext | None = None,
        learning_profile: LearningProfile | None = None,
        meta_learner: MetaLearner | None = None,
        self_evaluator: SelfEvaluationEngine | None = None,
        user_profile: UserProfile | None = None,
    ) -> None:
        self._tools = tools
        self._memory = memory
        self._recall_engine = RecallEngine(memory) if memory else None
        self._learning_context = learning_context
        self._learning_profile = learning_profile
        self._user_profile = user_profile
        self._meta_learner = meta_learner or MetaLearner()
        self._self_evaluator = self_evaluator or SelfEvaluationEngine()
        self._planner = planner or Planner(
            tools=tools,
            learning_profile=learning_profile,
        )
        self._decision_engine = decision_engine or DecisionEngine()

    @property
    def planner(self) -> Planner:
        return self._planner

    @property
    def decision_engine(self) -> DecisionEngine:
        return self._decision_engine

    @property
    def tools(self) -> ToolRegistry | None:
        return self._tools

    @property
    def memory(self) -> Memory | None:
        return self._memory

    @property
    def recall_engine(
        self,
    ) -> RecallEngine | None:
        """Return memory recall engine."""
        return self._recall_engine

    @property
    def learning_context(self) -> LearningContext | None:
        return self._learning_context

    @property
    def learning_profile(self) -> LearningProfile | None:
        return self._learning_profile

    @property
    def user_profile(
        self,
    ) -> UserProfile | None:
        """Return user personalization profile."""

        return self._user_profile

    @property
    def meta_learner(self) -> MetaLearner:
        return self._meta_learner

    def create_goal(
        self,
        user_message: str,
    ) -> Goal:
        """Create an execution goal from user input."""

        return Goal(
            description=user_message,
        )

    def think(
        self,
        user_message: str,
        memories: list[tuple[str, str]] | None = None,
        agent_context: dict[str, object] | None = None,
    ) -> tuple[Decision, Action]:
        """Analyze a request and select an action."""

        goal = self.create_goal(
            user_message,
        )

        learning = {}
        if agent_context:
            learning["agent_experience"] = agent_context
        if self._user_profile:
            learning["user_profile"] = {
                "preferences": self._user_profile.preferences,
                "coding_style": self._user_profile.coding_style,
                "workflow": self._user_profile.workflow,
                "favorite_tools": self._user_profile.favorite_tools,
                "communication_style": self._user_profile.communication_style,
            }
        if self._learning_context:
            learning.update(
                self._learning_context.summarize(),
            )

            improvement_plan = self._meta_learner.analyze(
                self._learning_context,
            )

            learning["meta_recommendation"] = improvement_plan

            learning["improvement_plan"] = {
                "suggestions": improvement_plan.suggestions,
                "target_strategy": improvement_plan.target_strategy,
                "confidence_change": improvement_plan.confidence_change,
                "risk_adjustment": improvement_plan.risk_adjustment,
            }

        if self._learning_profile:
            learning["profile"] = {
                "success_rate": self._learning_profile.success_rate,
                "confidence_accuracy": self._learning_profile.confidence_accuracy,
                "confidence_error": self._learning_profile.confidence_error,
                "average_quality": self._learning_profile.average_quality,
            }
            best_improvement = self._learning_profile.improvement_memory.best_strategy()

            if best_improvement:
                learning["best_improvement_strategy"] = best_improvement

            learning["self_evaluation"] = self._learning_profile.self_evaluation

            learning["skills"] = {
                skill.name: {
                    "confidence": skill.confidence,
                    "success_rate": skill.success_rate,
                    "usage_count": skill.usage_count,
                    "required_tools": skill.required_tools,
                }
                for skill in self._learning_profile.skill_registry.all()
            }

        if memories is None and self._recall_engine:
            memories = self._recall_engine.recall(
                user_message,
            )

        if memories:

            ranked_memories = (
                self._recall_engine.rank(memories) if self._recall_engine else memories
            )

            learning["retrieved_memories"] = ranked_memories

            task_failures = [
                content
                for _, content in ranked_memories
                if ("task_success=False" in content or "success=False" in content)
            ]

            if task_failures:
                learning["has_failures"] = True

            learning["task_failures"] = task_failures

            task_failures = [
                content
                for _, content in ranked_memories
                if ("task_success=False" in content or "success=False" in content)
            ]

            learning["task_failures"] = task_failures

            task_successes = [
                content
                for _, content in ranked_memories
                if ("task_success=True" in content or "success=True" in content)
            ]

            learning["task_successes"] = task_successes

            successful_strategies = [
                content
                for _, content in ranked_memories
                if "success=True" in content and "strategy=" in content
            ]

            learning["successful_strategies"] = successful_strategies

            strategy_scores = self._strategy_scores(
                successful_strategies,
            )

            task_experiences = [
                content
                for _, content in ranked_memories
                if ("task_success=True" in content and "strategy=" in content)
            ]

            learning["task_experiences"] = task_experiences

            if task_experiences:
                learning["best_task_experience"] = task_experiences[0]

            learning["strategy_scores"] = strategy_scores

            if strategy_scores:
                learning["preferred_strategy"] = max(
                    strategy_scores,
                    key=strategy_scores.get,
                )

                learning["strategy_confidence"] = max(
                    strategy_scores.values(),
                ) / sum(
                    strategy_scores.values(),
                )

        context = self.create_context(
            user_message,
            goal,
            learning,
            memories,
        )

        decision = self._planner.decide_with_context(
            context,
        )

        if self._learning_profile:
            strongest_skill = self._learning_profile.skill_registry.strongest()

            if strongest_skill:
                decision.metadata["skill_context"] = {
                    "name": strongest_skill.name,
                    "confidence": strongest_skill.confidence,
                    "success_rate": strongest_skill.success_rate,
                    "usage_count": strongest_skill.usage_count,
                    "required_tools": strongest_skill.required_tools,
                }

        if memories:
            decision.metadata["memory"] = memories

        if learning:
            decision.metadata["learning"] = learning

        decision.metadata["goal"] = {
            "description": goal.description,
            "completed": goal.completed,
            "progress": goal.progress,
            "priority": goal.priority,
        }

        action = self._decision_engine.decide(
            decision,
        )

        return decision, action

    def _strategy_scores(
        self,
        memories: list[str],
    ) -> dict[str, int]:
        """Count successful strategies."""

        scores: dict[str, int] = {}

        for content in memories:
            for part in content.split(";"):
                part = part.strip()

                if part.startswith(
                    "strategy=",
                ):
                    strategy = part.replace(
                        "strategy=",
                        "",
                    )

                    scores[strategy] = (
                        scores.get(
                            strategy,
                            0,
                        )
                        + 1
                    )

        return scores

    def create_context(
        self,
        user_message: str,
        goal: Goal,
        learning: dict[str, object] | None = None,
        memories: list[tuple[str, str]] | None = None,
    ) -> DecisionContext:
        """Create decision context."""

        return DecisionContext(
            user_message=user_message,
            goal=goal,
            learning=learning or {},
            memory=memories or [],
            user_profile=self._user_profile,
            metadata={
                "goal_description": goal.description,
            },
        )
