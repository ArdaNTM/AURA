from aura.brain.context_fusion import ContextFusion


def test_multimodal_context_fusion():

    fusion = ContextFusion()

    result = fusion.fuse(
        memory=[
            (
                "assistant",
                "previous task success",
            )
        ],
        vision={
            "objects": [
                "window",
            ]
        },
        user_profile={
            "coding_style": "clean",
        },
        learning={
            "success_rate": 0.9,
        },
    )

    assert "memory_context" in result
    assert "vision_context" in result
    assert "user_context" in result
    assert "learning_context" in result

    assert result["fusion"]["confidence"] == 1.0
