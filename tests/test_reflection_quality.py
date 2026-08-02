from aura.brain.reflection import Reflection


def test_reflection_has_quality_feedback():

    reflection = Reflection(
        success=True,
        summary="ok",
        quality_score=1.0,
        quality_level="high",
    )

    assert reflection.quality_score == 1.0

    assert reflection.quality_level == "high"
