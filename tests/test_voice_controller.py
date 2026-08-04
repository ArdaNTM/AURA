from aura.voice.models import VoiceInput
from aura.voice.speech_recognition import SpeechRecognizer


def test_voice_recognition_empty_audio():

    recognizer = SpeechRecognizer()

    result = recognizer.transcribe(
        b"",
    )

    assert isinstance(
        result,
        VoiceInput,
    )

    assert result.text == ""
