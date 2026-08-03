from aura.tools.search import SearchTool


def test_search_tool_metadata():
    tool = SearchTool()

    assert tool.name == "search"
    assert tool.capability == "search"


def test_search_tool_execution():
    tool = SearchTool()

    result = tool.execute(
        "Unity 6 features",
    )

    assert "Unity 6 features" in result
