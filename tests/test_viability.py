"""Recursive Viability Kernel tests.

Tests that the seven named recursion failure modes are detectable
from a session trace.

Neverthought / EIG — admissibility-kernel v0.1
"""
from neverthought_admissibility import GateOutcome, ViabilityStatus
from neverthought_admissibility.viability import RecursiveViabilityKernel, SessionTrace
from neverthought_admissibility.outcome import RecursionFailureMode


def clean_trace() -> SessionTrace:
    return SessionTrace()


class TestViabilityBasic:
    def test_empty_trace_is_viable(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        report = rvk.evaluate(trace)
        assert report.viability_status == ViabilityStatus.VIABLE

    def test_clean_runs_remain_viable(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        for _ in range(5):
            trace.record_outcome(GateOutcome.EXECUTE, omega_r=0.85, theta=0.80)
        report = rvk.evaluate(trace)
        assert report.viability_status == ViabilityStatus.VIABLE
        assert report.active_failure_modes == ()


class TestRecursionFailureModes:
    def test_deferred_collapse_masking_detected(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        for _ in range(3):
            trace.record_outcome(GateOutcome.DEFER, omega_r=0.80, theta=0.70)
        assert rvk.deferred_collapse_masking(trace)
        report = rvk.evaluate(trace)
        assert RecursionFailureMode.DEFERRED_COLLAPSE_MASKING in report.active_failure_modes

    def test_optionality_exhaustion_detected(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        trace.record_outcome(GateOutcome.EXECUTE, omega_r=0.08, theta=0.70)
        assert rvk.optionality_exhaustion(trace)

    def test_residue_compaction_at_high_residue(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        trace.accumulated_residue = 0.55
        assert rvk.residue_compaction(trace)

    def test_branch_contamination_at_two_permanent_closures(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        trace.permanent_closure_count = 2
        assert rvk.branch_contamination(trace)

    def test_transform_churn_detected(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        # Three consecutive transforms with flat Ωᵣ (no improvement)
        for _ in range(3):
            trace.record_outcome(GateOutcome.TRANSFORM, omega_r=0.60, theta=0.70)
        assert rvk.transform_churn(trace)
        report = rvk.evaluate(trace)
        assert RecursionFailureMode.TRANSFORM_CHURN in report.active_failure_modes

    def test_two_failure_modes_produces_non_viable(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        # DEFERRED_COLLAPSE_MASKING
        for _ in range(3):
            trace.record_outcome(GateOutcome.DEFER, omega_r=0.80, theta=0.70)
        # RESIDUE_COMPACTION
        trace.accumulated_residue = 0.55
        report = rvk.evaluate(trace)
        assert report.viability_status == ViabilityStatus.NON_VIABLE


class TestRecoverableVsIrrecoverableBranchLoss:
    """Recoverable and irrecoverable branch losses must route differently."""

    def test_recoverable_losses_not_contamination(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        trace.recoverable_branch_count = 5   # Many recoverable losses
        trace.permanent_closure_count = 0    # No permanent closures
        assert not rvk.branch_contamination(trace)

    def test_irrecoverable_losses_trigger_contamination(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        trace.recoverable_branch_count = 0
        trace.permanent_closure_count = 2
        assert rvk.branch_contamination(trace)

    def test_recoverable_losses_in_viability_report(self):
        rvk = RecursiveViabilityKernel()
        trace = clean_trace()
        trace.recoverable_branch_count = 3
        trace.permanent_closure_count = 0
        for _ in range(2):
            trace.record_outcome(GateOutcome.EXECUTE, omega_r=0.80, theta=0.75)
        report = rvk.evaluate(trace)
        assert report.recoverable_branch_count == 3
        assert report.permanent_closure_count == 0
