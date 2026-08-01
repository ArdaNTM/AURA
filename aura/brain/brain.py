"""AURA cognitive brain facade."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aura.brain.decision import Action, DecisionEngine
from aura.brain.decision_context import DecisionContext
from aura.brain.goal import Goal
from aura.brain.learning import LearningContext
from aura.brain.meta_learner import MetaLearner
from aura.brain.models import Decision
from aura.brain.planner import Planner

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
        meta_learner: MetaLearner | None = None,
    ) -> None:
        self._tools = tools
        self._memory = memory
        self._learning_context = learning_context
        self._meta_learner = meta_learner or MetaLearner()

        self._planner = planner or Planner(
            tools=tools,
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
    def learning_context(self) -> LearningContext | None:
        return self._learning_context

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
    ) -> tuple[Decision, Action]:
        """Analyze a request and select an action."""

        goal = self.create_goal(
            user_message,
        )

        learning = None

        if self._learning_context:
            learning = self._learning_context.summarize()

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

        if memories:
            if learning is None:
                learning = {}

            ranked_memories = self._rank_memories(
                memories,
            )

            learning["retrieved_memories"] = ranked_memories

            successful_strategies = [
                content
                for _, content in ranked_memories
                if "success=True" in content and "strategy=" in content
            ]

            learning["successful_strategies"] = successful_strategies

            strategy_scores = self._strategy_scores(
                successful_strategies,
            )

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

    def _rank_memories(
        self,
        memories: list[tuple[str, str]],
    ) -> list[tuple[str, str]]:
        """Rank memories by experience quality."""

        return sorted(
            memories,
            key=self._memory_score,
            reverse=True,
        )

    def _memory_score(
        self,
        memory: tuple[str, str],
    ) -> float:
        """Calculate memory value."""

        _, content = memory

        score = 0.0

        if "success=True" in content:
            score += 1.0

        if "confidence=" in content:
            try:
                score += float(
                    content.split(
                        "confidence=",
                    )[1].split(
                        ";",
                    )[0],
                )
            except (
                ValueError,
                IndexError,
            ):
                pass

        return score

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
            metadata={
                "goal_description": goal.description,
            },
        )
