from dataclasses import dataclass


@dataclass
class VoiceInput:
    text: str
    confidence: float = 0.0


@dataclass
class VoiceOutput:
    text: str
    success: bool = True
