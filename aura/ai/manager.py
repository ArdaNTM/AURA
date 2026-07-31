"""AI service boundary used by the rest of AURA."""

from __future__ import annotations

import inspect
from typing import Any

from aura.ai.providers.base import AIProvider
from aura.ai.tool_call import ToolCall
from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
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
        brain: Brain | None = None,
        executor: PlanExecutor | None = None,
    ) -> None:
        self._provider = provider
        self._session = session
        self._tools = tools
        self._tool_runner = tool_runner
        self._max_tool_calls = max_tool_calls
        self._event_bus = event_bus
        self._context_builder = context_builder
        self._brain = brain
        self._executor = executor
        self._last_action = None

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
    def brain(self) -> Brain | None:
        return self._brain

    @property
    def executor(self) -> PlanExecutor | None:
        return self._executor

    @property
    def last_action(self) -> object | None:
        return self._last_action

    def build_brain_metadata(self) -> dict[str, object]:
        """Return current brain decision metadata."""

        if not self._last_action:
            return {}

        return {
            "action": self._last_action.name,
            "reason": self._last_action.reason,
        }

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

    def run_brain_action(
        self,
    ) -> ToolResult | None:
        """Execute selected brain action."""

        if not self._last_action:
            return None

        if self._last_action.name != "execute_tool":
            return None

        if not self._last_action.tool_name:
            return None

        return self._tool_runner.run(
            self._last_action.tool_name,
            **self._last_action.parameters,
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
        memories: list[tuple[str, str]] | None = None,
    ) -> tuple[
        list[dict[str, str]],
        list[dict[str, object]],
    ]:
        """Build provider context."""

        if self._context_builder:
            context = self._context_builder.build(
                query=query,
                memories=memories,
                metadata=self.build_brain_metadata(),
            )

            return (
                context.messages,
                context.tools,
            )

        return (
            self._session.messages(),
            self._tools.openai_schemas(),
        )

    def think(
        self,
        user_message: str,
        memories: list[tuple[str, str]],
    ) -> None:
        """Run brain analysis safely."""

        if not self._brain:
            return

        parameters = inspect.signature(
            self._brain.think,
        ).parameters

        if "memories" in parameters:
            _, self._last_action = self._brain.think(
                user_message,
                memories=memories,
            )
        else:
            _, self._last_action = self._brain.think(
                user_message,
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

        memories = self._session.memory.search(
            user_message,
        )

        decision = None

        if self._brain:
            parameters = inspect.signature(
                self._brain.think,
            ).parameters

            if "memories" in parameters:
                decision, self._last_action = self._brain.think(
                    user_message,
                    memories=memories,
                )
            else:
                decision, self._last_action = self._brain.think(
                    user_message,
                )

        if decision and self._executor:
            results = self._executor.execute(
                decision,
            )

            if results:
                message = results[-1].output

                self._session.add_assistant_message(
                    message,
                )

                self.emit(
                    AIResponseCompleted(
                        message,
                    )
                )

                return message

        brain_result = self.run_brain_action()

        if brain_result:
            message = brain_result.output

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
            memories=memories,
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
                memories=self._session.memory.search(
                    user_message,
                ),
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
