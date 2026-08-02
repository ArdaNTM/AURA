from pathlib import Path

from aura.computer.screen import ScreenCapture


def test_screen_capture_creates_file(
    tmp_path,
):
    capture = ScreenCapture()

    target = tmp_path / "screen.png"

    result = capture.capture(
        str(target),
    )

    assert result == str(
        target.resolve(),
    )

    assert Path(result).exists()
