from aura.brain.improvement_evaluator import ImprovementEvaluator
from aura.brain.improvement_memory import ImprovementMemory
from aura.brain.performance import PerformanceReport
from aura.brain.self_evaluation import SelfEvaluation


def test_improvement_evaluator_accepts_positive_evolution():

    memory = ImprovementMemory()

    memory.add(
        "safe_tool_execution",
        0.5,
        0.9,
        True,
    )

    performance = PerformanceReport(
        success_rate=1.0,
        average_score=1.0,
        retry_rate=0.0,
        performance_score=1.0,
    )

    evaluation = SelfEvaluation(
        overall_score=1.0,
    )

    result = ImprovementEvaluator().evaluate(
        memory,
        performance,
        evaluation,
    )

    assert result.approved

    assert result.recommended_strategy == ("safe_tool_execution")

    assert result.evolution_score >= 0.5
