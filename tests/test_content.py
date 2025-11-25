"""
Tests for the content retrieval module.
"""

from pulsecraft.base import CustomerContext
from pulsecraft.content import ContentItem, ContentRetrievalAgent


class TestContentItem:
    """Tests for ContentItem dataclass."""

    def test_content_item_creation(self):
        """Test creating a content item."""
        item = ContentItem(
            template="Hello, {customer_name}!",
            content_type="greeting",
        )

        assert item.template == "Hello, {customer_name}!"
        assert item.content_type == "greeting"
        assert item.content_id is not None

    def test_content_item_with_provenance(self):
        """Test creating a content item with provenance."""
        item = ContentItem(
            template="Test template",
            provenance={"source": "marketing", "author": "admin"},
        )

        assert item.provenance["source"] == "marketing"
        assert item.provenance["author"] == "admin"


class TestContentRetrievalAgent:
    """Tests for ContentRetrievalAgent."""

    def test_agent_initialization(self):
        """Test agent initialization with defaults."""
        agent = ContentRetrievalAgent()

        assert agent.name == "ContentRetrievalAgent"
        assert len(agent.content_library) > 0

    def test_retrieve_content_for_segment(self):
        """Test retrieving content for a specific segment."""
        agent = ContentRetrievalAgent()
        context = CustomerContext(
            customer_id="cust_123",
            segment="high_value",
        )

        context, content = agent.process(context)

        assert content is not None
        assert "high_value" in content.segment_targeting

    def test_retrieve_content_for_new_customer(self):
        """Test retrieving content for new customer segment."""
        agent = ContentRetrievalAgent()
        context = CustomerContext(
            customer_id="cust_123",
            segment="new_customer",
        )

        context, content = agent.process(context)

        assert content is not None
        assert "new_customer" in content.segment_targeting

    def test_retrieve_default_content(self):
        """Test retrieving default content when no segment match."""
        agent = ContentRetrievalAgent()
        context = CustomerContext(
            customer_id="cust_123",
            segment="unknown_segment",
        )

        context, content = agent.process(context)

        assert content is not None
        assert content.content_id == "default_message"

    def test_add_custom_content(self):
        """Test adding custom content."""
        agent = ContentRetrievalAgent()
        custom_content = ContentItem(
            content_id="custom_promo",
            template="Special offer for you!",
            segment_targeting=["vip"],
        )

        content_id = agent.add_content(custom_content)

        assert content_id == "custom_promo"
        assert agent.get_content("custom_promo") is not None

    def test_remove_content(self):
        """Test removing content."""
        agent = ContentRetrievalAgent()

        # Add then remove
        custom_content = ContentItem(
            content_id="to_remove",
            template="Test",
        )
        agent.add_content(custom_content)

        assert agent.remove_content("to_remove") is True
        assert agent.remove_content("nonexistent") is False
        assert agent.get_content("to_remove") is None

    def test_list_content(self):
        """Test listing all content."""
        agent = ContentRetrievalAgent()

        all_content = agent.list_content()
        assert len(all_content) >= 4  # Default content

        segment_content = agent.list_content(segment="high_value")
        assert len(segment_content) >= 1

    def test_provenance_tracking(self):
        """Test that provenance is tracked in context."""
        agent = ContentRetrievalAgent()
        context = CustomerContext(
            customer_id="cust_123",
            segment="high_value",
        )

        context, content = agent.process(context)

        assert "content_provenance" in context.metadata
        assert context.metadata["selected_content_id"] is not None

    def test_audit_log_created(self):
        """Test that audit log is created on process."""
        agent = ContentRetrievalAgent()
        context = CustomerContext(customer_id="cust_123")

        agent.process(context)

        audit_log = agent.get_audit_log()
        assert len(audit_log) == 1
        assert audit_log[0]["agent_name"] == "ContentRetrievalAgent"
