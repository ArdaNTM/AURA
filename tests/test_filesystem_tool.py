from aura.tools.filesystem import FileSystemTool


def test_filesystem_creates_and_reads_file(tmp_path):

    tool = FileSystemTool(
        tmp_path,
    )

    tool.execute(
        "write",
        "hello.txt",
        "AURA",
    )

    result = tool.execute(
        "read",
        "hello.txt",
    )

    assert result == "AURA"


def test_filesystem_blocks_workspace_escape(tmp_path):

    tool = FileSystemTool(
        tmp_path,
    )

    try:
        tool.execute(
            "read",
            "../secret.txt",
        )

        assert False

    except PermissionError:
        assert True
