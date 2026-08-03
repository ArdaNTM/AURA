from aura.brain.learning_profile import LearningProfile
from aura.brain.planner import Planner
from aura.brain.skill import Skill


def test_planner_prefers_learned_skill_tool():

    profile = LearningProfile()

    skill = Skill(
        name="calculation",
        domain="math",
    )

    skill.add_tool(
        "calculator",
    )

    profile.skill_registry.register(
        skill,
    )

    planner = Planner(
        learning_profile=profile,
    )

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.target == "calculator"
