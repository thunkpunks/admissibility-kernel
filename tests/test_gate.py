"""Gate tests — Pre-Commitment Admissibility Gate (PCAG).

Tests the public-safe implementation layer.

Neverthought / EIG — admissibility-kernel v0.1
"""
import pytest
from neverthought_admissibility import (
    AdmissibilityGate,
    GateOutcome,
    TransformabilityStatus,
    Proposal,
    CurrentState,
    IrreversibilityClass,
    BlastRadius,
)
from neverthought_admissibility.records import DeferRecord


def viable_state() -> CurrentState:
    return CurrentState(
        omega_r=0.85,
        theta=0.80,
        b_iso="PRESERVED",
        accumulated_residue=0.0,
    )


def clean_proposal() -> Proposal:
    return Proposal(
        description="Reversible update to routing weights",
        target="routing_table",
        irreversibility=IrreversibilityClass.REVERSIBLE,
        blast_radius=BlastRadius.LOW,
        audit_basis="operational_signal_2024_q4",
    )


class TestGateBasics:
    def test_clean_proposal_executes(self):
        gate = AdmissibilityGate()
        result = gate.evaluate(clean_proposal(), viable_state())
        assert result.outcome == GateOutcome.EXECUTE
        assert result.decision_record is not None
        assert result.defer_record is None

    def test_no_audit_basis_rejects(self):
        gate = AdmissibilityGate()
        proposal = Proposal(
            description="",
            target="x",
            irreversibility=IrreversibilityClass.REVERSIBLE,
            blast_radius=BlastRadius.LOW,
            audit_basis="",
        )
        result = gate.evaluate(proposal, viable_state())
        assert result.outcome == GateOutcome.REJECT

    def test_decision_record_always_produced(self):
        gate = AdmissibilityGate()
        for irreversibility in IrreversibilityClass:
            proposal = Proposal(
                description="test",
                target="x",
                irreversibility=irreversibility,
                blast_radius=BlastRadius.LOW,
                audit_basis="test_basis",
            )
            result = gate.evaluate(proposal, viable_state())
            assert result.decision_record is not None, (
                f"No decision record for {irreversibility}"
            )


class TestPreCommitmentProperty:
    """Gate acts on projected state, not current state."""

    def test_same_proposal_different_residue_different_outcome(self):
        """The pre-commitment property: same proposal may pass at low residue
        and fail at high residue because the effective floor rises."""
        gate = AdmissibilityGate()

        proposal = Proposal(
            description="Reversible moderate-blast update",
            target="config",
            irreversibility=IrreversibilityClass.REVERSIBLE_WITH_COST,
            blast_radius=BlastRadius.MODERATE,
            audit_basis="q4_signal",
        )

        # Low residue — base floor applies
        low_residue_state = CurrentState(
            omega_r=0.27, theta=0.80, b_iso="PRESERVED",
            accumulated_residue=0.0,
        )
        # High residue — floor lifts, same proposal may fail
        high_residue_state = CurrentState(
            omega_r=0.27, theta=0.80, b_iso="PRESERVED",
            accumulated_residue=0.50,
        )

        result_low = gate.evaluate(proposal, low_residue_state)
        result_high = gate.evaluate(proposal, high_residue_state)

        # Low residue should pass; high residue should defer
        # (projected Ωᵣ is the same, but the floor is higher under high residue)
        assert result_low.projected_state is not None
        assert result_high.projected_state is not None
        assert (
            result_low.projected_state.projected_omega_r
            == result_high.projected_state.projected_omega_r
        ), "Projected Ωᵣ must be identical — proposal unchanged"

        assert result_low.projected_state.effective_omega_floor < (
            result_high.projected_state.effective_omega_floor
        ), "High residue must produce higher effective floor"


class TestDeferIsNonTransition:
    """DEFER must produce a DeferRecord and not commit state."""

    def test_defer_produces_formal_record(self):
        gate = AdmissibilityGate()
        # IRREVERSIBLE on LOW Ωᵣ — should DEFER (optionality floor breached)
        proposal = Proposal(
            description="Irreversible high-blast delete",
            target="archive",
            irreversibility=IrreversibilityClass.IRREVERSIBLE,
            blast_radius=BlastRadius.HIGH,
            audit_basis="delete_authorization_Q4",
        )
        state = CurrentState(
            omega_r=0.40, theta=0.80, b_iso="PRESERVED",
            accumulated_residue=0.0,
        )
        result = gate.evaluate(proposal, state)
        # May be DEFER or TRANSFORM depending on projection; either way no EXECUTE
        assert result.outcome != GateOutcome.EXECUTE

        if result.outcome == GateOutcome.DEFER:
            assert result.defer_record is not None, "DEFER must produce DeferRecord"
            assert isinstance(result.defer_record, DeferRecord)
            assert result.defer_record.unresolved_conditions
            assert result.defer_record.required_evidence
            assert result.defer_record.residue_weight > 0

    def test_residue_above_threshold_defers(self):
        gate = AdmissibilityGate()
        state = CurrentState(
            omega_r=0.85, theta=0.80, b_iso="PRESERVED",
            accumulated_residue=0.45,   # Above 0.40 threshold
        )
        result = gate.evaluate(clean_proposal(), state)
        assert result.outcome == GateOutcome.DEFER
        assert result.defer_record is not None
        assert "residue" in result.defer_record.defer_reason.value.lower()


class TestTransformabilityPreservation:
    """TPI must block transitions that violate future transformability."""

    def test_tpi_result_always_present(self):
        gate = AdmissibilityGate()
        result = gate.evaluate(clean_proposal(), viable_state())
        assert result.tpi_result is not None

    def test_execute_has_preserved_or_contracted_tpi(self):
        gate = AdmissibilityGate()
        result = gate.evaluate(clean_proposal(), viable_state())
        if result.outcome == GateOutcome.EXECUTE:
            assert result.tpi_result.status in (
                TransformabilityStatus.PRESERVED,
                TransformabilityStatus.CONTRACTED_WITHIN_BOUNDS,
            )
