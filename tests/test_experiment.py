"""
Tests for the experiment orchestration module.
"""

import pytest

from pulsecraft.base import CustomerContext
from pulsecraft.experiment import (
    ExperimentOrchestrator,
    ExperimentStatus,
    ExperimentVariant,
)


class TestExperimentOrchestrator:
    """Tests for ExperimentOrchestrator."""

    def test_agent_initialization(self):
        """Test agent initialization."""
        orchestrator = ExperimentOrchestrator()

        assert orchestrator.name == "ExperimentOrchestrator"
        assert len(orchestrator.experiments) == 0

    def test_create_experiment(self):
        """Test creating an experiment."""
        orchestrator = ExperimentOrchestrator()

        variants = [
            ExperimentVariant(variant_id="control", name="Control", weight=0.5),
            ExperimentVariant(variant_id="treatment", name="Treatment", weight=0.5),
        ]

        experiment = orchestrator.create_experiment(
            name="Test Experiment",
            variants=variants,
            description="A test experiment",
        )

        assert experiment.name == "Test Experiment"
        assert experiment.status == ExperimentStatus.DRAFT
        assert len(experiment.variants) == 2
        assert experiment.experiment_id in orchestrator.experiments

    def test_start_experiment(self):
        """Test starting an experiment."""
        orchestrator = ExperimentOrchestrator()
        variants = [
            ExperimentVariant(variant_id="control", name="Control"),
        ]
        experiment = orchestrator.create_experiment("Test", variants)

        result = orchestrator.start_experiment(experiment.experiment_id)

        assert result is True
        assert orchestrator.experiments[experiment.experiment_id].status == ExperimentStatus.RUNNING

    def test_pause_experiment(self):
        """Test pausing an experiment."""
        orchestrator = ExperimentOrchestrator()
        variants = [ExperimentVariant(variant_id="control", name="Control")]
        experiment = orchestrator.create_experiment("Test", variants)
        orchestrator.start_experiment(experiment.experiment_id)

        result = orchestrator.pause_experiment(experiment.experiment_id)

        assert result is True
        assert orchestrator.experiments[experiment.experiment_id].status == ExperimentStatus.PAUSED

    def test_complete_experiment(self):
        """Test completing an experiment."""
        orchestrator = ExperimentOrchestrator()
        variants = [ExperimentVariant(variant_id="control", name="Control")]
        experiment = orchestrator.create_experiment("Test", variants)

        result = orchestrator.complete_experiment(experiment.experiment_id)

        assert result is True
        assert (
            orchestrator.experiments[experiment.experiment_id].status == ExperimentStatus.COMPLETED
        )

    def test_variant_assignment(self):
        """Test assigning a customer to a variant."""
        orchestrator = ExperimentOrchestrator(random_seed=42)
        variants = [
            ExperimentVariant(variant_id="control", name="Control", weight=0.5),
            ExperimentVariant(variant_id="treatment", name="Treatment", weight=0.5),
        ]
        experiment = orchestrator.create_experiment("Test", variants)
        orchestrator.start_experiment(experiment.experiment_id)

        context = CustomerContext(customer_id="cust_123")
        result = orchestrator.process(context, experiment.experiment_id)

        assert result is not None
        assert result.customer_id == "cust_123"
        assert result.variant_id in ["control", "treatment"]

    def test_consistent_assignment(self):
        """Test that the same customer gets the same variant."""
        orchestrator = ExperimentOrchestrator(random_seed=42)
        variants = [
            ExperimentVariant(variant_id="control", name="Control", weight=0.5),
            ExperimentVariant(variant_id="treatment", name="Treatment", weight=0.5),
        ]
        experiment = orchestrator.create_experiment("Test", variants)
        orchestrator.start_experiment(experiment.experiment_id)

        context = CustomerContext(customer_id="cust_123")

        result1 = orchestrator.process(context, experiment.experiment_id)
        result2 = orchestrator.process(context, experiment.experiment_id)

        # Same customer should get same assignment
        assert result1.variant_id == result2.variant_id

    def test_segment_targeting(self):
        """Test that experiments respect segment targeting."""
        orchestrator = ExperimentOrchestrator()
        variants = [ExperimentVariant(variant_id="control", name="Control")]
        experiment = orchestrator.create_experiment(
            "Test",
            variants,
            target_segment="high_value",
        )
        orchestrator.start_experiment(experiment.experiment_id)

        # Customer not in target segment
        context = CustomerContext(customer_id="cust_123", segment="low_value")
        result = orchestrator.process(context)

        assert result is None

    def test_record_conversion(self):
        """Test recording a conversion."""
        orchestrator = ExperimentOrchestrator(random_seed=42)
        variants = [
            ExperimentVariant(variant_id="control", name="Control", weight=1.0),
        ]
        experiment = orchestrator.create_experiment("Test", variants)
        orchestrator.start_experiment(experiment.experiment_id)

        context = CustomerContext(customer_id="cust_123")
        orchestrator.process(context, experiment.experiment_id)

        result = orchestrator.record_conversion(
            "cust_123",
            experiment.experiment_id,
            value=100.0,
        )

        assert result is True

        metrics = orchestrator.get_experiment_metrics(experiment.experiment_id)
        assert metrics["control"].conversions == 1
        assert metrics["control"].total_value == 100.0

    def test_calculate_uplift(self):
        """Test calculating uplift."""
        orchestrator = ExperimentOrchestrator()
        variants = [
            ExperimentVariant(variant_id="control", name="Control"),
            ExperimentVariant(variant_id="treatment", name="Treatment"),
        ]
        experiment = orchestrator.create_experiment("Test", variants)

        # Manually set some metrics
        metrics = orchestrator.metrics[experiment.experiment_id]
        metrics["control"].impressions = 100
        metrics["control"].conversions = 10
        metrics["control"].conversion_rate = 0.10
        metrics["treatment"].impressions = 100
        metrics["treatment"].conversions = 15
        metrics["treatment"].conversion_rate = 0.15

        uplift = orchestrator.calculate_uplift(experiment.experiment_id, "control")

        assert uplift["control"] == 0.0
        assert uplift["treatment"] == pytest.approx(50.0)  # 50% uplift

    def test_list_experiments(self):
        """Test listing experiments."""
        orchestrator = ExperimentOrchestrator()
        variants = [ExperimentVariant(variant_id="control", name="Control")]

        orchestrator.create_experiment("Test1", variants)
        exp2 = orchestrator.create_experiment("Test2", variants)
        orchestrator.start_experiment(exp2.experiment_id)

        all_experiments = orchestrator.list_experiments()
        running_experiments = orchestrator.list_experiments(status=ExperimentStatus.RUNNING)

        assert len(all_experiments) == 2
        assert len(running_experiments) == 1

    def test_get_experiment(self):
        """Test getting an experiment by ID."""
        orchestrator = ExperimentOrchestrator()
        variants = [ExperimentVariant(variant_id="control", name="Control")]
        experiment = orchestrator.create_experiment("Test", variants)

        retrieved = orchestrator.get_experiment(experiment.experiment_id)

        assert retrieved is not None
        assert retrieved.name == "Test"

    def test_audit_log_created(self):
        """Test that audit log is created on process."""
        orchestrator = ExperimentOrchestrator()
        variants = [ExperimentVariant(variant_id="control", name="Control")]
        experiment = orchestrator.create_experiment("Test", variants)
        orchestrator.start_experiment(experiment.experiment_id)

        context = CustomerContext(customer_id="cust_123")
        orchestrator.process(context, experiment.experiment_id)

        audit_log = orchestrator.get_audit_log()
        assert len(audit_log) == 1
        assert audit_log[0]["agent_name"] == "ExperimentOrchestrator"
