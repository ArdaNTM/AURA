"""Utilities for parsing OpenAI responses."""

from __future__ import annotations

import json
from typing import Any

from aura.ai.provider_response import ProviderResponse
from aura.ai.tool_call import ToolCall


class OpenAIParser:
    """Parse OpenAI Responses API outputs."""

    def parse(
        self,
        response: Any,
    ) -> ProviderResponse:
        """Convert OpenAI response into AURA format."""

        for item in response.output:
            if item.type == "function_call":
                return ProviderResponse(
                    tool_call=ToolCall(
                        name=item.name,
                        arguments=json.loads(
                            item.arguments,
                        ),
                        call_id=getattr(
                            item,
                            "call_id",
                            None,
                        ),
                    ),
                )

        text = response.output_text.strip()

        return ProviderResponse(
            text=text or "AURA şu anda yanıt üretemedi.",
        )
