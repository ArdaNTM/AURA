"""Intent classification for AURA."""

from __future__ import annotations

import re

from aura.brain.models import IntentAnalysis


class IntentEngine:
    """Detect user intent."""

    def classify(
        self,
        message: str,
    ) -> IntentAnalysis:
        """Return detected intent analysis."""

        text = message.casefold()

        expression = self._extract_expression(
            message,
        )

        if self._is_calculation(
            text,
        ):
            entities: dict[str, object] = {}

            if expression:
                entities["expression"] = expression

            return IntentAnalysis(
                intent="calculation",
                confidence=0.95,
                entities=entities,
            )

        if any(
            keyword in text
            for keyword in [
                "araştır",
                "google",
                "web",
                "internet",
                "search",
            ]
        ):
            return IntentAnalysis(
                intent="search",
                confidence=0.90,
            )

        if any(
            keyword in text
            for keyword in [
                "python",
                "kod",
                "code",
                "program",
            ]
        ):
            return IntentAnalysis(
                intent="coding",
                confidence=0.90,
            )

        if any(
            keyword in text
            for keyword in [
                "dosya",
                "file",
                "klasör",
                "folder",
            ]
        ):
            return IntentAnalysis(
                intent="filesystem",
                confidence=0.90,
            )

        if any(
            keyword in text
            for keyword in [
                "aç",
                "kapat",
                "uygulama",
                "chrome",
                "bilgisayar",
            ]
        ):
            return IntentAnalysis(
                intent="computer",
                confidence=0.90,
            )

        if any(
            keyword in text
            for keyword in [
                "hatırla",
                "remember",
                "hafıza",
                "memory",
            ]
        ):
            return IntentAnalysis(
                intent="memory",
                confidence=0.90,
            )

        return IntentAnalysis(
            intent="conversation",
            confidence=0.70,
        )

    def _is_calculation(
        self,
        message: str,
    ) -> bool:
        """Detect calculation intent."""

        if any(
            keyword in message
            for keyword in (
                "hesapla",
                "kaç",
                "topla",
                "çıkar",
                "çarp",
                "böl",
            )
        ):
            return True

        return bool(
            re.search(
                r"\d+\s*[-+*/]\s*\d+",
                message,
            )
        )

    def _extract_expression(
        self,
        message: str,
    ) -> str | None:
        """Extract mathematical expression."""

        expression = re.sub(
            r"[^\d+\-*/().]",
            "",
            message,
        )

        if expression:
            return expression

        return None
