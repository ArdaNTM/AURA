from aura.brain.capability import CapabilityRegistry
from aura.brain.llm_validator import LLMValidator
from aura.brain.reasoning import ReasoningResult


def create_validator() -> LLMValidator:
    return LLMValidator(
        CapabilityRegistry(),
    )


def test_llm_validator_accepts_valid_reasoning():
    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
            capability="calculation",
            confidence=0.9,
            risk_level="low",
        )
    )

    assert result.valid


def test_llm_validator_rejects_unknown_intent():
    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="unknown_action",
            confidence=0.9,
        )
    )

    assert not result.valid

    assert "Unknown intent" in result.reason


def test_llm_validator_rejects_intent_capability_conflict():
    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
            capability="filesystem",
            confidence=0.9,
        )
    )

    assert not result.valid

    assert "mismatch" in result.reason


def test_llm_validator_rejects_capability_mismatch():
    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
            capability="filesystem",
            confidence=0.9,
        )
    )

    assert not result.valid

    assert "mismatch" in result.reason


def test_llm_validator_rejects_invalid_confidence():
    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
            confidence=1.5,
        )
    )

    assert not result.valid


def test_llm_validator_rejects_invalid_risk_level():
    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
            risk_level="critical",
        )
    )

    assert not result.valid


def test_llm_validator_rejects_unknown_capability():

    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
            capability="unknown_capability",
            confidence=0.9,
        )
    )

    assert not result.valid

    assert "Unknown capability" in result.reason


def test_llm_validator_accepts_matching_capability():

    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
            capability="calculation",
            confidence=0.9,
        )
    )

    assert result.valid


def test_llm_validator_rejects_missing_intent():

    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="",
            confidence=0.9,
        )
    )

    assert not result.valid


def test_llm_validator_handles_missing_confidence():

    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
        )
    )

    assert result.valid


def test_llm_validator_rejects_unknown_risk_level():

    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
            risk_level="critical",
        )
    )

    assert not result.valid

    assert "Invalid risk" in result.reason


def test_llm_validator_rejects_invalid_entities():

    validator = create_validator()

    reasoning = ReasoningResult(
        intent="calculation",
        confidence=0.9,
    )

    reasoning.entities = "invalid"

    result = validator.validate(
        reasoning,
    )

    assert not result.valid


def test_llm_validator_keeps_valid_calculation():

    validator = create_validator()

    result = validator.validate(
        ReasoningResult(
            intent="calculation",
            capability="calculation",
            confidence=0.95,
            risk_level="low",
            entities={
                "expression": "5+5",
            },
        )
    )

    assert result.valid
