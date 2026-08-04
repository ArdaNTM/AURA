from __future__ import annotations

from aura.agent.agent import Agent
from aura.voice.microphone import Microphone
from aura.voice.models import VoiceOutput
from aura.voice.speech_output import SpeechOutput
from aura.voice.speech_recognition import SpeechRecognizer


class VoiceController:
    """
    Coordinate voice interaction.
    """

    def __init__(
        self,
        agent: Agent,
        microphone: Microphone | None = None,
        recognizer: SpeechRecognizer | None = None,
        output: SpeechOutput | None = None,
    ) -> None:

        self._agent = agent

        self._microphone = microphone or Microphone()

        self._recognizer = recognizer or SpeechRecognizer()

        self._output = output or SpeechOutput()

    def listen_and_execute(
        self,
    ) -> VoiceOutput:

        audio = self._microphone.listen()

        voice_input = self._recognizer.transcribe(
            audio,
        )

        if not voice_input.text:
            return VoiceOutput(
                text="",
                success=False,
            )

        result = self._agent.execute(
            voice_input.text,
        )

        response = str(
            (
                result.output
                if hasattr(
                    result,
                    "output",
                )
                else result
            ),
        )

        return self._output.speak(
            response,
        )
