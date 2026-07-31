"""AI service boundary used by the rest of AURA."""

from __future__ import annotations

from typing import Any

from aura.ai.providers.base import AIProvider
from aura.ai.tool_call import ToolCall
from aura.ai.tool_runner import ToolRunner
from aura.brain.runtime import AgentRuntime
from aura.context.builder import ContextBuilder
from aura.core.ai_events import (
    AIResponseCompleted,
    AIResponseStarted,
    ToolCompleted,
    ToolFailed,
    ToolStarted,
)
from aura.core.events import Event, EventBus
from aura.core.session import Session
from aura.core.tool_result import ToolResult
from aura.core.tools import ToolRegistry


class AIManager:
    """Delegate response generation to the configured provider."""

    def __init__(
        self,
        provider: AIProvider,
        session: Session,
        tools: ToolRegistry,
        tool_runner: ToolRunner,
        max_tool_calls: int = 5,
        event_bus: EventBus | None = None,
        context_builder: ContextBuilder | None = None,
        runtime: AgentRuntime | None = None,
    ) -> None:
        self._provider = provider
        self._session = session
        self._tools = tools
        self._tool_runner = tool_runner
        self._max_tool_calls = max_tool_calls
        self._event_bus = event_bus
        self._context_builder = context_builder
        self._runtime = runtime

    @property
    def provider(self) -> AIProvider:
        return self._provider

    @property
    def session(self) -> Session:
        return self._session

    @property
    def tools(self) -> ToolRegistry:
        return self._tools

    @property
    def tool_runner(self) -> ToolRunner:
        return self._tool_runner

    @property
    def max_tool_calls(self) -> int:
        return self._max_tool_calls

    @property
    def runtime(self) -> AgentRuntime | None:
        """Return agent runtime."""

        return self._runtime

    def emit(
        self,
        event: Event,
    ) -> None:
        """Publish event when event bus exists."""

        if self._event_bus:
            self._event_bus.publish(
                event,
            )

    def set_provider(
        self,
        provider: AIProvider,
    ) -> None:
        """Replace active provider."""

        self._provider = provider

    def run_tool(
        self,
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> ToolResult:
        """Execute registered tool."""

        return self._tool_runner.run(
            name,
            *args,
            **kwargs,
        )

    def execute_tool_call(
        self,
        call: ToolCall,
    ) -> ToolResult:
        """Execute provider requested tool."""

        self.emit(
            ToolStarted(
                call.name,
            )
        )

        result = self._tool_runner.run(
            call.name,
            **call.arguments,
        )

        if result.success:
            self.emit(
                ToolCompleted(
                    call.name,
                    result.output,
                )
            )
        else:
            self.emit(
                ToolFailed(
                    call.name,
                    result.error or "Unknown error",
                )
            )

        return result

    def build_tool_message(
        self,
        result: ToolResult,
    ) -> dict[str, str]:
        """Convert tool result."""

        return {
            "role": "tool",
            "content": result.output,
        }

    def build_tool_output(
        self,
        call: ToolCall,
        result: ToolResult,
    ) -> dict[str, str]:
        """Convert tool result to function output."""

        return {
            "type": "function_call_output",
            "call_id": call.call_id or "",
            "output": result.output,
        }

    def build_context(
        self,
        query: str | None = None,
    ) -> tuple[
        list[dict[str, str]],
        list[dict[str, object]],
    ]:
        """Build provider context."""

        if self._context_builder:
            context = self._context_builder.build(
                query=query,
                metadata={},
            )

            return (
                context.messages,
                context.tools,
            )

        return (
            self._session.messages(),
            self._tools.openai_schemas(),
        )

    def respond(
        self,
        user_message: str,
    ) -> str:
        """Generate response."""

        self.emit(
            AIResponseStarted(
                user_message,
            )
        )

        self._session.add_user_message(
            user_message,
        )

        if self._runtime:
            state = self._runtime.run(
                user_message,
            )

            if state.output:
                message = state.output

                self._session.add_assistant_message(
                    message,
                )

                self.emit(
                    AIResponseCompleted(
                        message,
                    )
                )

                return message

        history, tools = self.build_context(
            query=user_message,
        )

        response = self._provider.generate_response(
            user_message,
            history=history,
            tools=tools,
        )

        tool_call_count = 0

        while response.has_tool_call:
            tool_call_count += 1

            if tool_call_count > self._max_tool_calls:
                message = "AURA çok fazla araç çağrısı denedi."

                self._session.add_assistant_message(
                    message,
                )

                self.emit(
                    AIResponseCompleted(
                        message,
                    )
                )

                return message

            call = response.tool_call

            result = self.execute_tool_call(
                call,
            )

            self._session.add_tool_message(
                result.output,
            )

            history, tools = self.build_context(
                query=user_message,
            )

            response = self._provider.generate_response(
                user_message,
                history=history,
                tools=tools,
                tool_outputs=[
                    self.build_tool_output(
                        call,
                        result,
                    )
                ],
            )

        if response.text:
            message = response.text
        else:
            message = "AURA şu anda yanıt üretemedi."

        self._session.add_assistant_message(
            message,
        )

        self.emit(
            AIResponseCompleted(
                message,
            )
        )

        return message
