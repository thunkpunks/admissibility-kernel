"""Transformability Preservation Invariant (TPI).

The deepest invariant. Governs whether a transition preserves the system's
ability to undergo legitimate future transformation.

Correctness, coherence, and reversibility are insufficient. A recursive system
can remain locally coherent while losing the ability to change meaningfully.
The central conserved quantity is future legitimate transformability.

Formal skeleton:
  TPI(S_t, u_t) holds iff:
    F_legit(Ŝ_{t+1|p}) is non-empty,
    Ωᵣ(Ŝ_{t+1|p}) >= Ω_floor,
    contraction_rate(Ωᵣ) <= ρ_max unless explicitly authorised,
    B_iso(Ŝ_{t+1|p}) is preserved,
    Θ(Ŝ_{t+1|p}) remains above renegotiability floor,
    and any lost branch is logged with residue and authority basis.

Statuses:
  PRESERVED               Future legitimate transformation remains recoverable.
  CONTRACTED_WITHIN_BOUNDS Transformability narrows but within authorised bounds.
  TRANSFORM_REQUIRED      Proposal must be reframed to preserve future manoeuvre space.
  DEFER_REQUIRED          Evidence is insufficient to determine transformability effect.
  VIOLATED                Transition destroys or illegitimately narrows future transformability.

Neverthought / EIG — admissibility-kernel public layer v0.1.0
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from neverthought_admissibility.outcome import TransformabilityStatus
from neverthought_admissibility.projection import (
    Proposal,
    ProjectedState,
    IrreversibilityClass,
    BlastRadius,
)


@dataclass(frozen=True)
class TPIResult:
    """Result of a Transformability Preservation Invariant assessment."""

    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    proposal_id: str = ""

    status: TransformabilityStatus = TransformabilityStatus.PRESERVED

    projected_omega_r: float = 1.0
    projected_b_iso: str = "PRESERVED"
    projected_theta: float = 1.0

    # Whether the transition preserved the minimum legitimate future set
    future_set_non_empty: bool = True
    contraction_within_bounds: bool = True
    branch_isolation_preserved: bool = True

    violation_basis: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class TransformabilityPreservationInvariant:
    """Assesses whether a proposed transition preserves future legitimate transformability.

    Evaluates four conditions on the projected state:
      1. Ωᵣ remains above the viability floor
      2. B_iso is not violated
      3. Θ remains above renegotiability floor (for irreversible transitions)
      4. Contraction rate is within bounds

    The TPI is assessed after projection. It is a second-order check:
    first the gate checks whether the proposed transition is locally admissible
    (C1–C7), then the TPI checks whether it is globally transformability-preserving.
    """

    _OMEGA_R_FLOOR: float = 0.20
    _THETA_FLOOR: float = 0.30
    _MAX_CONTRACTION_RATE: float = 0.35  # Ωᵣ drop above this requires authorisation

    def assess(
        self,
        proposal: Proposal,
        projected: ProjectedState,
    ) -> TPIResult:
        """Assess transformability preservation on the projected state."""
        violations: list[str] = []

        # Condition 1: Ωᵣ above floor
        omega_ok = projected.projected_omega_r > self._OMEGA_R_FLOOR
        if not omega_ok:
            violations.append(
                f"Ωᵣ={projected.projected_omega_r:.4f} below floor {self._OMEGA_R_FLOOR}"
            )

        # Condition 2: B_iso not violated
        b_iso_ok = projected.projected_b_iso != "VIOLATED"
        if not b_iso_ok:
            violations.append("B_iso VIOLATED — branch isolation broken")

        # Condition 3: Θ above renegotiability floor for irreversible transitions
        theta_ok = True
        if proposal.irreversibility == IrreversibilityClass.IRREVERSIBLE:
            theta_ok = projected.projected_theta > self._THETA_FLOOR
            if not theta_ok:
                violations.append(
                    f"Irreversible transition with Θ={projected.projected_theta:.4f} "
                    f"below renegotiability floor {self._THETA_FLOOR}"
                )

        # Condition 4: Contraction rate within bounds
        # (illustrative: HIGH blast on IRREVERSIBLE is above max contraction)
        contraction_high = (
            proposal.irreversibility == IrreversibilityClass.IRREVERSIBLE
            and proposal.blast_radius == BlastRadius.HIGH
        )
        contraction_ok = not contraction_high or projected.c4_optionality_preserved

        if not contraction_ok:
            violations.append(
                "Contraction rate exceeds authorised bounds: "
                "IRREVERSIBLE + HIGH blast without Ωᵣ margin"
            )

        # Route to status
        if not omega_ok and not b_iso_ok:
            status = TransformabilityStatus.VIOLATED
        elif not omega_ok or (not theta_ok and not b_iso_ok):
            status = TransformabilityStatus.VIOLATED
        elif not theta_ok and proposal.irreversibility == IrreversibilityClass.IRREVERSIBLE:
            status = TransformabilityStatus.TRANSFORM_REQUIRED
        elif not contraction_ok:
            status = TransformabilityStatus.TRANSFORM_REQUIRED
        elif not b_iso_ok:
            status = TransformabilityStatus.TRANSFORM_REQUIRED
        elif projected.projected_omega_r < 0.40:
            # Contracted but within bounds (above floor, below healthy)
            status = TransformabilityStatus.CONTRACTED_WITHIN_BOUNDS
        else:
            status = TransformabilityStatus.PRESERVED

        return TPIResult(
            proposal_id=proposal.proposal_id,
            status=status,
            projected_omega_r=projected.projected_omega_r,
            projected_b_iso=projected.projected_b_iso,
            projected_theta=projected.projected_theta,
            future_set_non_empty=omega_ok,
            contraction_within_bounds=contraction_ok,
            branch_isolation_preserved=b_iso_ok,
            violation_basis="; ".join(violations) if violations else "",
        )
