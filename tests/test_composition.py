"""
Tests for the message composition module.
"""

from pulsecraft.base import CustomerContext
from pulsecraft.composition import MessageCompositionAgent
from pulsecraft.content import ContentItem


class TestMessageCompositionAgent:
    """Tests for MessageCompositionAgent."""

    def test_agent_initialization(self):
        """Test agent initialization with defaults."""
        agent = MessageCompositionAgent()

        assert agent.name == "MessageCompositionAgent"
        assert "tone" in agent.brand_voice
        assert "formality" in agent.brand_voice
        assert "max_length" in agent.brand_voice

    def test_compose_message_with_content(self):
        """Test composing a message with content template."""
        agent = MessageCompositionAgent()
        context = CustomerContext(
            customer_id="cust_123",
            segment="high_value",
            attributes={"name": "John"},
        )
        content = ContentItem(
            content_id="test_content",
            template="Hello, {customer_name}! Welcome to our service.",
            version="1.0",
        )

        message = agent.process(context, content)

        assert "John" in message.content
        assert message.customer_id == "cust_123"
        assert message.provenance["content_id"] == "test_content"

    def test_compose_message_without_content(self):
        """Test composing a message without content template."""
        agent = MessageCompositionAgent()
        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Jane"},
        )

        message = agent.process(context, None)

        assert "Jane" in message.content
        assert message.provenance["content_source"] == "fallback"

    def test_template_interpolation(self):
        """Test template variable interpolation."""
        agent = MessageCompositionAgent()
        context = CustomerContext(
            customer_id="cust_123",
            segment="premium",
            attributes={"name": "Alice", "city": "New York"},
        )
        content = ContentItem(
            template="Hi {customer_name} from {city}! You're in the {segment} segment.",
        )

        message = agent.process(context, content)

        assert "Alice" in message.content
        assert "New York" in message.content
        assert "premium" in message.content

    def test_brand_voice_max_length(self):
        """Test that brand voice max length is enforced."""
        agent = MessageCompositionAgent(
            brand_voice={"max_length": 50, "tone": "friendly", "formality": "casual"}
        )
        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Bob"},
        )
        content = ContentItem(
            template="This is a very long message that should be truncated because it exceeds the maximum length allowed by the brand voice configuration."
        )

        message = agent.process(context, content)

        assert len(message.content) <= 50

    def test_set_brand_voice(self):
        """Test updating brand voice configuration."""
        agent = MessageCompositionAgent()

        agent.set_brand_voice({"tone": "formal", "max_length": 200})

        assert agent.brand_voice["tone"] == "formal"
        assert agent.brand_voice["max_length"] == 200

    def test_provenance_tracking(self):
        """Test that provenance is tracked in message."""
        agent = MessageCompositionAgent()
        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Test"},
        )
        content = ContentItem(
            content_id="test_id",
            version="2.0",
            template="Hello!",
            provenance={"source": "campaign_manager"},
        )

        message = agent.process(context, content)

        assert message.provenance["content_id"] == "test_id"
        assert message.provenance["content_version"] == "2.0"
        assert message.provenance["content_source"] == "campaign_manager"
        assert "template_vars_used" in message.provenance

    def test_default_customer_name(self):
        """Test default customer name when not provided."""
        agent = MessageCompositionAgent()
        context = CustomerContext(
            customer_id="cust_123",
            attributes={},  # No name provided
        )
        content = ContentItem(
            template="Hello, {customer_name}!",
        )

        message = agent.process(context, content)

        assert "Valued Customer" in message.content

    def test_audit_log_created(self):
        """Test that audit log is created on process."""
        agent = MessageCompositionAgent()
        context = CustomerContext(customer_id="cust_123")

        agent.process(context, None)

        audit_log = agent.get_audit_log()
        assert len(audit_log) == 1
        assert audit_log[0]["agent_name"] == "MessageCompositionAgent"
