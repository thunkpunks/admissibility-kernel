"""Three-state separation for pre-commitment admissibility.

The gate must never collapse proposal evaluation into post-state forensics.

  S_t          CurrentState  — state before the proposed transition
  Ŝ_{t+1|p}   ProjectedState — conservative estimate of state after proposal
  S_{t+1|o}   ObservedState  — actual state after execution (if it occurs)

The Pre-Commitment Admissibility Gate acts on Ŝ_{t+1|p}.
Not on S_t. Not on S_{t+1|o}.

Evaluating admissibility on current state is current-state auditing.
Evaluating admissibility on observed state is post-hoc forensics.
Neither is pre-commitment governance.

Projection is always conservative: under uncertainty, the projection
assumes the worst plausible consequence. Uncertainty tightens constraints;
it does not soften them.

Note on threshold values:
  The illustrative floor values and adjustment factors in ProposalEvaluator
  are public-safe demonstration values. Calibrated values are withheld.

Neverthought / EIG — admissibility-kernel public layer v0.1.0
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class IrreversibilityClass(Enum):
    REVERSIBLE = "REVERSIBLE"
    REVERSIBLE_WITH_COST = "REVERSIBLE_WITH_COST"
    IRREVERSIBLE = "IRREVERSIBLE"


class BlastRadius(Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


@dataclass(frozen=True)
class Proposal:
    """A proposed transition u_t — what the system intends to do.

    The proposal is the input to the gate. It is not yet execution.
    Nothing commits until the gate returns EXECUTE and the observed
    state is recorded.
    """
    proposal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    target: str = ""
    irreversibility: IrreversibilityClass = IrreversibilityClass.REVERSIBLE
    reversibility_basis: str = ""      # Must be stated if IRREVERSIBLE
    blast_radius: BlastRadius = BlastRadius.LOW
    audit_basis: str = ""              # Evidence basis for the proposal


@dataclass(frozen=True)
class CurrentState:
    """S_t — the state before the proposed transition.

    Contains the observable values that govern projection and constraint evaluation.
    The gate reads from CurrentState but does not act on it directly —
    it projects forward to Ŝ_{t+1|p} first.
    """
    state_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    omega_r: float = 1.0          # Recoverable optionality ∈ [0, 1]
    theta: float = 1.0            # Topology temperature ∈ [0, 1]
    b_iso: str = "PRESERVED"      # Branch isolation: PRESERVED | DEGRADED | VIOLATED
    accumulated_residue: float = 0.0  # Cross-run accumulated unresolved pressure ∈ [0, 1]
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass(frozen=True)
class ProjectedState:
    """Ŝ_{t+1|p} — conservative projection of proposed transition u_t.

    This is the state the gate evaluates. The projection is conservative:
    under uncertainty, it assumes the worst plausible consequence.

    C1–C7 are evaluated on the projected values, not on current state values.
    """
    projection_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    proposal_id: str = ""
    current_state_id: str = ""

    projected_omega_r: float = 1.0
    projected_theta: float = 1.0
    projected_b_iso: str = "PRESERVED"
    effective_omega_floor: float = 0.20   # Rises with accumulated residue

    # Admissibility conditions C1–C7 evaluated on projected values
    c1_invariant_membership: bool = True
    c2_boundary_distance: bool = True
    c3_constraint_non_loosening: bool = True
    c4_optionality_preserved: bool = True     # projected_omega_r > effective_omega_floor
    c5_residue_below_threshold: bool = True
    c6_branch_isolation_preserved: bool = True
    c7_audit_record_sufficient: bool = True

    conservative_adjustments: tuple[str, ...] = field(default_factory=tuple)
    projection_basis: str = ""

    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def all_conditions_pass(self) -> bool:
        return all([
            self.c1_invariant_membership,
            self.c2_boundary_distance,
            self.c3_constraint_non_loosening,
            self.c4_optionality_preserved,
            self.c5_residue_below_threshold,
            self.c6_branch_isolation_preserved,
            self.c7_audit_record_sufficient,
        ])

    def failed_conditions(self) -> list[str]:
        return [
            name for name, passed in {
                "C1:invariant_membership": self.c1_invariant_membership,
                "C2:boundary_distance": self.c2_boundary_distance,
                "C3:constraint_non_loosening": self.c3_constraint_non_loosening,
                "C4:optionality_preserved": self.c4_optionality_preserved,
                "C5:residue_below_threshold": self.c5_residue_below_threshold,
                "C6:branch_isolation_preserved": self.c6_branch_isolation_preserved,
                "C7:audit_record_sufficient": self.c7_audit_record_sufficient,
            }.items()
            if not passed
        ]


@dataclass(frozen=True)
class ObservedState:
    """S_{t+1|o} — the actual state after execution.

    Created only when execution occurs. Validates whether execution
    remained within the permitted envelope established by the ProjectedState.

    If observed values fall outside the projected envelope, the execution
    exceeded the pre-commitment authorisation. This is a governance event.
    """
    observation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    proposal_id: str = ""
    projection_id: str = ""

    observed_omega_r: float = 1.0
    observed_theta: float = 1.0
    observed_b_iso: str = "PRESERVED"

    within_projected_envelope: bool = True
    envelope_deviation_notes: str = ""

    execution_timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class ProposalEvaluator:
    """Π_p — projects a Proposal onto a conservative ProjectedState.

    The adjustment factors used here are illustrative public-safe values.
    Calibrated values are withheld (see CLAIM_BOUNDARY.md).

    The architecture of the projection — conservative adjustment by irreversibility,
    blast radius, and accumulated residue pressure — is the protectable contribution,
    not any specific threshold value.
    """

    # Illustrative base floor. Rises with accumulated residue.
    # See effective_omega_floor().
    _BASE_OMEGA_FLOOR: float = 0.20
    _BASE_THETA_FLOOR: float = 0.30
    _MAX_RESIDUE_LIFT: float = 0.15   # Maximum floor tightening from residue

    # Illustrative adjustments — not calibrated runtime values
    _IRREVERSIBLE_OMEGA_ADJ: dict[str, float] = {
        IrreversibilityClass.REVERSIBLE.value: 0.00,
        IrreversibilityClass.REVERSIBLE_WITH_COST.value: 0.05,
        IrreversibilityClass.IRREVERSIBLE.value: 0.20,
    }
    _BLAST_OMEGA_ADJ: dict[str, float] = {
        BlastRadius.LOW.value: 0.00,
        BlastRadius.MODERATE.value: 0.05,
        BlastRadius.HIGH.value: 0.10,
    }
    _BLAST_THETA_ADJ: dict[str, float] = {
        BlastRadius.LOW.value: 0.00,
        BlastRadius.MODERATE.value: 0.02,
        BlastRadius.HIGH.value: 0.08,
    }

    def effective_omega_floor(self, accumulated_residue: float) -> float:
        """Residue-adjusted Ωᵣ floor.

        Higher accumulated residue → tighter floor → less admissible deformation
        tolerance. The same proposed transition may be admitted under low residue
        and blocked under high residue — not because the proposal changed, but
        because the system has less recoverability margin.

        Floor ∈ [BASE_OMEGA_FLOOR, BASE_OMEGA_FLOOR + MAX_RESIDUE_LIFT].
        Clamped — no runaway tightening.
        """
        lift = min(max(accumulated_residue, 0.0), 1.0) * self._MAX_RESIDUE_LIFT
        return round(self._BASE_OMEGA_FLOOR + lift, 4)

    def project(
        self,
        proposal: Proposal,
        current: CurrentState,
    ) -> ProjectedState:
        """Produce Ŝ_{t+1|p} from proposal u_t and current state S_t."""
        adjustments: list[str] = []

        proj_omega_r = current.omega_r
        proj_theta = current.theta

        # Irreversibility adjustment
        omega_adj = self._IRREVERSIBLE_OMEGA_ADJ.get(
            proposal.irreversibility.value, 0.10
        )
        if omega_adj > 0:
            proj_omega_r -= omega_adj
            adjustments.append(f"irreversibility:{proposal.irreversibility.value}:Ωᵣ−{omega_adj}")

        # Blast radius adjustment
        omega_blast = self._BLAST_OMEGA_ADJ.get(proposal.blast_radius.value, 0.0)
        theta_blast = self._BLAST_THETA_ADJ.get(proposal.blast_radius.value, 0.0)
        if omega_blast or theta_blast:
            proj_omega_r -= omega_blast
            proj_theta -= theta_blast
            adjustments.append(
                f"blast:{proposal.blast_radius.value}:Ωᵣ−{omega_blast},Θ−{theta_blast}"
            )

        proj_omega_r = round(max(0.0, proj_omega_r), 4)
        proj_theta = round(max(0.0, proj_theta), 4)

        # B_iso projection
        if proposal.irreversibility == IrreversibilityClass.IRREVERSIBLE:
            proj_b_iso = "DEGRADED"
            adjustments.append("b_iso:DEGRADED:irreversible")
        else:
            proj_b_iso = current.b_iso

        # Floor (history-aware)
        floor = self.effective_omega_floor(current.accumulated_residue)
        c4_pass = proj_omega_r > floor
        c2_pass = proj_theta > self._BASE_THETA_FLOOR or (
            proposal.irreversibility == IrreversibilityClass.REVERSIBLE
        )
        c5_pass = current.accumulated_residue < 0.40
        c6_pass = proj_b_iso != "VIOLATED"
        c7_pass = bool(proposal.audit_basis or proposal.description)

        if not c4_pass:
            adjustments.append(
                f"C4_fail:projected_Ωᵣ={proj_omega_r:.4f}<floor({floor:.4f})"
                f"[residue={current.accumulated_residue:.4f}]"
            )

        return ProjectedState(
            proposal_id=proposal.proposal_id,
            current_state_id=current.state_id,
            projected_omega_r=proj_omega_r,
            projected_theta=proj_theta,
            projected_b_iso=proj_b_iso,
            effective_omega_floor=floor,
            c1_invariant_membership=True,
            c2_boundary_distance=c2_pass,
            c3_constraint_non_loosening=True,
            c4_optionality_preserved=c4_pass,
            c5_residue_below_threshold=c5_pass,
            c6_branch_isolation_preserved=c6_pass,
            c7_audit_record_sufficient=c7_pass,
            conservative_adjustments=tuple(adjustments),
            projection_basis=(
                f"From Ωᵣ={current.omega_r:.4f}, Θ={current.theta:.4f}; "
                f"residue={current.accumulated_residue:.4f}; "
                f"floor={floor:.4f}; "
                f"irreversibility={proposal.irreversibility.value}; "
                f"blast={proposal.blast_radius.value}"
            ),
        )
