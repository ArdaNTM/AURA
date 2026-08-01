from aura.brain.capability import CapabilityRegistry


def test_calculation_allows_calculator():
    capabilities = CapabilityRegistry()

    assert capabilities.validate_tool(
        "calculation",
        "calculator",
    )


def test_calculation_rejects_wrong_tool():
    capabilities = CapabilityRegistry()

    assert not capabilities.validate_tool(
        "calculation",
        "filesystem",
    )
