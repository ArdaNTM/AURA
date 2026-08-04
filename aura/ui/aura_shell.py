from __future__ import annotations

from aura.agent.agent import Agent


class AuraShell:
    """Interactive AURA terminal interface."""

    def __init__(
        self,
        agent: Agent,
    ) -> None:
        self._agent = agent

    def start(self) -> None:
        print("""
================================
             AURA
   Personal Autonomous Assistant
================================

Type 'exit' to quit.
""")

        while True:
            try:
                message = input("\nYou > ")

            except KeyboardInterrupt:
                print("\nAURA shutting down.")
                break

            if message.lower() in {
                "exit",
                "quit",
            }:
                break

            if not message.strip():
                continue

            try:
                state = self._agent.execute(
                    message,
                )

                self._display(
                    state,
                )

            except Exception as error:
                print(
                    f"AURA ERROR: {error}",
                )

    def _display(
        self,
        state,
    ) -> None:
        print("\nAURA >")

        if state.output:
            print(
                state.output,
            )

        if state.metadata:
            print(
                "\nStatus:",
            )

            if "performance" in state.metadata:
                print(
                    "Performance:",
                    state.metadata["performance"],
                )

            if state.metadata.get(
                "permission_required",
            ):
                print(
                    "Permission required.",
                )

        print("\n--------------------------------")
