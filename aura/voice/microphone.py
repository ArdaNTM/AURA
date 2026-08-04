from __future__ import annotations


class Microphone:
    """
    Capture user voice input.

    Hardware layer abstraction.
    """

    def listen(self) -> bytes:
        """
        Capture raw audio.

        Real microphone providers
        will override this.
        """

        return b""
