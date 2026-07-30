"""OpenAI-backed implementation of the AURA provider contract."""

from __future__ import annotations

from typing import Any

from openai import OpenAI

from aura.ai.openai_parser import OpenAIParser
from aura.ai.provider_response import ProviderResponse
from aura.ai.providers.base import AIProvider


class OpenAIProvider(AIProvider):
    """Generate text with the OpenAI Responses API."""

    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        self._client = OpenAI(
            api_key=api_key,
        )

        self._model = model
        self._parser = OpenAIParser()

    @property
    def name(self) -> str:
        """Return the provider name."""

        return "openai"

    @property
    def model(self) -> str:
        """Return the configured model name."""

        return self._model

    def _format_tools(
        self,
        tools: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        """Convert AURA tool schemas into OpenAI tools."""

        if not tools:
            return []

        return [
            {
                "type": "function",
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            }
            for tool in tools
        ]

    def _format_tool_outputs(
        self,
        tool_outputs: list[dict[str, str]] | None,
    ) -> list[dict[str, str]]:
        """Convert AURA tool outputs into OpenAI format."""

        if not tool_outputs:
            return []

        return [
            {
                "type": "function_call_output",
                "call_id": output["call_id"],
                "output": output["output"],
            }
            for output in tool_outputs
        ]

    def generate_response(
        self,
        user_message: str,
        history: list[dict[str, str]] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_outputs: list[dict[str, str]] | None = None,
    ) -> ProviderResponse:
        """Return the provider's normalized response."""

        input_messages = history or [
            {
                "role": "user",
                "content": user_message,
            }
        ]

        formatted_tool_outputs = self._format_tool_outputs(
            tool_outputs,
        )

        if formatted_tool_outputs:
            input_messages = [
                *input_messages,
                *formatted_tool_outputs,
            ]

        request: dict[str, Any] = {
            "model": self._model,
            "input": input_messages,
        }

        formatted_tools = self._format_tools(
            tools,
        )

        if formatted_tools:
            request["tools"] = formatted_tools

        response = self._client.responses.create(
            **request,
        )

        return self._parser.parse(
            response,
        )
