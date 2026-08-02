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


def test_filesystem_lists_directory(tmp_path):

    tool = FileSystemTool(
        tmp_path,
    )

    tool.execute(
        "write",
        "a.txt",
        "A",
    )

    tool.execute(
        "write",
        "b.txt",
        "B",
    )

    result = tool.execute(
        "list",
        "",
    )

    assert "a.txt" in result
    assert "b.txt" in result


def test_filesystem_creates_folder(tmp_path):

    tool = FileSystemTool(
        tmp_path,
    )

    result = tool.execute(
        "create_folder",
        "documents",
    )

    assert "Folder created" in result
    assert (tmp_path / "documents").exists()


def test_filesystem_rejects_unknown_operation(tmp_path):

    tool = FileSystemTool(
        tmp_path,
    )

    try:
        tool.execute(
            "delete",
            "test.txt",
        )

        assert False

    except ValueError as exc:
        assert "Unsupported filesystem operation" in str(exc)
