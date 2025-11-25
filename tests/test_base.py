"""
Tests for the base module.
"""

from pulsecraft.base import AuditRecord, CustomerContext, Message


class TestAuditRecord:
    """Tests for AuditRecord dataclass."""

    def test_audit_record_creation(self):
        """Test creating an audit record with default values."""
        record = AuditRecord(agent_name="TestAgent")

        assert record.agent_name == "TestAgent"
        assert record.trace_id is not None
        assert record.timestamp is not None

    def test_audit_record_to_dict(self):
        """Test converting audit record to dictionary."""
        record = AuditRecord(
            agent_name="TestAgent",
            input_summary="test input",
            output_summary="test output",
            duration_ms=10.5,
            metadata={"key": "value"},
        )

        result = record.to_dict()

        assert result["agent_name"] == "TestAgent"
        assert result["input_summary"] == "test input"
        assert result["output_summary"] == "test output"
        assert result["duration_ms"] == 10.5
        assert result["metadata"] == {"key": "value"}


class TestCustomerContext:
    """Tests for CustomerContext dataclass."""

    def test_customer_context_creation(self):
        """Test creating a customer context."""
        context = CustomerContext(customer_id="cust_123")

        assert context.customer_id == "cust_123"
        assert context.segment is None
        assert context.attributes == {}
        assert context.behavioral_signals == {}
        assert context.propensity_scores == {}

    def test_customer_context_with_data(self):
        """Test creating a customer context with data."""
        context = CustomerContext(
            customer_id="cust_123",
            segment="high_value",
            attributes={"name": "John"},
            behavioral_signals={"clicks": 10},
        )

        assert context.customer_id == "cust_123"
        assert context.segment == "high_value"
        assert context.attributes["name"] == "John"
        assert context.behavioral_signals["clicks"] == 10


class TestMessage:
    """Tests for Message dataclass."""

    def test_message_creation(self):
        """Test creating a message."""
        message = Message(content="Hello, World!")

        assert message.content == "Hello, World!"
        assert message.message_id is not None
        assert message.channel == "email"

    def test_message_with_all_fields(self):
        """Test creating a message with all fields."""
        message = Message(
            content="Test content",
            subject="Test Subject",
            channel="sms",
            customer_id="cust_123",
            provenance={"source": "test"},
        )

        assert message.content == "Test content"
        assert message.subject == "Test Subject"
        assert message.channel == "sms"
        assert message.customer_id == "cust_123"
        assert message.provenance == {"source": "test"}
