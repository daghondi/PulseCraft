"""
Message Composition Agent for generative message creation.

Composes personalized messages by combining templates with customer data.
"""

import re
import time
from typing import Optional

from pulsecraft.base import BaseAgent, CustomerContext, Message
from pulsecraft.content import ContentItem


class MessageCompositionAgent(BaseAgent):
    """
    Agent responsible for composing personalized messages.

    Combines content templates with customer context to generate personalized
    messages with full provenance tracking.
    """

    def __init__(
        self,
        name: str = "MessageCompositionAgent",
        brand_voice: Optional[dict] = None,
    ):
        """
        Initialize the message composition agent.

        Args:
            name: Agent name for audit logging
            brand_voice: Brand voice configuration for message styling
        """
        super().__init__(name)
        self.brand_voice = brand_voice or {
            "tone": "friendly",
            "formality": "casual",
            "max_length": 500,
        }

    def process(
        self,
        context: CustomerContext,
        content: Optional[ContentItem] = None,
    ) -> Message:
        """
        Compose a personalized message for the customer.

        Args:
            context: Customer context with attributes and signals
            content: Content template to use for composition

        Returns:
            Composed Message with provenance tracking
        """
        start_time = time.time()

        # Extract customer attributes for personalization
        customer_name = context.attributes.get("name", "Valued Customer")

        # Prepare template variables
        template_vars = {
            "customer_name": customer_name,
            "customer_id": context.customer_id,
            "segment": context.segment or "default",
            **context.attributes,
        }

        # Compose message content
        if content:
            message_content = self._interpolate_template(content.template, template_vars)
            provenance = {
                "content_id": content.content_id,
                "content_version": content.version,
                "content_source": content.provenance.get("source", "unknown"),
                "template_vars_used": list(template_vars.keys()),
                "composition_timestamp": time.time(),
            }
            channel = content.channel
        else:
            message_content = f"Hi {customer_name}, thank you for being a valued customer!"
            provenance = {
                "content_id": None,
                "content_source": "fallback",
                "composition_timestamp": time.time(),
            }
            channel = "email"

        # Apply brand voice constraints
        message_content = self._apply_brand_voice(message_content)

        # Create message object
        message = Message(
            content=message_content,
            channel=channel,
            customer_id=context.customer_id,
            provenance=provenance,
            metadata={
                "segment": context.segment,
                "brand_voice": self.brand_voice,
            },
        )

        duration_ms = (time.time() - start_time) * 1000
        self._create_audit_record(
            input_summary=f"customer_id={context.customer_id}, content_id={content.content_id if content else 'none'}",
            output_summary=f"message_id={message.message_id}, length={len(message_content)}",
            duration_ms=duration_ms,
            metadata={
                "message_id": message.message_id,
                "channel": channel,
                "content_length": len(message_content),
            },
        )

        return message

    def _interpolate_template(self, template: str, variables: dict) -> str:
        """
        Interpolate template with variables.

        Args:
            template: Template string with {variable} placeholders
            variables: Dictionary of variable values

        Returns:
            Interpolated string
        """
        result = template

        # Find all placeholders in the template
        placeholders = re.findall(r"\{(\w+)\}", template)

        for placeholder in placeholders:
            if placeholder in variables:
                value = variables[placeholder]
                result = result.replace(f"{{{placeholder}}}", str(value))

        return result

    def _apply_brand_voice(self, content: str) -> str:
        """
        Apply brand voice constraints to content.

        Args:
            content: Original content

        Returns:
            Content adjusted for brand voice
        """
        max_length = self.brand_voice.get("max_length", 500)

        if len(content) > max_length:
            content = content[: max_length - 3] + "..."

        return content

    def set_brand_voice(self, config: dict) -> None:
        """
        Update brand voice configuration.

        Args:
            config: New brand voice configuration
        """
        self.brand_voice.update(config)
