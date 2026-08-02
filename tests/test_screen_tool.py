from pathlib import Path

from aura.tools.screen import ScreenCaptureTool


def test_screen_tool_metadata():
    tool = ScreenCaptureTool()

    assert tool.name == "screen_capture"

    assert tool.capability == "screen"

    assert tool.requires_permission


def test_screen_tool_capture():
    tool = ScreenCaptureTool()

    result = tool.execute(
        action="capture",
    )

    assert result.success

    assert result.name == "screen_capture"

    assert "image_path" in result.metadata

    image_path = result.metadata["image_path"]

    assert isinstance(
        image_path,
        str,
    )

    assert image_path.endswith(
        ".png",
    )

    assert Path(
        image_path,
    ).exists()
