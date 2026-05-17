"""Decision records — the evidence artefacts produced by the gate.

Every gate decision produces a structured record. Records are evidence.
They cannot be cancelled or superseded by subsequent decisions.

AdmissibilityDecisionRecord
  Produced by every gate evaluation. Contains the proposal, projected state
  reference, constraint results, transformability status, and the decision.
  Audit-hash mechanics are outside this public inspection layer.

DeferRecord
  Produced when the gate returns DEFER. Documents precisely why commitment
  was withheld, what conditions are unresolved, what evidence is required,
  and how much residue this DEFER contributes to accumulated pressure.

  DEFER is not a UI hesitation. It is a controlled non-transition:
  DEFER(S_t, u_t) = S_t + DeferRecord(...)
  No commitment boundary is crossed. The state does not change.

TransformRecord
  Produced when a TRANSFORM proposal is submitted for validation.
  A TRANSFORM is admissible only if its projected Ωᵣ >= the original
  proposal's projected Ωᵣ. A transform that reduces recoverable optionality
  is not a reframing — it is a softening, and it fails.

Neverthought / EIG — admissibility-kernel public layer v0.1.0
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from neverthought_admissibility.outcome import GateOutcome, TransformabilityStatus


class DeferReason(Enum):
    PROJECTED_STATE_FAILS_CONDITIONS = "PROJECTED_STATE_FAILS_CONDITIONS"
    IRREVERSIBLE_ON_COLD_TOPOLOGY = "IRREVERSIBLE_ON_COLD_TOPOLOGY"
    RESIDUE_ABOVE_THRESHOLD = "RESIDUE_ABOVE_THRESHOLD"
    AUDIT_BASIS_ABSENT = "AUDIT_BASIS_ABSENT"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class TransformValidationStatus(Enum):
    VALID = "VALID"
    INVALID_OPTIONALITY_REDUCED = "INVALID_OPTIONALITY_REDUCED"
    INVALID_CONSTRAINT_WEAKENED = "INVALID_CONSTRAINT_WEAKENED"
    INVALID_CONDITIONS_FAIL = "INVALID_CONDITIONS_FAIL"
    CHURN_DETECTED = "CHURN_DETECTED"


@dataclass(frozen=True)
class ConstraintResult:
    constraint_id: str
    status: str   # PASS | FAIL | UNKNOWN_CONSERVATIVE | NOT_APPLICABLE
    summary: str = ""


@dataclass(frozen=True)
class AdmissibilityDecisionRecord:
    """Evidence artefact for every gate decision.

    This record persists regardless of the decision.
    A REJECT decision is not erased by a subsequent EXECUTE on a different proposal.
    """
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    proposal_id: str = ""
    state_ref: str = ""
    projection_ref: str = ""
    observed_state_ref: Optional[str] = None   # Populated after execution

    decision: GateOutcome = GateOutcome.DEFER

    constraint_results: tuple[ConstraintResult, ...] = field(default_factory=tuple)

    residue_count: int = 0
    review_required: bool = False

    optionality_direction: str = "UNKNOWN"   # PRESERVED | EXPANDED | CONTRACTED | UNKNOWN
    transformability_status: TransformabilityStatus = TransformabilityStatus.PRESERVED

    review_prompts: tuple[str, ...] = field(default_factory=tuple)
    denial_reason: Optional[str] = None

    # audit_hash: outside public inspection layer
    audit_hash: str = "PROXY_HASH_UNCERTIFIED"


@dataclass(frozen=True)
class DeferRecord:
    """Formal non-transition record for DEFER outcomes.

    The existence of this record is the governance act. The state has not changed.
    The proposal has not executed. The record documents the gap.

    residue_weight: how much this DEFER adds to the session's accumulated
    pressure. Repeated DEFERs without resolution compound residue. A system
    that accumulates DEFER residue without resolving the underlying conditions
    is masking deferred collapse.
    """
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    proposal_id: str = ""
    state_ref: str = ""
    defer_reason: DeferReason = DeferReason.PROJECTED_STATE_FAILS_CONDITIONS

    unresolved_conditions: tuple[str, ...] = field(default_factory=tuple)
    residue_items: tuple[str, ...] = field(default_factory=tuple)
    required_evidence: tuple[str, ...] = field(default_factory=tuple)
    required_human_review: bool = False
    expiry_or_recheck_condition: str = ""

    residue_weight: float = 0.10   # Contribution to accumulated session pressure

    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass(frozen=True)
class TransformRecord:
    """Validation record for a TRANSFORM proposal.

    A TRANSFORM is admissible only if:
      projected_omega_r (transform) >= projected_omega_r (original proposal)

    This is the Ωᵣ-preservation constraint. It means:
      - The reframing must preserve or improve recoverable optionality
      - It must not weaken any constraint relative to the rejected proposal
      - Its projected state must satisfy C1–C7

    A transform that reduces Ωᵣ is not a reframing. It is a softening.
    It fails. The correct response to a rejected softening is DEFER or REJECT,
    not a further transform attempt.

    Repeated transforms without Ωᵣ improvement constitute TRANSFORM_CHURN —
    a recursion failure mode of the RVK.
    """
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    transform_proposal_id: str = ""
    original_proposal_id: str = ""

    status: TransformValidationStatus = TransformValidationStatus.INVALID_CONDITIONS_FAIL

    original_projected_omega_r: float = 0.0
    transform_projected_omega_r: float = 0.0
    omega_r_delta: float = 0.0          # transform − original; must be >= 0 to be VALID

    conditions_checked: tuple[str, ...] = field(default_factory=tuple)
    conditions_failed: tuple[str, ...] = field(default_factory=tuple)
    denial_reason: Optional[str] = None
    chain_depth: int = 0               # How many transforms have been attempted

    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def valid(self) -> bool:
        return self.status == TransformValidationStatus.VALID
