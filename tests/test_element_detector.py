from aura.vision.element_detector import ElementDetector


def test_detector_returns_ui_elements():

    detector = ElementDetector()

    result = detector.detect(
        "screen.png",
    )

    assert len(result) == 1

    assert result[0].element_type == "button"

    assert result[0].confidence == 0.5
