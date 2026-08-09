"""Replaceable agent output evaluation."""

from typing import Any

from .schemas import Evaluation


class Evaluator:
    """Evaluate tool execution mechanically until domain evaluators arrive."""

    async def evaluate(
        self, *, results: list[dict[str, Any]], expected_output: str | None
    ) -> Evaluation:
        """Return a bounded result-quality assessment without AI scoring."""
        failures = [result for result in results if result.get("status") == "failed"]
        success = not failures
        if not results:
            score = 50.0 if expected_output else 0.0
            rationale = "No tool steps were configured for this goal."
        else:
            score = 100.0 if success else 0.0
            rationale = (
                "All configured tool steps completed."
                if success
                else "A tool step failed."
            )
        return Evaluation(success=success, quality_score=score, rationale=rationale)
