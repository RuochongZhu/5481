"""Pipeline Router — abstraction layer for loop/backtrack logic.

Current: pure Python while/if.
Future: can be swapped to LangGraph StateGraph without changing callers.
"""

import logging
import os

log = logging.getLogger("research_agent")


class PipelineRouter:
    """Decides what to do next based on evaluation scores.

    Routing table maps weakest dimension → (action, target_phase, params).
    """

    ROUTING_TABLE = {
        "coverage":      ("rerun", "1",   {"mode": "补搜"}),
        "narrative":     ("rerun", "3.5", {}),
        "contradiction": ("rerun", "3.7", {}),
        "gap":           ("rerun", "3",   {"retry": True}),
        "honesty":       ("rerun", "4",   {}),
    }

    def __init__(self, target_score: float = 0.8, max_iterations: int = 5):
        self.target_score = target_score
        self.max_iterations = max_iterations

    def decide(self, aggregated: dict) -> dict:
        """Input: aggregated review scores. Output: action dict.

        Returns:
            {"action": "done|rerun|human",
             "target_phase": "1"|"3"|"3.5"|...,
             "reason": "...",
             "params": {...}}
        """
        score = aggregated.get("overall_score", 0)
        scores = aggregated.get("individual_scores", {})
        weakest = aggregated.get("weakest_dimension", "")

        # Reviewer disagreement → human review
        if aggregated.get("needs_human_review"):
            return {
                "action": "human",
                "reason": f"Reviewer disagreement: {aggregated.get('disagreements', [])}",
            }

        # Target reached
        if score >= self.target_score:
            return {
                "action": "done",
                "reason": f"Score {score:.3f} ≥ target {self.target_score}",
            }

        # Route to weakest dimension's phase
        action, phase, params = self.ROUTING_TABLE.get(
            weakest, ("human", "3", {})
        )

        return {
            "action": action,
            "target_phase": phase,
            "weakest": weakest,
            "weakest_score": scores.get(weakest, 0),
            "reason": f"Weakest: {weakest} ({scores.get(weakest, 0):.2f}) → Phase {phase}",
            "params": params,
        }

    def should_enable_graphrag(self, corpus_size: int,
                               narrative_score: float,
                               consecutive_low: int) -> bool:
        """Decide whether to enable nano-graphrag layer.

        Trigger conditions (from addendum):
        - corpus > 500 → enable
        - narrative_score < 0.5 for 2+ consecutive iterations AND corpus < 500 → enable
        - corpus ≤ 300 AND narrative_score ≥ 0.6 → don't need
        """
        threshold = int(os.environ.get("CORPUS_SIZE_THRESHOLD_FOR_GRAPHRAG", "500"))

        if corpus_size > threshold:
            return True
        if consecutive_low >= 2 and narrative_score < 0.5:
            return True
        return False

    def should_use_cosmograph(self, corpus_size: int) -> bool:
        """Switch from pyvis to Cosmograph for large corpora."""
        threshold = int(os.environ.get("CORPUS_SIZE_THRESHOLD_FOR_COSMOGRAPH", "500"))
        return corpus_size > threshold
