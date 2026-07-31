"""Memory storage policy for AURA agent."""

from __future__ import annotations

from aura.brain.observation import Observation


class MemoryPolicy:
    """Decide which observations should be stored."""

    def should_store(
        self,
        observation: Observation,
    ) -> bool:
        """Return whether observation is valuable for memory."""

        if not observation.success:
            return False

        if not observation.output:
            return False

        return True
