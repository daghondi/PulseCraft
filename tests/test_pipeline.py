"""
Tests for the pipeline module.
"""

from pulsecraft.base import CustomerContext
from pulsecraft.experiment import ExperimentVariant
from pulsecraft.pipeline import Pipeline


class TestPipeline:
    """Tests for Pipeline orchestrator."""

    def test_pipeline_initialization(self):
        """Test pipeline initialization with default agents."""
        pipeline = Pipeline()

        assert pipeline.segmentation_agent is not None
        assert pipeline.signal_scoring_agent is not None
        assert pipeline.content_retrieval_agent is not None
        assert pipeline.message_composition_agent is not None
        assert pipeline.safety_check_agent is not None
        assert pipeline.experiment_orchestrator is not None

    def test_pipeline_execution(self):
        """Test full pipeline execution."""
        pipeline = Pipeline()

        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "John", "lifetime_value": 1500},
            behavioral_signals={
                "days_since_activity": 5,
                "email_opens_30d": 10,
            },
        )

        result = pipeline.execute(context)

        assert result.is_success is True
        assert result.customer_id == "cust_123"
        assert result.segment is not None
        assert result.message is not None
        assert len(result.propensity_scores) > 0
        assert len(result.audit_trail) > 0

    def test_pipeline_safety_check(self):
        """Test that pipeline performs safety checks."""
        pipeline = Pipeline()

        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Jane"},
        )

        result = pipeline.execute(context)

        assert result.safety_report is not None
        assert result.is_safe_to_send is True or result.is_safe_to_send is False

    def test_pipeline_skip_safety_check(self):
        """Test pipeline with safety check skipped."""
        pipeline = Pipeline()

        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Bob"},
        )

        result = pipeline.execute(context, skip_safety_check=True)

        assert result.safety_report is None
        assert result.is_safe_to_send is True

    def test_pipeline_with_experiment(self):
        """Test pipeline with experiment orchestration."""
        pipeline = Pipeline()

        # Create an experiment
        variants = [
            ExperimentVariant(variant_id="control", name="Control", weight=0.5),
            ExperimentVariant(variant_id="treatment", name="Treatment", weight=0.5),
        ]
        experiment = pipeline.experiment_orchestrator.create_experiment(
            name="Test Experiment",
            variants=variants,
        )
        pipeline.experiment_orchestrator.start_experiment(experiment.experiment_id)

        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Alice"},
        )

        result = pipeline.execute(context, experiment_id=experiment.experiment_id)

        assert result.is_success is True
        assert result.experiment_variant is not None

    def test_pipeline_batch_execution(self):
        """Test batch pipeline execution."""
        pipeline = Pipeline()

        contexts = [
            CustomerContext(
                customer_id=f"cust_{i}",
                attributes={"name": f"Customer {i}"},
            )
            for i in range(5)
        ]

        results = pipeline.execute_batch(contexts)

        assert len(results) == 5
        assert all(r.is_success for r in results)

    def test_pipeline_execution_history(self):
        """Test pipeline execution history tracking."""
        pipeline = Pipeline()

        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Test"},
        )

        pipeline.execute(context)
        pipeline.execute(context)

        history = pipeline.get_execution_history()

        assert len(history) == 2

    def test_pipeline_clear_history(self):
        """Test clearing execution history."""
        pipeline = Pipeline()

        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Test"},
        )

        pipeline.execute(context)
        pipeline.clear_execution_history()

        assert len(pipeline.get_execution_history()) == 0

    def test_pipeline_audit_trail(self):
        """Test getting audit trail for a specific execution."""
        pipeline = Pipeline()

        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Test"},
        )

        result = pipeline.execute(context)
        audit_trail = pipeline.get_audit_trail(result.pipeline_id)

        assert len(audit_trail) > 0

    def test_pipeline_stats(self):
        """Test pipeline statistics."""
        pipeline = Pipeline()

        contexts = [
            CustomerContext(
                customer_id=f"cust_{i}",
                attributes={"name": f"Customer {i}"},
            )
            for i in range(3)
        ]

        pipeline.execute_batch(contexts)

        stats = pipeline.get_pipeline_stats()

        assert stats["total_executions"] == 3
        assert 0 <= stats["success_rate"] <= 1
        assert 0 <= stats["safe_to_send_rate"] <= 1
        assert stats["average_execution_time_ms"] >= 0

    def test_pipeline_stats_empty(self):
        """Test pipeline statistics with no executions."""
        pipeline = Pipeline()

        stats = pipeline.get_pipeline_stats()

        assert stats["total_executions"] == 0
        assert stats["success_rate"] == 0.0

    def test_pipeline_result_to_dict(self):
        """Test converting pipeline result to dictionary."""
        pipeline = Pipeline()

        context = CustomerContext(
            customer_id="cust_123",
            attributes={"name": "Test"},
        )

        result = pipeline.execute(context)
        result_dict = result.to_dict()

        assert result_dict["customer_id"] == "cust_123"
        assert "pipeline_id" in result_dict
        assert "message_id" in result_dict
        assert "execution_time_ms" in result_dict

    def test_high_value_customer_flow(self):
        """Test complete flow for a high-value customer."""
        pipeline = Pipeline()

        context = CustomerContext(
            customer_id="cust_vip_001",
            attributes={
                "name": "VIP Customer",
                "lifetime_value": 5000,
                "tenure_days": 365,
            },
            behavioral_signals={
                "days_since_activity": 2,
                "email_opens_30d": 20,
                "product_views_7d": 30,
            },
        )

        result = pipeline.execute(context)

        assert result.is_success is True
        assert result.segment == "high_value"
        assert "churn_propensity" in result.propensity_scores
        assert "purchase_propensity" in result.propensity_scores

    def test_at_risk_customer_flow(self):
        """Test complete flow for an at-risk customer."""
        pipeline = Pipeline()

        context = CustomerContext(
            customer_id="cust_at_risk_001",
            attributes={
                "name": "Inactive Customer",
                "lifetime_value": 200,
            },
            behavioral_signals={
                "days_since_activity": 45,
                "support_tickets_30d": 2,
            },
        )

        result = pipeline.execute(context)

        assert result.is_success is True
        assert result.segment == "at_risk"
        assert result.propensity_scores.get("churn_propensity", 0) > 0.3
