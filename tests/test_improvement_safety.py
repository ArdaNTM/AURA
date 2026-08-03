from aura.brain.improvement_validator import (
    ImprovementValidator,
)


def test_safe_improvement_is_allowed():

    validator = ImprovementValidator()

    result = validator.validate(
        "strategy",
        "Change execution strategy",
    )

    assert result is True


def test_security_change_is_blocked():

    validator = ImprovementValidator()

    result = validator.validate(
        "security",
        "Disable permission system",
    )

    assert result is False
