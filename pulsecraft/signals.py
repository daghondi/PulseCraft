"""
Signal Scoring Agent for behavioral signals and model-driven propensities.

Computes propensity scores based on behavioral signals and predictive models.
"""

import time
from typing import Callable, Optional

from pulsecraft.base import BaseAgent, CustomerContext


class SignalScoringAgent(BaseAgent):
    """
    Agent responsible for computing propensity scores from behavioral signals.

    Uses configurable scoring models to convert raw behavioral data into
    actionable propensity scores for personalization.
    """

    def __init__(
        self,
        name: str = "SignalScoringAgent",
        scoring_models: Optional[dict] = None,
    ):
        """
        Initialize the signal scoring agent.

        Args:
            name: Agent name for audit logging
            scoring_models: Dictionary mapping score names to model functions
        """
        super().__init__(name)
        self.scoring_models = scoring_models or self._default_scoring_models()

    def _default_scoring_models(self) -> dict[str, Callable]:
        """Return default scoring models."""
        return {
            "churn_propensity": self._compute_churn_propensity,
            "purchase_propensity": self._compute_purchase_propensity,
            "engagement_score": self._compute_engagement_score,
        }

    def _compute_churn_propensity(self, context: CustomerContext) -> float:
        """Compute churn propensity score (0-1)."""
        days_inactive = float(context.behavioral_signals.get("days_since_activity", 0))
        support_tickets = float(context.behavioral_signals.get("support_tickets_30d", 0))

        # Simple heuristic model
        base_score = min(days_inactive / 90.0, 1.0) * 0.6
        ticket_factor = min(support_tickets / 5.0, 1.0) * 0.4

        return min(base_score + ticket_factor, 1.0)

    def _compute_purchase_propensity(self, context: CustomerContext) -> float:
        """Compute purchase propensity score (0-1)."""
        recent_views = float(context.behavioral_signals.get("product_views_7d", 0))
        cart_additions = float(context.behavioral_signals.get("cart_additions_7d", 0))
        past_purchases = float(context.attributes.get("total_purchases", 0))

        # Simple heuristic model
        view_score = min(recent_views / 20.0, 1.0) * 0.3
        cart_score = min(cart_additions / 5.0, 1.0) * 0.4
        history_score = min(past_purchases / 10.0, 1.0) * 0.3

        return min(view_score + cart_score + history_score, 1.0)

    def _compute_engagement_score(self, context: CustomerContext) -> float:
        """Compute engagement score (0-100)."""
        email_opens = float(context.behavioral_signals.get("email_opens_30d", 0))
        clicks = float(context.behavioral_signals.get("clicks_30d", 0))
        site_visits = float(context.behavioral_signals.get("site_visits_30d", 0))

        # Weighted combination
        score = (
            min(email_opens / 10.0, 1.0) * 30
            + min(clicks / 20.0, 1.0) * 40
            + min(site_visits / 15.0, 1.0) * 30
        )

        return min(score, 100.0)

    def process(self, context: CustomerContext) -> CustomerContext:
        """
        Compute propensity scores for the customer.

        Args:
            context: Customer context with behavioral signals

        Returns:
            Updated customer context with propensity scores
        """
        start_time = time.time()

        computed_scores = {}
        errors = {}

        for score_name, model_fn in self.scoring_models.items():
            try:
                score = model_fn(context)
                computed_scores[score_name] = score
            except Exception as e:
                errors[score_name] = str(e)

        context.propensity_scores.update(computed_scores)
        context.metadata["scoring_errors"] = errors

        duration_ms = (time.time() - start_time) * 1000
        self._create_audit_record(
            input_summary=f"customer_id={context.customer_id}, signals={len(context.behavioral_signals)}",
            output_summary=f"scores_computed={len(computed_scores)}",
            duration_ms=duration_ms,
            metadata={
                "computed_scores": list(computed_scores.keys()),
                "errors": errors,
            },
        )

        return context

    def add_scoring_model(self, score_name: str, model_fn: Callable) -> None:
        """
        Add a custom scoring model.

        Args:
            score_name: Name of the score
            model_fn: Function that takes CustomerContext and returns a score
        """
        self.scoring_models[score_name] = model_fn

    def remove_scoring_model(self, score_name: str) -> bool:
        """
        Remove a scoring model.

        Args:
            score_name: Name of the score to remove

        Returns:
            True if model was removed, False if it didn't exist
        """
        if score_name in self.scoring_models:
            del self.scoring_models[score_name]
            return True
        return False
