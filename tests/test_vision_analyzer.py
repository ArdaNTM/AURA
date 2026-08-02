from aura.vision.analyzer import VisionAnalyzer


def test_vision_analyzer_returns_metadata(
    tmp_path,
):
    image = tmp_path / "test.png"

    image.write_bytes(
        b"fake",
    )

    analyzer = VisionAnalyzer()

    result = analyzer.analyze(
        str(image),
    )

    assert result.confidence == 0.5
    assert result.metadata["image_path"] == str(image)
