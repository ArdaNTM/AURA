"""Safe code execution tool."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from aura.core.tools import Tool


class CodeExecutionTool(Tool):
    """Execute generated code inside isolated workspace."""

    @property
    def name(
        self,
    ) -> str:
        return "code_execution"

    @property
    def capability(
        self,
    ) -> str:
        return "coding"

    @property
    def description(
        self,
    ) -> str:
        return "Execute Python code in a sandbox."

    @property
    def risk_level(
        self,
    ) -> str:
        return "medium"

    @property
    def requires_permission(
        self,
    ) -> bool:
        return True

    @property
    def parameters(
        self,
    ) -> dict[str, Any]:
        return {
            "code": {
                "type": "string",
                "description": "Python code to execute.",
            }
        }

    def execute(
        self,
        code: str,
    ) -> str:
        """Run python code safely."""

        self._validate_code(
            code,
        )

        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "main.py"

            file.write_text(
                code,
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(file),
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    result.stderr.strip(),
                )

            return result.stdout.strip()

    def _validate_code(
        self,
        code: str,
    ) -> None:
        """Block dangerous operations."""

        blocked = (
            "os.system",
            "subprocess",
            "shutil",
            "socket",
            "password",
            "token",
            "credential",
        )

        lowered = code.casefold()

        for item in blocked:
            if item in lowered:
                raise PermissionError(
                    f"Blocked code operation: {item}",
                )
