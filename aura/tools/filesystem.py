"""Filesystem tool implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aura.core.tools import Tool


class FileSystemTool(Tool):
    """Safe filesystem operations inside workspace."""

    def __init__(
        self,
        workspace: str | Path = "workspace",
    ) -> None:
        self._workspace = Path(
            workspace,
        ).resolve()

        self._workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

    @property
    def name(
        self,
    ) -> str:
        """Return tool name."""

        return "filesystem"

    @property
    def capability(
        self,
    ) -> str:
        """Return capability."""

        return "filesystem"

    @property
    def description(
        self,
    ) -> str:
        """Return description."""

        return "Manage files inside AURA workspace."

    @property
    def risk_level(
        self,
    ) -> str:
        """Filesystem operations are sensitive."""

        return "medium"

    @property
    def requires_permission(
        self,
    ) -> bool:
        return False

    @property
    def parameters(
        self,
    ) -> dict[str, Any]:
        return {
            "operation": {
                "type": "string",
                "description": ("Operation: read, write, list, create_folder"),
            },
            "path": {
                "type": "string",
                "description": "Relative workspace path.",
            },
            "content": {
                "type": "string",
                "description": "Content for write operation.",
            },
        }

    def execute(
        self,
        operation: str,
        path: str = "",
        content: str = "",
    ) -> str:
        """Execute filesystem operation."""

        target = self._safe_path(
            path,
        )

        if operation == "list":
            return "\n".join(item.name for item in target.iterdir())

        if operation == "create_folder":
            target.mkdir(
                parents=True,
                exist_ok=True,
            )

            return f"Folder created: {path}"

        if operation == "read":
            return target.read_text(
                encoding="utf-8",
            )

        if operation == "write":
            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            target.write_text(
                content,
                encoding="utf-8",
            )

            return f"File written: {path}"

        raise ValueError(
            f"Unsupported filesystem operation: {operation}",
        )

    def _safe_path(
        self,
        path: str,
    ) -> Path:
        """Prevent escaping workspace."""

        target = (self._workspace / path).resolve()

        if not str(target).startswith(
            str(self._workspace),
        ):
            raise PermissionError(
                "Path outside workspace is not allowed.",
            )

        return target
