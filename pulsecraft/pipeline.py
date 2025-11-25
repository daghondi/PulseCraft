"""
Pipeline orchestrator for PulseCraft.

Links segmentation, signal scoring, content retrieval, message composition,
safety checks, and experiment orchestration into a reproducible pipeline.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pulsecraft.base import CustomerContext, Message
from pulsecraft.composition import MessageCompositionAgent
from pulsecraft.content import ContentRetrievalAgent
from pulsecraft.experiment import ExperimentOrchestrator
from pulsecraft.safety import SafetyCheckAgent, SafetyCheckReport
from pulsecraft.segmentation import SegmentationAgent
from pulsecraft.signals import SignalScoringAgent


def _utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class PipelineResult:
    """Result of a pipeline execution."""

    pipeline_id: str = field(default_factory=lambda: str(uuid4()))
    customer_id: str = ""
    message: Optional[Message] = None
    safety_report: Optional[SafetyCheckReport] = None
    is_success: bool = False
    is_safe_to_send: bool = False
    experiment_variant: Optional[str] = None
    segment: Optional[str] = None
    propensity_scores: dict = field(default_factory=dict)
    audit_trail: list = field(default_factory=list)
    execution_time_ms: float = 0.0
    created_at: datetime = field(default_factory=_utc_now)
    error: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "pipeline_id": self.pipeline_id,
            "customer_id": self.customer_id,
            "is_success": self.is_success,
            "is_safe_to_send": self.is_safe_to_send,
            "message_id": self.message.message_id if self.message else None,
            "message_content": self.message.content if self.message else None,
            "segment": self.segment,
            "experiment_variant": self.experiment_variant,
            "propensity_scores": self.propensity_scores,
            "execution_time_ms": self.execution_time_ms,
            "created_at": self.created_at.isoformat(),
            "error": self.error,
        }


class Pipeline:
    """
    Main pipeline orchestrator for PulseCraft.

    Links all agents together in a reproducible, auditable pipeline for
    personalized customer messaging.
    """

    def __init__(
        self,
        segmentation_agent: Optional[SegmentationAgent] = None,
        signal_scoring_agent: Optional[SignalScoringAgent] = None,
        content_retrieval_agent: Optional[ContentRetrievalAgent] = None,
        message_composition_agent: Optional[MessageCompositionAgent] = None,
        safety_check_agent: Optional[SafetyCheckAgent] = None,
        experiment_orchestrator: Optional[ExperimentOrchestrator] = None,
    ):
        """
        Initialize the pipeline with agents.

        Args:
            segmentation_agent: Agent for customer segmentation
            signal_scoring_agent: Agent for behavioral signal scoring
            content_retrieval_agent: Agent for content retrieval
            message_composition_agent: Agent for message composition
            safety_check_agent: Agent for safety validation
            experiment_orchestrator: Agent for experiment orchestration
        """
        self.segmentation_agent = segmentation_agent or SegmentationAgent()
        self.signal_scoring_agent = signal_scoring_agent or SignalScoringAgent()
        self.content_retrieval_agent = content_retrieval_agent or ContentRetrievalAgent()
        self.message_composition_agent = message_composition_agent or MessageCompositionAgent()
        self.safety_check_agent = safety_check_agent or SafetyCheckAgent()
        self.experiment_orchestrator = experiment_orchestrator or ExperimentOrchestrator()

        self.execution_history: list[PipelineResult] = []

    def execute(
        self,
        customer_context: CustomerContext,
        experiment_id: Optional[str] = None,
        skip_safety_check: bool = False,
    ) -> PipelineResult:
        """
        Execute the full pipeline for a customer.

        Args:
            customer_context: Customer context with attributes and signals
            experiment_id: Optional experiment ID to use
            skip_safety_check: Whether to skip safety validation

        Returns:
            PipelineResult with message and audit trail
        """
        start_time = time.time()
        result = PipelineResult(customer_id=customer_context.customer_id)
        audit_trail = []

        try:
            # Step 1: Segmentation
            customer_context = self.segmentation_agent.process(customer_context)
            result.segment = customer_context.segment
            audit_trail.extend(self.segmentation_agent.get_audit_log())
            self.segmentation_agent.clear_audit_log()

            # Step 2: Signal Scoring
            customer_context = self.signal_scoring_agent.process(customer_context)
            result.propensity_scores = customer_context.propensity_scores.copy()
            audit_trail.extend(self.signal_scoring_agent.get_audit_log())
            self.signal_scoring_agent.clear_audit_log()

            # Step 3: Experiment Assignment (if applicable)
            exp_result = self.experiment_orchestrator.process(
                customer_context,
                experiment_id=experiment_id,
            )
            if exp_result:
                result.experiment_variant = exp_result.variant_name
            audit_trail.extend(self.experiment_orchestrator.get_audit_log())
            self.experiment_orchestrator.clear_audit_log()

            # Step 4: Content Retrieval
            customer_context, content = self.content_retrieval_agent.process(customer_context)
            audit_trail.extend(self.content_retrieval_agent.get_audit_log())
            self.content_retrieval_agent.clear_audit_log()

            # Step 5: Message Composition
            message = self.message_composition_agent.process(customer_context, content)
            result.message = message
            audit_trail.extend(self.message_composition_agent.get_audit_log())
            self.message_composition_agent.clear_audit_log()

            # Step 6: Safety Check
            if not skip_safety_check:
                safety_report = self.safety_check_agent.process(message)
                result.safety_report = safety_report
                result.is_safe_to_send = safety_report.is_safe_to_send
                audit_trail.extend(self.safety_check_agent.get_audit_log())
                self.safety_check_agent.clear_audit_log()
            else:
                result.is_safe_to_send = True

            result.is_success = True

        except Exception as e:
            result.is_success = False
            result.error = str(e)

        result.execution_time_ms = (time.time() - start_time) * 1000
        result.audit_trail = audit_trail

        # Store in history
        self.execution_history.append(result)

        return result

    def execute_batch(
        self,
        customer_contexts: list[CustomerContext],
        experiment_id: Optional[str] = None,
        skip_safety_check: bool = False,
    ) -> list[PipelineResult]:
        """
        Execute the pipeline for multiple customers.

        Args:
            customer_contexts: List of customer contexts
            experiment_id: Optional experiment ID to use
            skip_safety_check: Whether to skip safety validation

        Returns:
            List of PipelineResults
        """
        results = []
        for context in customer_contexts:
            result = self.execute(
                context,
                experiment_id=experiment_id,
                skip_safety_check=skip_safety_check,
            )
            results.append(result)
        return results

    def get_execution_history(self) -> list[PipelineResult]:
        """
        Get all pipeline execution results.

        Returns:
            List of PipelineResults
        """
        return self.execution_history

    def clear_execution_history(self) -> None:
        """Clear execution history."""
        self.execution_history = []

    def get_audit_trail(self, pipeline_id: str) -> list[dict]:
        """
        Get audit trail for a specific pipeline execution.

        Args:
            pipeline_id: Pipeline execution ID

        Returns:
            List of audit records
        """
        for result in self.execution_history:
            if result.pipeline_id == pipeline_id:
                return result.audit_trail
        return []

    def get_pipeline_stats(self) -> dict:
        """
        Get statistics about pipeline executions.

        Returns:
            Dictionary with execution statistics
        """
        if not self.execution_history:
            return {
                "total_executions": 0,
                "success_rate": 0.0,
                "safe_to_send_rate": 0.0,
                "average_execution_time_ms": 0.0,
            }

        total = len(self.execution_history)
        successful = sum(1 for r in self.execution_history if r.is_success)
        safe_to_send = sum(1 for r in self.execution_history if r.is_safe_to_send)
        total_time = sum(r.execution_time_ms for r in self.execution_history)

        return {
            "total_executions": total,
            "success_rate": successful / total,
            "safe_to_send_rate": safe_to_send / total,
            "average_execution_time_ms": total_time / total,
        }
