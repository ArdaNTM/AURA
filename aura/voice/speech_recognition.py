from __future__ import annotations

from aura.voice.models import VoiceInput


class SpeechRecognizer:
    """
    Convert audio into text.
    """

    def transcribe(
        self,
        audio: bytes,
    ) -> VoiceInput:
        """
        Speech to text abstraction.
        """

        if not audio:
            return VoiceInput(
                text="",
                confidence=0.0,
            )

        return VoiceInput(
            text="",
            confidence=0.0,
        )
