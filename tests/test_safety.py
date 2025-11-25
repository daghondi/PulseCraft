"""
Tests for the safety check module.
"""

from pulsecraft.base import Message
from pulsecraft.safety import SafetyCheckAgent, SafetyCheckResult


class TestSafetyCheckAgent:
    """Tests for SafetyCheckAgent."""

    def test_agent_initialization(self):
        """Test agent initialization with defaults."""
        agent = SafetyCheckAgent()

        assert agent.name == "SafetyCheckAgent"
        assert len(agent.safety_checks) > 0
        assert len(agent.blocked_patterns) > 0

    def test_safe_message_passes(self):
        """Test that a safe message passes all checks."""
        agent = SafetyCheckAgent()
        message = Message(
            content="Hello John, thank you for being a valued member of our community!",
            customer_id="cust_123",
        )

        report = agent.process(message)

        assert report.is_safe_to_send is True
        assert report.overall_result == SafetyCheckResult.PASS

    def test_empty_message_fails(self):
        """Test that an empty message fails."""
        agent = SafetyCheckAgent()
        message = Message(content="")

        report = agent.process(message)

        assert report.is_safe_to_send is False
        assert report.overall_result == SafetyCheckResult.FAIL
        assert len(report.checks_failed) > 0

    def test_blocked_pattern_fails(self):
        """Test that blocked patterns cause failure."""
        agent = SafetyCheckAgent()
        message = Message(
            content="This offer is guaranteed to make you rich! Act now!",
        )

        report = agent.process(message)

        assert report.is_safe_to_send is False
        assert report.overall_result == SafetyCheckResult.FAIL

    def test_unresolved_placeholders_fail(self):
        """Test that unresolved placeholders cause failure."""
        agent = SafetyCheckAgent()
        message = Message(
            content="Hello {customer_name}, welcome to our service!",
        )

        report = agent.process(message)

        assert report.is_safe_to_send is False
        assert any("unresolved" in check["detail"].lower() for check in report.checks_failed)

    def test_generic_personalization_warns(self):
        """Test that generic personalization causes warning."""
        agent = SafetyCheckAgent()
        message = Message(
            content="Dear Customer, thank you for your interest.",
        )

        report = agent.process(message)

        # Should warn but not fail
        assert report.is_safe_to_send is True
        assert len(report.checks_warned) > 0

    def test_add_custom_safety_check(self):
        """Test adding a custom safety check."""
        agent = SafetyCheckAgent()

        def custom_check(msg):
            if "spam" in msg.content.lower():
                return SafetyCheckResult.FAIL, "Contains spam keyword"
            return SafetyCheckResult.PASS, "No spam detected"

        agent.add_safety_check("spam_check", custom_check)

        message = Message(content="This is spam content")
        report = agent.process(message)

        assert report.is_safe_to_send is False
        assert any("spam" in check["detail"].lower() for check in report.checks_failed)

    def test_remove_safety_check(self):
        """Test removing a safety check."""
        agent = SafetyCheckAgent()

        assert agent.remove_safety_check("content_length") is True
        assert agent.remove_safety_check("nonexistent") is False
        assert "content_length" not in agent.safety_checks

    def test_add_blocked_pattern(self):
        """Test adding a blocked pattern."""
        agent = SafetyCheckAgent()
        agent.add_blocked_pattern(r"(?i)\btest_block\b")

        message = Message(content="This contains test_block word")
        report = agent.process(message)

        assert report.is_safe_to_send is False

    def test_remove_blocked_pattern(self):
        """Test removing a blocked pattern."""
        agent = SafetyCheckAgent()
        pattern = r"(?i)\b(guarantee|guaranteed)\b"

        assert agent.remove_blocked_pattern(pattern) is True
        assert agent.remove_blocked_pattern("nonexistent") is False

    def test_message_safety_checks_updated(self):
        """Test that message.safety_checks is updated."""
        agent = SafetyCheckAgent()
        message = Message(
            content="Hello John, welcome to our service!",
        )

        agent.process(message)

        assert "overall_result" in message.safety_checks
        assert "is_safe_to_send" in message.safety_checks

    def test_audit_log_created(self):
        """Test that audit log is created on process."""
        agent = SafetyCheckAgent()
        message = Message(content="Test message content")

        agent.process(message)

        audit_log = agent.get_audit_log()
        assert len(audit_log) == 1
        assert audit_log[0]["agent_name"] == "SafetyCheckAgent"
