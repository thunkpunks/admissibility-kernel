"""Recursive Viability Kernel (RVK).

Evaluates whether a sequence of locally admissible transitions remains
governable under recursive composition.

The core problem: a system can pass every local gate and still become
globally non-viable. The failure is not a single violation — it is the
recursive contraction of future manoeuvre space across a horizon of decisions.

Core definition:
  RV_H(S_t) = VIABLE
  iff for all authorised sequences σ_h, h <= H:
    GatePath(S_t, σ_h) ∈ {
      EXECUTE_SAFE,
      TRANSFORM_BEFORE_VIOLATION,
      DEFER_BEFORE_COMMITMENT,
      REJECT_BEFORE_EXECUTION,
    }

Seven named recursion failure modes:

  LOCAL_PASS_GLOBAL_FAIL     Every tick passes; horizon collapses.
                             Also known as OstinatoLock: apparent stability
                             masking declining renegotiability.

  RESIDUE_COMPACTION         Unresolved DEFER/HOLD residue accumulates faster
                             than EXECUTE resolves it.

  AUTHORITY_COOLING          Decision authority concentrates; reviewer pool shrinks.

  BRANCH_CONTAMINATION       Counterfactual alternatives become unrecoverable.
                             Irrecoverable branch losses accumulate.

  OPTIONALITY_EXHAUSTION     Ωᵣ falls below recoverable floor.

  DEFERRED_COLLAPSE_MASKING  Repeated DEFER without resolution hides commitment drift.

  TRANSFORM_CHURN            Repeated TRANSFORM without Ωᵣ improvement signals
                             instability rather than progress.

Neverthought / EIG — admissibility-kernel public layer v0.1.0
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from neverthought_admissibility.outcome import GateOutcome, ViabilityStatus, RecursionFailureMode


@dataclass
class SessionTrace:
    """Lightweight cross-run state for the RVK.

    Maintained by the caller across a sequence of gate evaluations.
    The RVK reads from this trace to detect horizon-level failure modes.
    """
    omega_r_history: list[float] = field(default_factory=list)
    theta_history: list[float] = field(default_factory=list)
    outcome_history: list[GateOutcome] = field(default_factory=list)
    accumulated_residue: float = 0.0
    recoverable_branch_count: int = 0
    permanent_closure_count: int = 0
    reviewer_ids_per_run: list[set[str]] = field(default_factory=list)
    consecutive_defers: int = 0
    consecutive_transforms: int = 0
    transform_omega_r_history: list[float] = field(default_factory=list)

    def record_outcome(
        self,
        outcome: GateOutcome,
        omega_r: float,
        theta: float,
        residue_delta: float = 0.0,
        reviewer_ids: Optional[set[str]] = None,
    ) -> None:
        self.omega_r_history.append(omega_r)
        self.theta_history.append(theta)
        self.outcome_history.append(outcome)

        if outcome == GateOutcome.DEFER:
            self.accumulated_residue = min(self.accumulated_residue + residue_delta + 0.10, 1.0)
            self.consecutive_defers += 1
            self.consecutive_transforms = 0
        elif outcome == GateOutcome.TRANSFORM:
            self.consecutive_transforms += 1
            self.consecutive_defers = 0
            self.transform_omega_r_history.append(omega_r)
        elif outcome == GateOutcome.EXECUTE:
            self.accumulated_residue = max(self.accumulated_residue - 0.10, 0.0)
            self.consecutive_defers = 0
            self.consecutive_transforms = 0

        if reviewer_ids is not None:
            self.reviewer_ids_per_run.append(reviewer_ids)


@dataclass(frozen=True)
class ViabilityReport:
    """Output of a RecursiveViabilityKernel evaluation."""

    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    viability_status: ViabilityStatus = ViabilityStatus.VIABLE
    active_failure_modes: tuple[RecursionFailureMode, ...] = field(default_factory=tuple)
    manifold_pressure: float = 0.0
    omega_r_trajectory: str = "STABLE"
    theta_trajectory: str = "WARM"
    accumulated_residue: float = 0.0
    recoverable_branch_count: int = 0
    permanent_closure_count: int = 0
    recommended_action: GateOutcome = GateOutcome.EXECUTE
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class RecursiveViabilityKernel:
    """Detects horizon-level failure modes across a session trace.

    Operates on SessionTrace — the accumulated cross-run state.
    Each method detects one of the seven named failure modes.

    The RVK does not gate individual proposals. The AdmissibilityGate does that.
    The RVK evaluates whether the sequence of gate decisions is producing
    a viable trajectory or a structurally failing one.
    """

    def local_pass_global_fail(self, trace: SessionTrace) -> bool:
        """Apparent stability masking declining renegotiability (OstinatoLock).

        Requires: mostly-passing outcomes AND strictly declining Ωᵣ.
        A flat stable Ωᵣ is not OstinatoLock — it is healthy stability.
        """
        if len(trace.omega_r_history) < 3:
            return False
        non_reject = sum(
            1 for o in trace.outcome_history
            if o not in (GateOutcome.REJECT,)
        )
        runs = len(trace.outcome_history)
        if non_reject / runs < 0.70:
            return False
        # Ωᵣ must be strictly declining (not merely flat)
        recent = trace.omega_r_history[-3:]
        return recent[-1] < recent[0]

    def residue_compaction(self, trace: SessionTrace) -> bool:
        """Residue accumulating faster than EXECUTE resolves it."""
        if trace.accumulated_residue > 0.50:
            return True
        if len(trace.outcome_history) < 3:
            return False
        recent = trace.outcome_history[-3:]
        defer_hold = sum(1 for o in recent if o in (GateOutcome.DEFER,))
        execute = sum(1 for o in recent if o == GateOutcome.EXECUTE)
        return defer_hold > execute and trace.accumulated_residue > 0.30

    def authority_cooling(self, trace: SessionTrace) -> bool:
        """Reviewer pool shrinking — authority concentrating."""
        if len(trace.reviewer_ids_per_run) < 3:
            return False
        recent: set[str] = set()
        for r in trace.reviewer_ids_per_run[-3:]:
            recent |= r
        early: set[str] = set()
        for r in trace.reviewer_ids_per_run[:-3]:
            early |= r
        if not early:
            return False
        return len(recent) < len(early) or len(recent) <= 1

    def branch_contamination(self, trace: SessionTrace) -> bool:
        """Irrecoverable branch losses making futures unrecoverable."""
        return trace.permanent_closure_count >= 2

    def optionality_exhaustion(self, trace: SessionTrace) -> bool:
        """Ωᵣ collapsed below recoverable floor."""
        if not trace.omega_r_history:
            return False
        return trace.omega_r_history[-1] < 0.10

    def deferred_collapse_masking(self, trace: SessionTrace) -> bool:
        """3+ consecutive DEFERs without resolution."""
        return trace.consecutive_defers >= 3

    def transform_churn(self, trace: SessionTrace) -> bool:
        """3+ consecutive TRANSFORMs without Ωᵣ improvement."""
        if trace.consecutive_transforms < 3:
            return False
        if len(trace.transform_omega_r_history) < 3:
            return False
        recent = trace.transform_omega_r_history[-3:]
        return not any(recent[i + 1] > recent[i] for i in range(len(recent) - 1))

    def manifold_pressure(self, trace: SessionTrace) -> float:
        """Scalar summary of session-level governance pressure ∈ [0, 1]."""
        if not trace.omega_r_history:
            return 0.0
        recent_omega = trace.omega_r_history[-1]
        residue_contrib = trace.accumulated_residue * 0.4
        omega_contrib = (1.0 - recent_omega) * 0.4
        mode_contrib = min(len(self.active_failure_modes(trace)) * 0.1, 0.2)
        return round(min(residue_contrib + omega_contrib + mode_contrib, 1.0), 4)

    def omega_r_trajectory(self, trace: SessionTrace) -> str:
        if len(trace.omega_r_history) < 2:
            return "UNKNOWN"
        recent = trace.omega_r_history[-3:]
        delta = recent[-1] - recent[0]
        if delta > 0.05:
            return "RECOVERING"
        if delta < -0.20:
            return "COLLAPSED"
        if delta < -0.05:
            return "DECLINING"
        return "STABLE"

    def active_failure_modes(self, trace: SessionTrace) -> list[RecursionFailureMode]:
        return [
            mode for mode, detected in [
                (RecursionFailureMode.LOCAL_PASS_GLOBAL_FAIL, self.local_pass_global_fail(trace)),
                (RecursionFailureMode.RESIDUE_COMPACTION, self.residue_compaction(trace)),
                (RecursionFailureMode.AUTHORITY_COOLING, self.authority_cooling(trace)),
                (RecursionFailureMode.BRANCH_CONTAMINATION, self.branch_contamination(trace)),
                (RecursionFailureMode.OPTIONALITY_EXHAUSTION, self.optionality_exhaustion(trace)),
                (RecursionFailureMode.DEFERRED_COLLAPSE_MASKING, self.deferred_collapse_masking(trace)),
                (RecursionFailureMode.TRANSFORM_CHURN, self.transform_churn(trace)),
            ]
            if detected
        ]

    def evaluate(self, trace: SessionTrace) -> ViabilityReport:
        """Produce a ViabilityReport from the current session trace."""
        modes = self.active_failure_modes(trace)
        pressure = self.manifold_pressure(trace)
        traj = self.omega_r_trajectory(trace)

        if len(modes) >= 2:
            status = ViabilityStatus.NON_VIABLE
            action = GateOutcome.DEFER
        elif modes:
            status = ViabilityStatus.DEFER_REQUIRED
            action = GateOutcome.DEFER
        elif pressure > 0.40:
            status = ViabilityStatus.CONDITIONALLY_VIABLE
            action = GateOutcome.EXECUTE
        else:
            status = ViabilityStatus.VIABLE
            action = GateOutcome.EXECUTE

        theta_traj = "UNKNOWN"
        if len(trace.theta_history) >= 2:
            delta = trace.theta_history[-1] - trace.theta_history[0]
            theta_traj = (
                "WARMING" if delta > 0.05
                else "COLD" if trace.theta_history[-1] < 0.30
                else "COOLING" if delta < -0.05
                else "WARM"
            )

        return ViabilityReport(
            viability_status=status,
            active_failure_modes=tuple(modes),
            manifold_pressure=pressure,
            omega_r_trajectory=traj,
            theta_trajectory=theta_traj,
            accumulated_residue=trace.accumulated_residue,
            recoverable_branch_count=trace.recoverable_branch_count,
            permanent_closure_count=trace.permanent_closure_count,
            recommended_action=action,
        )
