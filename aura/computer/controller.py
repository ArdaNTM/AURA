"""Computer controller abstraction."""

from __future__ import annotations

import subprocess


class ComputerController:
    """Control operating system actions."""

    def open_application(
        self,
        application: str,
    ) -> str:
        """Open application."""

        subprocess.Popen(
            application,
            shell=True,
        )

        return f"Opened application: {application}"

    def execute_action(
        self,
        action: str,
    ) -> str:
        """Execute computer action."""

        if action.startswith(
            "open:",
        ):
            application = action.split(
                ":",
                1,
            )[1]

            return self.open_application(
                application,
            )

        return f"Unsupported computer action: {action}"
