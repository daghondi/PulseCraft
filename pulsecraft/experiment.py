"""
Experiment Orchestration for A/B testing and uplift measurement.

Manages experiments, variant assignment, and tracks metrics for measuring uplift.
"""

import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pulsecraft.base import BaseAgent, CustomerContext


def _utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


class ExperimentStatus(Enum):
    """Status of an experiment."""

    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"


@dataclass
class ExperimentVariant:
    """A variant in an experiment."""

    variant_id: str
    name: str
    weight: float = 0.5  # Traffic allocation weight
    content_id: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class Experiment:
    """An A/B experiment configuration."""

    experiment_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    status: ExperimentStatus = ExperimentStatus.DRAFT
    variants: list = field(default_factory=list)
    target_segment: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=_utc_now)
    metadata: dict = field(default_factory=dict)


@dataclass
class ExperimentResult:
    """Result of an experiment assignment."""

    experiment_id: str
    variant_id: str
    variant_name: str
    customer_id: str
    assigned_at: datetime = field(default_factory=_utc_now)
    metadata: dict = field(default_factory=dict)


@dataclass
class ExperimentMetrics:
    """Metrics for an experiment."""

    experiment_id: str
    variant_id: str
    impressions: int = 0
    conversions: int = 0
    total_value: float = 0.0
    conversion_rate: float = 0.0
    average_value: float = 0.0


class ExperimentOrchestrator(BaseAgent):
    """
    Agent responsible for experiment orchestration.

    Manages A/B experiments, handles variant assignment, and tracks
    metrics for measuring uplift.
    """

    def __init__(
        self,
        name: str = "ExperimentOrchestrator",
        random_seed: Optional[int] = None,
    ):
        """
        Initialize the experiment orchestrator.

        Args:
            name: Agent name for audit logging
            random_seed: Optional seed for reproducible random assignment
        """
        super().__init__(name)
        self.experiments: dict[str, Experiment] = {}
        self.assignments: dict[
            str, dict[str, ExperimentResult]
        ] = {}  # customer_id -> experiment_id -> result
        self.metrics: dict[
            str, dict[str, ExperimentMetrics]
        ] = {}  # experiment_id -> variant_id -> metrics

        if random_seed is not None:
            random.seed(random_seed)

    def create_experiment(
        self,
        name: str,
        variants: list[ExperimentVariant],
        target_segment: Optional[str] = None,
        description: str = "",
    ) -> Experiment:
        """
        Create a new experiment.

        Args:
            name: Experiment name
            variants: List of experiment variants
            target_segment: Optional segment to target
            description: Experiment description

        Returns:
            Created Experiment
        """
        experiment = Experiment(
            name=name,
            description=description,
            variants=variants,
            target_segment=target_segment,
        )

        self.experiments[experiment.experiment_id] = experiment

        # Initialize metrics for each variant
        self.metrics[experiment.experiment_id] = {}
        for variant in variants:
            self.metrics[experiment.experiment_id][variant.variant_id] = ExperimentMetrics(
                experiment_id=experiment.experiment_id,
                variant_id=variant.variant_id,
            )

        return experiment

    def start_experiment(self, experiment_id: str) -> bool:
        """
        Start an experiment.

        Args:
            experiment_id: ID of the experiment to start

        Returns:
            True if started, False if experiment not found
        """
        if experiment_id not in self.experiments:
            return False

        experiment = self.experiments[experiment_id]
        experiment.status = ExperimentStatus.RUNNING
        experiment.start_date = _utc_now()
        return True

    def pause_experiment(self, experiment_id: str) -> bool:
        """
        Pause an experiment.

        Args:
            experiment_id: ID of the experiment to pause

        Returns:
            True if paused, False if experiment not found
        """
        if experiment_id not in self.experiments:
            return False

        self.experiments[experiment_id].status = ExperimentStatus.PAUSED
        return True

    def complete_experiment(self, experiment_id: str) -> bool:
        """
        Complete an experiment.

        Args:
            experiment_id: ID of the experiment to complete

        Returns:
            True if completed, False if experiment not found
        """
        if experiment_id not in self.experiments:
            return False

        experiment = self.experiments[experiment_id]
        experiment.status = ExperimentStatus.COMPLETED
        experiment.end_date = _utc_now()
        return True

    def process(
        self,
        context: CustomerContext,
        experiment_id: Optional[str] = None,
    ) -> Optional[ExperimentResult]:
        """
        Assign a customer to an experiment variant.

        Args:
            context: Customer context
            experiment_id: Optional specific experiment ID

        Returns:
            ExperimentResult if assigned, None otherwise
        """
        start_time = time.time()

        # Find applicable experiment
        experiment = None
        if experiment_id:
            experiment = self.experiments.get(experiment_id)
        else:
            # Find first running experiment matching customer segment
            for exp in self.experiments.values():
                if exp.status != ExperimentStatus.RUNNING:
                    continue
                if exp.target_segment is None or exp.target_segment == context.segment:
                    experiment = exp
                    break

        if experiment is None:
            return None

        # Check for existing assignment
        customer_assignments = self.assignments.get(context.customer_id, {})
        if experiment.experiment_id in customer_assignments:
            return customer_assignments[experiment.experiment_id]

        # Assign variant based on weights
        variant = self._select_variant(experiment.variants)

        result = ExperimentResult(
            experiment_id=experiment.experiment_id,
            variant_id=variant.variant_id,
            variant_name=variant.name,
            customer_id=context.customer_id,
        )

        # Store assignment
        if context.customer_id not in self.assignments:
            self.assignments[context.customer_id] = {}
        self.assignments[context.customer_id][experiment.experiment_id] = result

        # Track impression
        self._record_impression(experiment.experiment_id, variant.variant_id)

        # Update context with experiment info
        context.metadata["experiment_id"] = experiment.experiment_id
        context.metadata["variant_id"] = variant.variant_id
        context.metadata["variant_name"] = variant.name

        duration_ms = (time.time() - start_time) * 1000
        self._create_audit_record(
            input_summary=f"customer_id={context.customer_id}, experiment={experiment.name}",
            output_summary=f"variant={variant.name}",
            duration_ms=duration_ms,
            metadata={
                "experiment_id": experiment.experiment_id,
                "variant_id": variant.variant_id,
            },
        )

        return result

    def _select_variant(self, variants: list[ExperimentVariant]) -> ExperimentVariant:
        """
        Select a variant based on weights.

        Args:
            variants: List of variants to select from

        Returns:
            Selected variant
        """
        total_weight = sum(v.weight for v in variants)
        rand = random.random() * total_weight

        cumulative = 0.0
        for variant in variants:
            cumulative += variant.weight
            if rand <= cumulative:
                return variant

        return variants[-1]

    def _record_impression(self, experiment_id: str, variant_id: str) -> None:
        """Record an impression for a variant."""
        if experiment_id in self.metrics and variant_id in self.metrics[experiment_id]:
            self.metrics[experiment_id][variant_id].impressions += 1

    def record_conversion(
        self,
        customer_id: str,
        experiment_id: str,
        value: float = 0.0,
    ) -> bool:
        """
        Record a conversion for an experiment.

        Args:
            customer_id: Customer who converted
            experiment_id: Experiment ID
            value: Conversion value

        Returns:
            True if recorded, False if assignment not found
        """
        customer_assignments = self.assignments.get(customer_id, {})
        if experiment_id not in customer_assignments:
            return False

        result = customer_assignments[experiment_id]
        variant_id = result.variant_id

        if experiment_id in self.metrics and variant_id in self.metrics[experiment_id]:
            metrics = self.metrics[experiment_id][variant_id]
            metrics.conversions += 1
            metrics.total_value += value

            # Update derived metrics
            if metrics.impressions > 0:
                metrics.conversion_rate = metrics.conversions / metrics.impressions
            if metrics.conversions > 0:
                metrics.average_value = metrics.total_value / metrics.conversions

        return True

    def get_experiment_metrics(self, experiment_id: str) -> dict[str, ExperimentMetrics]:
        """
        Get metrics for all variants of an experiment.

        Args:
            experiment_id: Experiment ID

        Returns:
            Dictionary mapping variant_id to ExperimentMetrics
        """
        return self.metrics.get(experiment_id, {})

    def calculate_uplift(self, experiment_id: str, control_variant_id: str) -> dict[str, float]:
        """
        Calculate uplift for each variant compared to control.

        Args:
            experiment_id: Experiment ID
            control_variant_id: ID of the control variant

        Returns:
            Dictionary mapping variant_id to uplift percentage
        """
        metrics = self.get_experiment_metrics(experiment_id)

        if control_variant_id not in metrics:
            return {}

        control_rate = metrics[control_variant_id].conversion_rate

        if control_rate == 0:
            return dict.fromkeys(metrics.keys(), 0.0)

        uplift = {}
        for variant_id, variant_metrics in metrics.items():
            if variant_id == control_variant_id:
                uplift[variant_id] = 0.0
            else:
                uplift[variant_id] = (
                    (variant_metrics.conversion_rate - control_rate) / control_rate * 100
                )

        return uplift

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """
        Get an experiment by ID.

        Args:
            experiment_id: Experiment ID

        Returns:
            Experiment if found, None otherwise
        """
        return self.experiments.get(experiment_id)

    def list_experiments(
        self,
        status: Optional[ExperimentStatus] = None,
    ) -> list[Experiment]:
        """
        List all experiments, optionally filtered by status.

        Args:
            status: Optional status to filter by

        Returns:
            List of experiments
        """
        if status is None:
            return list(self.experiments.values())

        return [exp for exp in self.experiments.values() if exp.status == status]
