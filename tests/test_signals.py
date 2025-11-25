"""
Tests for the signal scoring module.
"""

from pulsecraft.base import CustomerContext
from pulsecraft.signals import SignalScoringAgent


class TestSignalScoringAgent:
    """Tests for SignalScoringAgent."""

    def test_agent_initialization(self):
        """Test agent initialization with defaults."""
        agent = SignalScoringAgent()

        assert agent.name == "SignalScoringAgent"
        assert "churn_propensity" in agent.scoring_models
        assert "purchase_propensity" in agent.scoring_models
        assert "engagement_score" in agent.scoring_models

    def test_compute_churn_propensity(self):
        """Test computing churn propensity."""
        agent = SignalScoringAgent()
        context = CustomerContext(
            customer_id="cust_123",
            behavioral_signals={
                "days_since_activity": 60,
                "support_tickets_30d": 3,
            },
        )

        result = agent.process(context)

        assert "churn_propensity" in result.propensity_scores
        score = result.propensity_scores["churn_propensity"]
        assert 0 <= score <= 1

    def test_compute_purchase_propensity(self):
        """Test computing purchase propensity."""
        agent = SignalScoringAgent()
        context = CustomerContext(
            customer_id="cust_123",
            attributes={"total_purchases": 5},
            behavioral_signals={
                "product_views_7d": 15,
                "cart_additions_7d": 3,
            },
        )

        result = agent.process(context)

        assert "purchase_propensity" in result.propensity_scores
        score = result.propensity_scores["purchase_propensity"]
        assert 0 <= score <= 1

    def test_compute_engagement_score(self):
        """Test computing engagement score."""
        agent = SignalScoringAgent()
        context = CustomerContext(
            customer_id="cust_123",
            behavioral_signals={
                "email_opens_30d": 8,
                "clicks_30d": 15,
                "site_visits_30d": 10,
            },
        )

        result = agent.process(context)

        assert "engagement_score" in result.propensity_scores
        score = result.propensity_scores["engagement_score"]
        assert 0 <= score <= 100

    def test_add_custom_scoring_model(self):
        """Test adding a custom scoring model."""
        agent = SignalScoringAgent()

        def custom_score(ctx):
            return 0.75

        agent.add_scoring_model("custom_score", custom_score)

        context = CustomerContext(customer_id="cust_123")
        result = agent.process(context)

        assert "custom_score" in result.propensity_scores
        assert result.propensity_scores["custom_score"] == 0.75

    def test_remove_scoring_model(self):
        """Test removing a scoring model."""
        agent = SignalScoringAgent()

        assert agent.remove_scoring_model("churn_propensity") is True
        assert agent.remove_scoring_model("nonexistent") is False
        assert "churn_propensity" not in agent.scoring_models

    def test_audit_log_created(self):
        """Test that audit log is created on process."""
        agent = SignalScoringAgent()
        context = CustomerContext(customer_id="cust_123")

        agent.process(context)

        audit_log = agent.get_audit_log()
        assert len(audit_log) == 1
        assert audit_log[0]["agent_name"] == "SignalScoringAgent"
