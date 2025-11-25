"""
Tests for the segmentation module.
"""

from pulsecraft.base import CustomerContext
from pulsecraft.segmentation import SegmentationAgent


class TestSegmentationAgent:
    """Tests for SegmentationAgent."""

    def test_agent_initialization(self):
        """Test agent initialization with defaults."""
        agent = SegmentationAgent()

        assert agent.name == "SegmentationAgent"
        assert len(agent.segment_rules) > 0
        assert "high_value" in agent.segment_rules

    def test_segment_high_value_customer(self):
        """Test segmenting a high value customer."""
        agent = SegmentationAgent()
        context = CustomerContext(
            customer_id="cust_123",
            attributes={"lifetime_value": 2000},
        )

        result = agent.process(context)

        assert result.segment == "high_value"
        assert "high_value" in result.metadata.get("matching_segments", [])

    def test_segment_at_risk_customer(self):
        """Test segmenting an at-risk customer."""
        agent = SegmentationAgent()
        context = CustomerContext(
            customer_id="cust_123",
            behavioral_signals={"days_since_activity": 45},
        )

        result = agent.process(context)

        assert result.segment == "at_risk"

    def test_segment_new_customer(self):
        """Test segmenting a new customer."""
        agent = SegmentationAgent()
        context = CustomerContext(
            customer_id="cust_123",
            attributes={"tenure_days": 10},
        )

        result = agent.process(context)

        assert result.segment == "new_customer"

    def test_segment_default(self):
        """Test default segment assignment."""
        agent = SegmentationAgent()
        context = CustomerContext(
            customer_id="cust_123",
            # Set tenure_days to avoid matching new_customer rule
            attributes={"tenure_days": 100, "lifetime_value": 100},
            behavioral_signals={"days_since_activity": 5, "engagement_score": 50},
        )

        result = agent.process(context)

        assert result.segment == "default"

    def test_add_custom_segment_rule(self):
        """Test adding a custom segment rule."""
        agent = SegmentationAgent()

        agent.add_segment_rule(
            "premium",
            lambda ctx: ctx.attributes.get("subscription_tier") == "premium",
        )

        context = CustomerContext(
            customer_id="cust_123",
            attributes={"subscription_tier": "premium"},
        )

        # Premium should be checked first if added last
        result = agent.process(context)
        assert "premium" in result.metadata.get("matching_segments", [])

    def test_remove_segment_rule(self):
        """Test removing a segment rule."""
        agent = SegmentationAgent()

        assert agent.remove_segment_rule("high_value") is True
        assert agent.remove_segment_rule("nonexistent") is False
        assert "high_value" not in agent.segment_rules

    def test_audit_log_created(self):
        """Test that audit log is created on process."""
        agent = SegmentationAgent()
        context = CustomerContext(customer_id="cust_123")

        agent.process(context)

        audit_log = agent.get_audit_log()
        assert len(audit_log) == 1
        assert audit_log[0]["agent_name"] == "SegmentationAgent"
