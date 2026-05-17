"""Outcome taxonomy for the admissibility kernel.

All gate outputs are members of one of these enumerations.
No outcome is a soft category — each has a precise formal meaning.

GateOutcome:
  EXECUTE   Proposal satisfies admissibility conditions on projected state.
            Execution is permitted. Observed state validation follows.
  TRANSFORM Proposal is not executable as stated. An admissible reframing
            may exist, subject to Ωᵣ-preservation constraint.
  DEFER     Commitment boundary must not be crossed. Produces a DeferRecord.
            State does not change. No execution occurs.
  REJECT    Proposal violates invariant, boundary, or transformability conditions.
            No reframing can recover it within the current evaluation context.

ViabilityStatus:
  VIABLE                Recursive continuation preserves governability over horizon H.
  CONDITIONALLY_VIABLE  Viability holds under explicit constraints or reduced horizon.
  DEFER_REQUIRED        Insufficient evidence or margin to cross commitment boundary.
  NON_VIABLE            Horizon projection produces unavoidable violation or collapse.

TransformabilityStatus:
  PRESERVED               Future legitimate transformation remains recoverable.
  CONTRACTED_WITHIN_BOUNDS Transformability narrows but within authorised bounds.
  TRANSFORM_REQUIRED      Proposal must be reframed to preserve future manoeuvre space.
  DEFER_REQUIRED          Evidence is insufficient to determine transformability effect.
  VIOLATED                Transition destroys or illegitimately narrows future transformability.

Neverthought / EIG — admissibility-kernel public layer v0.1.0
"""
from enum import Enum


class GateOutcome(Enum):
    EXECUTE = "EXECUTE"
    TRANSFORM = "TRANSFORM"
    DEFER = "DEFER"
    REJECT = "REJECT"


class ViabilityStatus(Enum):
    VIABLE = "VIABLE"
    CONDITIONALLY_VIABLE = "CONDITIONALLY_VIABLE"
    DEFER_REQUIRED = "DEFER_REQUIRED"
    NON_VIABLE = "NON_VIABLE"


class TransformabilityStatus(Enum):
    PRESERVED = "PRESERVED"
    CONTRACTED_WITHIN_BOUNDS = "CONTRACTED_WITHIN_BOUNDS"
    TRANSFORM_REQUIRED = "TRANSFORM_REQUIRED"
    DEFER_REQUIRED = "DEFER_REQUIRED"
    VIOLATED = "VIOLATED"


class RecursionFailureMode(Enum):
    """The seven named recursion failure modes of the RVK.

    A locally admissible system can fail globally through any of these.
    Each is a distinct structural failure, not a severity ranking.
    """
    LOCAL_PASS_GLOBAL_FAIL = "LOCAL_PASS_GLOBAL_FAIL"
    RESIDUE_COMPACTION = "RESIDUE_COMPACTION"
    AUTHORITY_COOLING = "AUTHORITY_COOLING"
    BRANCH_CONTAMINATION = "BRANCH_CONTAMINATION"
    OPTIONALITY_EXHAUSTION = "OPTIONALITY_EXHAUSTION"
    DEFERRED_COLLAPSE_MASKING = "DEFERRED_COLLAPSE_MASKING"
    TRANSFORM_CHURN = "TRANSFORM_CHURN"
