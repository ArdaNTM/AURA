"""Terminal tool implementation."""

from __future__ import annotations

import subprocess
from typing import Any

from aura.core.tools import Tool


class TerminalTool(Tool):
    """Execute safe terminal commands."""

    BLOCKED_COMMANDS = (
        "format",
        "shutdown",
        "reboot",
        "rm -rf",
        "del /s",
        "credential",
        "password",
        "token",
    )

    @property
    def name(
        self,
    ) -> str:
        """Return tool name."""

        return "terminal"

    @property
    def capability(
        self,
    ) -> str:
        """Return capability."""

        return "terminal"

    @property
    def description(
        self,
    ) -> str:
        """Return terminal description."""

        return "Execute operating system commands."

    @property
    def risk_level(
        self,
    ) -> str:
        """Terminal execution is high risk."""

        return "high"

    @property
    def requires_permission(
        self,
    ) -> bool:
        """Require user approval."""

        return True

    @property
    def parameters(
        self,
    ) -> dict[str, Any]:
        return {
            "command": {
                "type": "string",
                "description": "Terminal command to execute.",
            }
        }

    def execute(
        self,
        command: str,
    ) -> str:
        """Execute terminal command."""

        self._validate_command(
            command,
        )

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip(),
            )

        return result.stdout.strip()

    def _validate_command(
        self,
        command: str,
    ) -> None:
        """Block dangerous commands."""

        lowered = command.casefold()

        for blocked in self.BLOCKED_COMMANDS:
            if blocked in lowered:
                raise PermissionError(
                    f"Blocked terminal command: {blocked}",
                )
