from aura.voice.models import VoiceOutput


def test_voice_output():

    output = VoiceOutput(
        text="hello",
    )

    assert output.success

    assert output.text == "hello"
