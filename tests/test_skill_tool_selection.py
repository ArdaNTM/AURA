from aura.brain.skill import Skill
from aura.brain.skill_registry import SkillRegistry


def test_skill_registry_returns_preferred_tool():

    registry = SkillRegistry()

    skill = Skill(
        name="calculation",
        domain="math",
    )

    skill.add_tool(
        "calculator",
    )

    registry.register(
        skill,
    )

    assert (
        registry.preferred_tool(
            "calculation",
        )
        == "calculator"
    )
