"""
Base classes and interfaces for PulseCraft agents.

Provides foundational abstractions for building reproducible, auditable pipelines.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4


def _utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class AuditRecord:
    """Record of an agent execution for auditability and explainability."""

    agent_name: str
    timestamp: datetime = field(default_factory=_utc_now)
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    input_summary: Optional[str] = None
    output_summary: Optional[str] = None
    duration_ms: Optional[float] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "agent_name": self.agent_name,
            "timestamp": self.timestamp.isoformat(),
            "trace_id": self.trace_id,
            "input_summary": self.input_summary,
            "output_summary": self.output_summary,
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
        }


@dataclass
class CustomerContext:
    """Customer context containing behavioral signals and attributes."""

    customer_id: str
    segment: Optional[str] = None
    attributes: dict = field(default_factory=dict)
    behavioral_signals: dict = field(default_factory=dict)
    propensity_scores: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)


@dataclass
class Message:
    """Composed message with content provenance tracking."""

    message_id: str = field(default_factory=lambda: str(uuid4()))
    content: str = ""
    subject: Optional[str] = None
    channel: str = "email"
    customer_id: Optional[str] = None
    provenance: dict = field(default_factory=dict)
    safety_checks: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)


class BaseAgent(ABC):
    """
    Abstract base class for all PulseCraft agents.

    Provides common functionality for auditability and tracing.
    """

    def __init__(self, name: str):
        self.name = name
        self.audit_log: list[AuditRecord] = []

    @abstractmethod
    def process(self, context: Any) -> Any:
        """Process input and return output. Must be implemented by subclasses."""
        pass

    def _create_audit_record(
        self,
        input_summary: Optional[str] = None,
        output_summary: Optional[str] = None,
        duration_ms: Optional[float] = None,
        metadata: Optional[dict] = None,
    ) -> AuditRecord:
        """Create and store an audit record."""
        record = AuditRecord(
            agent_name=self.name,
            input_summary=input_summary,
            output_summary=output_summary,
            duration_ms=duration_ms,
            metadata=metadata or {},
        )
        self.audit_log.append(record)
        return record

    def get_audit_log(self) -> list[dict]:
        """Get all audit records as dictionaries."""
        return [record.to_dict() for record in self.audit_log]

    def clear_audit_log(self) -> None:
        """Clear all audit records."""
        self.audit_log = []
