"""Memory for autonomous improvement results."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ImprovementRecord:
    """Stored improvement experiment."""

    strategy: str

    before_score: float

    after_score: float

    success: bool

    notes: str = ""


@dataclass
class ImprovementMemory:
    """Track improvement experiments."""

    records: list[ImprovementRecord] = field(
        default_factory=list,
    )

    def add(
        self,
        strategy: str,
        before_score: float,
        after_score: float,
        success: bool,
        notes: str = "",
    ) -> None:
        """Store improvement result."""

        self.records.append(
            ImprovementRecord(
                strategy=strategy,
                before_score=before_score,
                after_score=after_score,
                success=success,
                notes=notes,
            ),
        )

    def best_strategy(
        self,
    ) -> str | None:
        """Return best performing improvement."""

        successful = [record for record in self.records if record.success]

        if not successful:
            return None

        return max(
            successful,
            key=lambda record: (record.after_score - record.before_score),
        ).strategy

    def success_rate(
        self,
        strategy: str,
    ) -> float:
        """Calculate improvement success rate."""

        items = [record for record in self.records if record.strategy == strategy]

        if not items:
            return 0.0

        return sum(1 for item in items if item.success) / len(items)
