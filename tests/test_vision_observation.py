from aura.brain.observation import Observation


def test_observation_supports_vision_metadata():

    observation = Observation(
        source="screen_capture",
        output="screen.png",
        metadata={
            "image_path": "screen.png",
            "vision": {
                "confidence": 0.5,
            },
        },
    )

    assert observation.metadata["image_path"] == "screen.png"

    assert observation.metadata["vision"]["confidence"] == 0.5
