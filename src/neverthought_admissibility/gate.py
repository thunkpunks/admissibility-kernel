"""Pre-Commitment Admissibility Gate (PCAG).

The gate evaluates a proposed transition u_t before execution.
It acts on Ŝ_{t+1|p} — the conservatively projected next state —
not on the current state S_t.

Gate sequence:
  1. Project proposal onto Ŝ_{t+1|p} (ProposalEvaluator)
  2. Evaluate C1–C7 admissibility conditions on projected values
  3. Check transformability preservation (TPI)
  4. Route to EXECUTE | TRANSFORM | DEFER | REJECT
  5. Produce AdmissibilityDecisionRecord

The gate does not execute the proposal. It returns a GateResult.
Execution is the caller's responsibility, contingent on EXECUTE outcome.
If execution occurs, the caller must record an ObservedState and verify
envelope compliance.

Neverthought / EIG — admissibility-kernel public layer v0.1.0
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from neverthought_admissibility.outcome import GateOutcome, TransformabilityStatus
from neverthought_admissibility.projection import (
    Proposal,
    CurrentState,
    ProjectedState,
    ProposalEvaluator,
    IrreversibilityClass,
)
from neverthought_admissibility.records import (
    AdmissibilityDecisionRecord,
    ConstraintResult,
    DeferRecord,
    DeferReason,
)
from neverthought_admissibility.tpi import TransformabilityPreservationInvariant, TPIResult


@dataclass(frozen=True)
class GateResult:
    """The output of one gate evaluation.

    Contains the decision, the projected state used for evaluation,
    the decision record, and (if DEFER) a DeferRecord.

    The gate result is not execution. It is a governance determination.
    """
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    outcome: GateOutcome = GateOutcome.DEFER
    projected_state: Optional[ProjectedState] = None
    tpi_result: Optional[TPIResult] = None
    decision_record: Optional[AdmissibilityDecisionRecord] = None
    defer_record: Optional[DeferRecord] = None
    denial_reason: Optional[str] = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class AdmissibilityGate:
    """Pre-Commitment Admissibility Gate (PCAG).

    Evaluates proposals before execution using conservative projection.

    The gate sequence separates:
      - Proposal evaluation (on projected state)
      - Transformability assessment (TPI)
      - Outcome routing (EXECUTE | TRANSFORM | DEFER | REJECT)
      - Record production (AdmissibilityDecisionRecord + optional DeferRecord)

    This separation is the architectural contribution. A gate that collapses
    these steps cannot produce traceable pre-commitment governance.
    """

    def __init__(self) -> None:
        self._evaluator = ProposalEvaluator()
        self._tpi = TransformabilityPreservationInvariant()

    def evaluate(
        self,
        proposal: Proposal,
        current: CurrentState,
    ) -> GateResult:
        """Evaluate proposal u_t against projected state Ŝ_{t+1|p}.

        Returns a GateResult containing the outcome and all evidence artefacts.
        """
        # Step 1: Project
        projected = self._evaluator.project(proposal, current)

        # Step 2: TPI assessment
        tpi_result = self._tpi.assess(proposal, projected)

        # Step 3: Route
        outcome, denial_reason, defer_record = self._route(
            proposal, current, projected, tpi_result
        )

        # Step 4: Build decision record
        constraint_results = tuple(
            ConstraintResult(
                constraint_id=name,
                status="PASS" if passed else "FAIL",
            )
            for name, passed in {
                "C1:invariant_membership": projected.c1_invariant_membership,
                "C2:boundary_distance": projected.c2_boundary_distance,
                "C3:constraint_non_loosening": projected.c3_constraint_non_loosening,
                "C4:optionality_preserved": projected.c4_optionality_preserved,
                "C5:residue_below_threshold": projected.c5_residue_below_threshold,
                "C6:branch_isolation_preserved": projected.c6_branch_isolation_preserved,
                "C7:audit_record_sufficient": projected.c7_audit_record_sufficient,
            }.items()
        )

        optionality_direction = (
            "CONTRACTED" if projected.projected_omega_r < current.omega_r
            else "PRESERVED" if projected.projected_omega_r == current.omega_r
            else "EXPANDED"
        )

        record = AdmissibilityDecisionRecord(
            proposal_id=proposal.proposal_id,
            state_ref=current.state_id,
            projection_ref=projected.projection_id,
            decision=outcome,
            constraint_results=constraint_results,
            residue_count=int(current.accumulated_residue * 10),
            review_required=outcome != GateOutcome.EXECUTE,
            optionality_direction=optionality_direction,
            transformability_status=tpi_result.status,
            denial_reason=denial_reason,
            review_prompts=self._review_prompts(outcome, projected, tpi_result),
        )

        return GateResult(
            outcome=outcome,
            projected_state=projected,
            tpi_result=tpi_result,
            decision_record=record,
            defer_record=defer_record,
            denial_reason=denial_reason,
        )

    def _route(
        self,
        proposal: Proposal,
        current: CurrentState,
        projected: ProjectedState,
        tpi: TPIResult,
    ) -> tuple[GateOutcome, Optional[str], Optional[DeferRecord]]:
        """Route to outcome based on projected state and TPI."""

        # REJECT: TPI violated — no reframing can recover
        if tpi.status == TransformabilityStatus.VIOLATED:
            return (
                GateOutcome.REJECT,
                f"Transformability violated: {tpi.violation_basis}",
                None,
            )

        # REJECT: C7 absent — no audit basis
        if not projected.c7_audit_record_sufficient:
            return (
                GateOutcome.REJECT,
                "No audit basis: proposal requires description or evidence basis.",
                None,
            )

        # DEFER: residue above threshold — C5 fails
        if not projected.c5_residue_below_threshold:
            record = DeferRecord(
                proposal_id=proposal.proposal_id,
                state_ref=current.state_id,
                defer_reason=DeferReason.RESIDUE_ABOVE_THRESHOLD,
                unresolved_conditions=(
                    "accumulated_residue_exceeds_threshold",
                ),
                residue_items=(
                    f"residue={current.accumulated_residue:.4f}>threshold=0.40",
                ),
                required_evidence=(
                    "resolve_prior_deferred_conditions",
                    "or explicit_authority_override_with_record",
                ),
                required_human_review=True,
                expiry_or_recheck_condition=(
                    "When accumulated_residue falls below 0.40 through resolved "
                    "prior deferrals or authorised clearance."
                ),
                residue_weight=0.08,
            )
            return (
                GateOutcome.DEFER,
                f"Residue {current.accumulated_residue:.4f} exceeds threshold.",
                record,
            )

        # DEFER: Ωᵣ falls below floor on projected state
        if not projected.c4_optionality_preserved:
            record = DeferRecord(
                proposal_id=proposal.proposal_id,
                state_ref=current.state_id,
                defer_reason=DeferReason.PROJECTED_STATE_FAILS_CONDITIONS,
                unresolved_conditions=(
                    f"C4:projected_Ωᵣ={projected.projected_omega_r:.4f}"
                    f"<floor({projected.effective_omega_floor:.4f})",
                ),
                residue_items=(
                    f"optionality_contraction:"
                    f"{current.omega_r:.4f}→{projected.projected_omega_r:.4f}",
                ),
                required_evidence=(
                    "proposal_with_lower_irreversibility_or_blast_radius",
                    "or explicit_authority_override_with_optionality_record",
                ),
                required_human_review=False,
                expiry_or_recheck_condition=(
                    "When a reframed proposal produces projected_Ωᵣ > effective_floor, "
                    "or when accumulated_residue decreases, raising the floor threshold."
                ),
                residue_weight=0.12,
            )
            return (
                GateOutcome.DEFER,
                (
                    f"Projected Ωᵣ={projected.projected_omega_r:.4f} falls below "
                    f"effective floor {projected.effective_omega_floor:.4f} "
                    f"(residue={current.accumulated_residue:.4f})."
                ),
                record,
            )

        # DEFER: irreversible on cold topology — C2 fails
        if not projected.c2_boundary_distance:
            record = DeferRecord(
                proposal_id=proposal.proposal_id,
                state_ref=current.state_id,
                defer_reason=DeferReason.IRREVERSIBLE_ON_COLD_TOPOLOGY,
                unresolved_conditions=(
                    f"C2:projected_Θ={projected.projected_theta:.4f}<floor",
                    "irreversible_mutation_requires_warm_topology",
                ),
                residue_items=(
                    f"topology_contraction:Θ={current.theta:.4f}→{projected.projected_theta:.4f}",
                ),
                required_evidence=(
                    "wait_for_topology_recovery",
                    "or reduce_mutation_to_reversible_form",
                ),
                required_human_review=False,
                expiry_or_recheck_condition=(
                    "When topology temperature rises above renegotiability floor, "
                    "or when proposal is revised to reversible form."
                ),
                residue_weight=0.10,
            )
            return (
                GateOutcome.DEFER,
                f"Irreversible mutation with projected Θ={projected.projected_theta:.4f} "
                f"below renegotiability floor.",
                record,
            )

        # TRANSFORM: TPI requires reframing
        if tpi.status == TransformabilityStatus.TRANSFORM_REQUIRED:
            return (
                GateOutcome.TRANSFORM,
                f"Transformability requires reframing: {tpi.violation_basis}",
                None,
            )

        # TRANSFORM: TPI defers for insufficient evidence
        if tpi.status == TransformabilityStatus.DEFER_REQUIRED:
            record = DeferRecord(
                proposal_id=proposal.proposal_id,
                state_ref=current.state_id,
                defer_reason=DeferReason.INSUFFICIENT_EVIDENCE,
                unresolved_conditions=("tpi_evidence_insufficient",),
                residue_items=(f"tpi_status:{tpi.status.value}",),
                required_evidence=("transformability_assessment_evidence",),
                required_human_review=False,
                expiry_or_recheck_condition="When TPI can be assessed with available evidence.",
                residue_weight=0.08,
            )
            return (GateOutcome.DEFER, "TPI: insufficient evidence.", record)

        # EXECUTE: all conditions pass
        return (GateOutcome.EXECUTE, None, None)

    def _review_prompts(
        self,
        outcome: GateOutcome,
        projected: ProjectedState,
        tpi: TPIResult,
    ) -> tuple[str, ...]:
        prompts: list[str] = []
        if outcome != GateOutcome.EXECUTE:
            failed = projected.failed_conditions()
            if failed:
                prompts.append(f"Projected state fails: {', '.join(failed)}")
            if tpi.status not in (
                TransformabilityStatus.PRESERVED,
                TransformabilityStatus.CONTRACTED_WITHIN_BOUNDS,
            ):
                prompts.append(f"TPI status: {tpi.status.value} — {tpi.violation_basis}")
        return tuple(prompts)
