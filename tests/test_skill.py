from aura.brain.skill import Skill


def test_skill_registers_success():

    skill = Skill(
        name="calculation",
        domain="math",
    )

    skill.register_result(
        success=True,
        score=0.9,
    )

    assert skill.usage_count == 1

    assert skill.success_rate == 1.0

    assert skill.confidence == 0.18


def test_skill_adds_tools():

    skill = Skill(
        name="coding",
        domain="software",
    )

    skill.add_tool(
        "terminal",
    )

    skill.add_tool(
        "terminal",
    )

    assert skill.required_tools == [
        "terminal",
    ]
