from __future__ import annotations

from aura.voice.models import VoiceOutput


class SpeechOutput:
    """
    Convert text response into voice.
    """

    def speak(
        self,
        text: str,
    ) -> VoiceOutput:
        """
        Text to speech abstraction.
        """

        return VoiceOutput(
            text=text,
            success=True,
        )
