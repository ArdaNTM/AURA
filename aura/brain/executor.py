"""AURA plan execution layer."""

from __future__ import annotations

from aura.ai.tool_runner import ToolRunner
from aura.brain.audit_log import AuditLog
from aura.brain.models import Decision, PlanStep
from aura.brain.observation import Observation
from aura.brain.permission_runtime import PermissionRuntime
from aura.brain.safety_policy import SafetyPolicy
from aura.brain.tool_recovery import ToolRecovery
from aura.core.tool_result import ToolResult


class PlanExecutor:
    """Execute planned actions."""

    def __init__(
        self,
        tool_runner: ToolRunner,
        permission_runtime: PermissionRuntime | None = None,
        recovery: ToolRecovery | None = None,
        audit_log: AuditLog | None = None,
        safety_policy: SafetyPolicy | None = None,
    ) -> None:

        self._tool_runner = tool_runner

        self._permission_runtime = permission_runtime or PermissionRuntime()

        self._recovery = recovery or ToolRecovery()

        self._audit_log = audit_log or AuditLog()

        self._safety_policy = safety_policy or SafetyPolicy()

    @property
    def tool_runner(
        self,
    ) -> ToolRunner:
        """Return tool runner."""

        return self._tool_runner

    def execute(
        self,
        decision: Decision,
    ) -> list[ToolResult]:
        """Execute decision plan."""

        if decision.requires_permission:

            if not self._permission_runtime.check(
                decision,
            ):
                return []

        results: list[ToolResult] = []

        for step in decision.plan:
            result = self._execute_step(
                step,
            )

            if result is not None:
                results.append(result)

            step.completed = True

        return results

    def execute_with_observation(
        self,
        decision: Decision,
    ) -> list[Observation]:
        """Execute plan and return observations."""

        observations: list[Observation] = []

        for step in decision.plan:
            result = self._execute_step(
                step,
            )

            step.completed = True

            if result is None:
                continue

            observations.append(
                Observation(
                    source=result.name,
                    output=result.output,
                    success=result.success,
                    metadata=result.metadata
                    | (
                        {
                            "error": result.error,
                        }
                        if result.error
                        else {}
                    ),
                )
            )

        return observations

    def _execute_step(
        self,
        step: PlanStep,
    ) -> ToolResult | None:
        """Execute a single plan step."""

        safety = self._safety_policy.evaluate(
            step.action,
        )

        if not safety.allowed:
            self._audit_log.record(
                action=step.action,
                success=False,
                approved=False,
                details=safety.reason,
            )

            return ToolResult(
                name=step.action,
                output=None,
                success=False,
                error=safety.reason,
                duration=0,
            )

        if step.action is None:
            return None

        if step.action in (
            "analyze",
            "respond",
        ):
            return None

        attempt = 0
        recovery_metadata: dict[str, object] = {}

        while True:
            result = self._tool_runner.run(
                step.action,
                **step.metadata,
            )

            if not self._recovery.should_retry(
                result,
                attempt,
            ):
                if recovery_metadata:
                    return ToolResult(
                        name=result.name,
                        output=result.output,
                        success=result.success,
                        error=result.error,
                        duration=result.duration,
                        timestamp=result.timestamp,
                        metadata=result.metadata | recovery_metadata,
                    )

                self._audit_log.record(
                    action=result.name,
                    success=result.success,
                    approved=True,
                    details="Tool execution",
                )

                return result

            attempt += 1

            recovery_metadata = {
                "recovery": self._recovery.analyze(
                    result,
                ),
                "retry_attempt": attempt,
            }
