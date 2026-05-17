"""neverthought_admissibility — Neverthought / EIG public implementation layer.

Pre-commitment admissibility architecture for runtime governance of agentic systems.

Three named assets:
  PCAG  Pre-Commitment Admissibility Gate
  RVK   Recursive Viability Kernel
  TPI   Transformability Preservation Invariant

Governing invariant:
  Can the system still become otherwise?

Attribution: Mebs Loghdey / Neverthought
Framework: Epistemic Integrity Governance (EIG) / Semantic Ruliad
"""
from neverthought_admissibility.outcome import GateOutcome, ViabilityStatus, TransformabilityStatus
from neverthought_admissibility.records import (
    AdmissibilityDecisionRecord,
    DeferRecord,
    TransformRecord,
)
from neverthought_admissibility.projection import (
    Proposal,
    CurrentState,
    ProjectedState,
    ObservedState,
    ProposalEvaluator,
    IrreversibilityClass,
    BlastRadius,
)
from neverthought_admissibility.gate import AdmissibilityGate, GateResult
from neverthought_admissibility.viability import RecursiveViabilityKernel, ViabilityReport
from neverthought_admissibility.tpi import TransformabilityPreservationInvariant, TPIResult

__all__ = [
    "GateOutcome",
    "ViabilityStatus",
    "TransformabilityStatus",
    "AdmissibilityDecisionRecord",
    "DeferRecord",
    "TransformRecord",
    "Proposal",
    "CurrentState",
    "ProjectedState",
    "ObservedState",
    "ProposalEvaluator",
    "IrreversibilityClass",
    "BlastRadius",
    "AdmissibilityGate",
    "GateResult",
    "RecursiveViabilityKernel",
    "ViabilityReport",
    "TransformabilityPreservationInvariant",
    "TPIResult",
]

__version__ = "0.1.0"
__author__ = "Mebs Loghdey / Neverthought"
