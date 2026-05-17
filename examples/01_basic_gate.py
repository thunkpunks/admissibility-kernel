from neverthought_admissibility import (
    AdmissibilityGate,
    Proposal,
    CurrentState,
    IrreversibilityClass,
    BlastRadius,
)


def show(result):
    record = result.decision_record
    projected = result.projected_state
    print(f"outcome: {result.outcome.value}")
    print(f"projected Ωᵣ: {projected.projected_omega_r}")
    print(f"projected Θ: {projected.projected_theta}")
    print(f"TPI: {result.tpi_result.status.value}")
    print(f"review required: {record.review_required}")
    if result.denial_reason:
        print(f"reason: {result.denial_reason}")
    if record.review_prompts:
        print("review prompts:")
        for prompt in record.review_prompts:
            print(f"- {prompt}")


if __name__ == "__main__":
    gate = AdmissibilityGate()

    current = CurrentState(
        omega_r=0.85,
        theta=0.80,
        b_iso="PRESERVED",
        accumulated_residue=0.0,
    )

    proposal = Proposal(
        description="Reversible update to routing weights",
        target="routing_table",
        irreversibility=IrreversibilityClass.REVERSIBLE,
        blast_radius=BlastRadius.LOW,
        audit_basis="public_demo_signal",
    )

    result = gate.evaluate(proposal, current)
    show(result)
