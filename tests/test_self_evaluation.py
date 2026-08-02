from aura.brain.evaluator import Evaluator
from aura.brain.learning_profile import LearningProfile
from aura.brain.observation import Observation
from aura.brain.performance import PerformanceReport
from aura.brain.self_evaluation_engine import SelfEvaluationEngine


def test_evaluator_returns_quality_metrics():

    evaluator = Evaluator()

    observation = Observation(
        source="calculator",
        output="10",
        success=True,
    )

    result = evaluator.evaluate(
        observation,
    )

    quality = evaluator.evaluate_quality(
        result,
    )

    assert quality["success"]

    assert quality["quality_level"] == "high"


def test_self_evaluation_detects_skill_strength():

    profile = LearningProfile()

    profile.update_skill(
        "calculation",
        0.95,
    )

    profile.update_skill(
        "coding",
        0.3,
    )

    report = PerformanceReport(
        success_rate=1.0,
        average_score=1.0,
        retry_rate=0.0,
        performance_score=1.0,
    )

    result = SelfEvaluationEngine().evaluate(
        profile,
        report,
    )

    assert result.strongest_skill == "calculation"

    assert result.weakest_skill == "coding"
