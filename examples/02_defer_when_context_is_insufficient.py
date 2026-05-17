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
        accumulated_residue=0.45,
    )

    proposal = Proposal(
        description="Proceed with automation despite unresolved prior review items",
        target="workflow_policy",
        irreversibility=IrreversibilityClass.REVERSIBLE,
        blast_radius=BlastRadius.LOW,
        audit_basis="prior_review_incomplete",
    )

    result = gate.evaluate(proposal, current)
    show(result)

    if result.defer_record:
        print("required evidence:")
        for item in result.defer_record.required_evidence:
            print(f"- {item}")
