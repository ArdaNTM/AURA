from aura.vision.recovery import VisionRecovery


def test_recovery_finds_similar_element():

    recovery = VisionRecovery()

    result = recovery.recover(
        "save",
        [
            "cancel_button",
            "save_button",
            "open_button",
        ],
    )

    assert result["retry"]

    assert result["new_target"] == "save_button"

    assert result["confidence"] == 0.8


def test_recovery_fails_without_match():

    recovery = VisionRecovery()

    result = recovery.recover(
        "delete",
        [
            "save_button",
            "open_button",
        ],
    )

    assert result["retry"] is False
