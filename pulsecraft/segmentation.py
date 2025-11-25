"""
Segmentation Agent for customer segmentation.

Assigns customers to segments based on their attributes and behavioral signals.
"""

import time
from typing import Any, Optional

from pulsecraft.base import BaseAgent, CustomerContext


class SegmentationAgent(BaseAgent):
    """
    Agent responsible for customer segmentation.

    Segments customers based on configurable rules and attributes to enable
    targeted messaging strategies.
    """

    def __init__(
        self,
        name: str = "SegmentationAgent",
        segment_rules: Optional[dict] = None,
    ):
        """
        Initialize the segmentation agent.

        Args:
            name: Agent name for audit logging
            segment_rules: Dictionary mapping segment names to rule functions
        """
        super().__init__(name)
        self.segment_rules = segment_rules or self._default_segment_rules()

    def _default_segment_rules(self) -> dict:
        """Return default segmentation rules."""
        return {
            "high_value": lambda ctx: ctx.attributes.get("lifetime_value", 0) > 1000,
            "at_risk": lambda ctx: ctx.behavioral_signals.get("days_since_activity", 0) > 30,
            "new_customer": lambda ctx: ctx.attributes.get("tenure_days", 0) < 30,
            "engaged": lambda ctx: ctx.behavioral_signals.get("engagement_score", 0) > 70,
        }

    def process(self, context: CustomerContext) -> CustomerContext:
        """
        Assign a segment to the customer based on rules.

        Args:
            context: Customer context with attributes and signals

        Returns:
            Updated customer context with segment assignment
        """
        start_time = time.time()

        assigned_segment = "default"
        matching_segments = []

        for segment_name, rule_fn in self.segment_rules.items():
            try:
                if rule_fn(context):
                    matching_segments.append(segment_name)
            except Exception:
                # Skip rules that fail to evaluate
                continue

        # Use first matching segment (priority-based)
        if matching_segments:
            assigned_segment = matching_segments[0]

        context.segment = assigned_segment
        context.metadata["matching_segments"] = matching_segments

        duration_ms = (time.time() - start_time) * 1000
        self._create_audit_record(
            input_summary=f"customer_id={context.customer_id}",
            output_summary=f"segment={assigned_segment}",
            duration_ms=duration_ms,
            metadata={"matching_segments": matching_segments},
        )

        return context

    def add_segment_rule(self, segment_name: str, rule_fn: Any) -> None:
        """
        Add a custom segmentation rule.

        Args:
            segment_name: Name of the segment
            rule_fn: Function that takes CustomerContext and returns bool
        """
        self.segment_rules[segment_name] = rule_fn

    def remove_segment_rule(self, segment_name: str) -> bool:
        """
        Remove a segmentation rule.

        Args:
            segment_name: Name of the segment to remove

        Returns:
            True if rule was removed, False if it didn't exist
        """
        if segment_name in self.segment_rules:
            del self.segment_rules[segment_name]
            return True
        return False
