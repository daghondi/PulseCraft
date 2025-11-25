"""
Content Retrieval Agent for fetching content with provenance tracking.

Retrieves and manages content templates with full provenance information.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pulsecraft.base import BaseAgent, CustomerContext


def _utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class ContentItem:
    """Content item with provenance information."""

    content_id: str = field(default_factory=lambda: str(uuid4()))
    template: str = ""
    content_type: str = "text"
    channel: str = "email"
    segment_targeting: list = field(default_factory=list)
    provenance: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)
    version: str = "1.0"


class ContentRetrievalAgent(BaseAgent):
    """
    Agent responsible for retrieving content with provenance tracking.

    Maintains a content library and retrieves appropriate content based on
    customer segment and context, with full provenance information.
    """

    def __init__(
        self,
        name: str = "ContentRetrievalAgent",
        content_library: Optional[dict[str, ContentItem]] = None,
    ):
        """
        Initialize the content retrieval agent.

        Args:
            name: Agent name for audit logging
            content_library: Initial content library mapping IDs to ContentItems
        """
        super().__init__(name)
        self.content_library: dict[str, ContentItem] = content_library or {}
        self._initialize_default_content()

    def _initialize_default_content(self) -> None:
        """Initialize default content templates."""
        default_content = [
            ContentItem(
                content_id="welcome_new",
                template="Welcome to our family, {customer_name}! We're excited to have you.",
                content_type="greeting",
                channel="email",
                segment_targeting=["new_customer"],
                provenance={"source": "default_library", "author": "system"},
            ),
            ContentItem(
                content_id="engagement_boost",
                template="Hi {customer_name}, we miss you! Check out what's new.",
                content_type="re-engagement",
                channel="email",
                segment_targeting=["at_risk"],
                provenance={"source": "default_library", "author": "system"},
            ),
            ContentItem(
                content_id="vip_offer",
                template="As a valued customer, {customer_name}, enjoy this exclusive offer.",
                content_type="promotion",
                channel="email",
                segment_targeting=["high_value"],
                provenance={"source": "default_library", "author": "system"},
            ),
            ContentItem(
                content_id="default_message",
                template="Hi {customer_name}, thanks for being with us!",
                content_type="general",
                channel="email",
                segment_targeting=["default"],
                provenance={"source": "default_library", "author": "system"},
            ),
        ]

        for item in default_content:
            if item.content_id not in self.content_library:
                self.content_library[item.content_id] = item

    def process(self, context: CustomerContext) -> tuple[CustomerContext, Optional[ContentItem]]:
        """
        Retrieve appropriate content for the customer.

        Args:
            context: Customer context with segment information

        Returns:
            Tuple of (updated context, retrieved ContentItem or None)
        """
        start_time = time.time()

        segment = context.segment or "default"
        selected_content = None

        # Find content matching the segment
        for content_item in self.content_library.values():
            if segment in content_item.segment_targeting:
                selected_content = content_item
                break

        # Fall back to default content
        if selected_content is None:
            selected_content = self.content_library.get("default_message")

        if selected_content:
            context.metadata["selected_content_id"] = selected_content.content_id
            context.metadata["content_provenance"] = selected_content.provenance

        duration_ms = (time.time() - start_time) * 1000
        self._create_audit_record(
            input_summary=f"customer_id={context.customer_id}, segment={segment}",
            output_summary=f"content_id={selected_content.content_id if selected_content else 'none'}",
            duration_ms=duration_ms,
            metadata={
                "segment": segment,
                "content_id": selected_content.content_id if selected_content else None,
            },
        )

        return context, selected_content

    def add_content(self, content: ContentItem) -> str:
        """
        Add content to the library.

        Args:
            content: ContentItem to add

        Returns:
            Content ID of the added item
        """
        self.content_library[content.content_id] = content
        return content.content_id

    def get_content(self, content_id: str) -> Optional[ContentItem]:
        """
        Get content by ID.

        Args:
            content_id: ID of the content to retrieve

        Returns:
            ContentItem if found, None otherwise
        """
        return self.content_library.get(content_id)

    def remove_content(self, content_id: str) -> bool:
        """
        Remove content from the library.

        Args:
            content_id: ID of the content to remove

        Returns:
            True if content was removed, False if it didn't exist
        """
        if content_id in self.content_library:
            del self.content_library[content_id]
            return True
        return False

    def list_content(self, segment: Optional[str] = None) -> list[ContentItem]:
        """
        List all content, optionally filtered by segment.

        Args:
            segment: Optional segment to filter by

        Returns:
            List of ContentItems
        """
        if segment is None:
            return list(self.content_library.values())

        return [item for item in self.content_library.values() if segment in item.segment_targeting]
