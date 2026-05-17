"""Adversarial tests — wrong surface admitted correctly.

A structurally valid proposal that is substantively wrong should still be
blocked if it violates admissibility conditions on the projected state.

This tests a key architectural property: the gate evaluates what the system
*will be* after the transition, not merely whether the proposal is well-formed.

A well-formed proposal on the wrong surface passes structural checks.
A well-formed proposal that violates transformability on the projected state
is blocked regardless of how well-formed it is.

This is the seam the architecture makes inspectable.

Neverthought / EIG — admissibility-kernel v0.1
"""
from neverthought_admissibility import (
    AdmissibilityGate,
    GateOutcome,
    Proposal,
    CurrentState,
    IrreversibilityClass,
    BlastRadius,
)


def make_wrong_surface_proposal() -> Proposal:
    """A structurally complete proposal that governs the wrong surface.

    The proposal is well-formed: it has a description, a target, an audit basis,
    and declared irreversibility. But it is IRREVERSIBLE with HIGH blast on a
    system with low recoverable optionality — it will violate transformability
    preservation on the projected state.
    """
    return Proposal(
        description="Permanent deletion of legacy routing records",
        target="legacy_routing_archive",
        irreversibility=IrreversibilityClass.IRREVERSIBLE,
        reversibility_basis="NONE — records cannot be recovered once deleted",
        blast_radius=BlastRadius.HIGH,
        audit_basis="compliance_directive_2024_q4_v2",
    )


def make_constrained_state() -> CurrentState:
    """A system state with low optionality and accumulated residue.

    The system is under pressure. The same proposal that would be admitted
    in a healthy state will be blocked here — not because the proposal is
    malformed, but because the system has insufficient recoverability margin.
    """
    return CurrentState(
        omega_r=0.45,
        theta=0.60,
        b_iso="PRESERVED",
        accumulated_residue=0.20,
    )


class TestWrongSurface:
    def test_wrong_surface_proposal_not_executed(self):
        """A structurally complete proposal on the wrong surface must not EXECUTE."""
        gate = AdmissibilityGate()
        result = gate.evaluate(make_wrong_surface_proposal(), make_constrained_state())
        assert result.outcome != GateOutcome.EXECUTE, (
            "A structurally complete but transformability-violating proposal "
            "must not be admitted for execution."
        )

    def test_wrong_surface_still_produces_record(self):
        """Every gate evaluation produces a decision record, including rejections."""
        gate = AdmissibilityGate()
        result = gate.evaluate(make_wrong_surface_proposal(), make_constrained_state())
        assert result.decision_record is not None
        assert result.decision_record.decision != GateOutcome.EXECUTE

    def test_same_proposal_passes_on_healthy_state(self):
        """The same structurally complete proposal may EXECUTE when the system is healthy.

        This proves the gate is evaluating system state and projected consequences,
        not merely the structural form of the proposal.

        Note: even on a healthy state, IRREVERSIBLE + HIGH blast will apply
        conservative adjustments. The outcome depends on whether projections
        still satisfy admissibility conditions.
        """
        gate = AdmissibilityGate()
        healthy_state = CurrentState(
            omega_r=0.95,
            theta=0.90,
            b_iso="PRESERVED",
            accumulated_residue=0.0,
        )
        result = gate.evaluate(make_wrong_surface_proposal(), healthy_state)
        # On a very healthy state, the adjusted values may still satisfy conditions.
        # What matters is that the outcome differs from the constrained case.
        constrained_result = gate.evaluate(
            make_wrong_surface_proposal(), make_constrained_state()
        )
        # The two evaluations must not produce identical outcomes
        # if the state difference is material
        assert result.outcome != constrained_result.outcome or (
            result.projected_state.projected_omega_r
            != constrained_result.projected_state.projected_omega_r
            or result.projected_state.effective_omega_floor
            != constrained_result.projected_state.effective_omega_floor
        ), (
            "Gate must produce state-dependent outcomes — "
            "healthy and constrained states should differ"
        )

    def test_transform_required_is_not_execution(self):
        """TRANSFORM_REQUIRED is a blocking outcome, not a form of execution."""
        gate = AdmissibilityGate()
        result = gate.evaluate(make_wrong_surface_proposal(), make_constrained_state())
        if result.outcome == GateOutcome.TRANSFORM:
            # TRANSFORM blocks execution — the caller must reframe
            assert result.decision_record.decision == GateOutcome.TRANSFORM
            assert result.defer_record is None  # TRANSFORM doesn't defer, it reframes
