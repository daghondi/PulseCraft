"""
PulseCraft - Modular Agent-Based Customer Experience Personalization Platform

PulseCraft personalizes outbound customer experiences for subscription and consumer
brands by turning behavioral signals and model-driven propensities into safe,
on-brand messages with traceable content provenance and measurable uplift.
"""

__version__ = "0.1.0"

from pulsecraft.composition import MessageCompositionAgent
from pulsecraft.content import ContentRetrievalAgent
from pulsecraft.experiment import ExperimentOrchestrator
from pulsecraft.pipeline import Pipeline
from pulsecraft.safety import SafetyCheckAgent
from pulsecraft.segmentation import SegmentationAgent
from pulsecraft.signals import SignalScoringAgent

__all__ = [
    "Pipeline",
    "SegmentationAgent",
    "SignalScoringAgent",
    "ContentRetrievalAgent",
    "MessageCompositionAgent",
    "SafetyCheckAgent",
    "ExperimentOrchestrator",
]
