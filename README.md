# PulseCraft

PulseCraft is a modular agent-based platform that personalizes outbound customer experiences for subscription and consumer brands by turning behavioral signals and model-driven propensities into safe, on-brand messages with traceable content provenance and measurable uplift.

## Features

- **Segmentation**: Rule-based customer segmentation for targeted messaging
- **Signal Scoring**: Behavioral signal processing and propensity scoring
- **Content Retrieval**: Template-based content library with provenance tracking
- **Message Composition**: Generative message creation with personalization
- **Safety Checks**: Pre-send validation for safe, on-brand messaging
- **Experiment Orchestration**: A/B testing with variant assignment and uplift measurement

## Installation

```bash
pip install pulsecraft
```

For development:
```bash
pip install pulsecraft[dev]
```

## Quick Start

```python
from pulsecraft import Pipeline
from pulsecraft.base import CustomerContext

# Create a pipeline with default agents
pipeline = Pipeline()

# Create a customer context
context = CustomerContext(
    customer_id="cust_123",
    attributes={
        "name": "John Doe",
        "lifetime_value": 2500,
        "tenure_days": 180,
    },
    behavioral_signals={
        "days_since_activity": 5,
        "email_opens_30d": 12,
        "product_views_7d": 8,
    },
)

# Execute the pipeline
result = pipeline.execute(context)

# Access the results
print(f"Segment: {result.segment}")
print(f"Message: {result.message.content}")
print(f"Safe to send: {result.is_safe_to_send}")
print(f"Propensity scores: {result.propensity_scores}")
```

## Architecture

PulseCraft uses a modular agent-based architecture:

```
CustomerContext
       │
       ▼
┌──────────────────┐
│ SegmentationAgent │  → Assigns customer segment
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ SignalScoringAgent│  → Computes propensity scores
└──────────────────┘
       │
       ▼
┌─────────────────────┐
│ExperimentOrchestrator│  → Assigns experiment variant
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│ContentRetrievalAgent │  → Retrieves content template
└─────────────────────┘
       │
       ▼
┌────────────────────────┐
│MessageCompositionAgent │  → Composes personalized message
└────────────────────────┘
       │
       ▼
┌──────────────────┐
│ SafetyCheckAgent │  → Validates message safety
└──────────────────┘
       │
       ▼
   PipelineResult
```

## Agents

### SegmentationAgent

Segments customers based on configurable rules:

```python
from pulsecraft import SegmentationAgent

agent = SegmentationAgent()

# Add custom segment rule
agent.add_segment_rule(
    "premium",
    lambda ctx: ctx.attributes.get("subscription_tier") == "premium"
)
```

### SignalScoringAgent

Computes propensity scores from behavioral signals:

```python
from pulsecraft import SignalScoringAgent

agent = SignalScoringAgent()

# Add custom scoring model
def loyalty_score(ctx):
    return min(ctx.attributes.get("tenure_days", 0) / 365, 1.0)

agent.add_scoring_model("loyalty_score", loyalty_score)
```

### ContentRetrievalAgent

Manages content library with provenance tracking:

```python
from pulsecraft import ContentRetrievalAgent
from pulsecraft.content import ContentItem

agent = ContentRetrievalAgent()

# Add custom content
content = ContentItem(
    content_id="special_offer",
    template="Hi {customer_name}, enjoy 20% off!",
    segment_targeting=["high_value"],
    provenance={"source": "marketing_campaign", "author": "marketing_team"},
)
agent.add_content(content)
```

### SafetyCheckAgent

Validates messages before sending:

```python
from pulsecraft import SafetyCheckAgent
from pulsecraft.safety import SafetyCheckResult

agent = SafetyCheckAgent()

# Add custom safety check
def check_profanity(message):
    if "badword" in message.content.lower():
        return SafetyCheckResult.FAIL, "Contains profanity"
    return SafetyCheckResult.PASS, "No profanity detected"

agent.add_safety_check("profanity_check", check_profanity)
```

### ExperimentOrchestrator

Manages A/B experiments with uplift measurement:

```python
from pulsecraft import ExperimentOrchestrator
from pulsecraft.experiment import ExperimentVariant

orchestrator = ExperimentOrchestrator()

# Create experiment
variants = [
    ExperimentVariant(variant_id="control", name="Control", weight=0.5),
    ExperimentVariant(variant_id="treatment", name="Treatment", weight=0.5),
]
experiment = orchestrator.create_experiment(
    name="Welcome Email Test",
    variants=variants,
    target_segment="new_customer",
)
orchestrator.start_experiment(experiment.experiment_id)

# Record conversions
orchestrator.record_conversion("cust_123", experiment.experiment_id, value=50.0)

# Calculate uplift
uplift = orchestrator.calculate_uplift(experiment.experiment_id, "control")
```

## Auditability & Explainability

Every agent creates audit records for full traceability:

```python
result = pipeline.execute(context)

# Access audit trail
for record in result.audit_trail:
    print(f"{record['agent_name']}: {record['output_summary']}")
```

## License

MIT License - see [LICENSE](LICENSE) for details.
