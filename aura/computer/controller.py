from __future__ import annotations

import subprocess


class ComputerController:
    """Control operating system actions safely."""

    ALLOWED_APPLICATIONS = {
        "chrome": "chrome",
        "notepad": "notepad",
        "calculator": "calc",
        "paint": "mspaint",
        "explorer": "explorer",
    }

    def open_application(
        self,
        application: str,
    ) -> str:
        """Open approved application."""

        executable = self.ALLOWED_APPLICATIONS.get(
            application.casefold(),
        )

        if executable is None:
            return f"Blocked application: {application}"

        subprocess.Popen(
            executable,
            shell=True,
        )

        return f"Opened application: {application}"

    def close_application(
        self,
        application: str,
    ) -> str:
        """Close application placeholder."""

        return f"Close request received: {application}"

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

        if action.startswith(
            "close:",
        ):
            application = action.split(
                ":",
                1,
            )[1]

            return self.close_application(
                application,
            )

        return f"Unsupported computer action: {action}"
