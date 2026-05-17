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

    reference_surface = {
        "externally_grounded": True,
        "current": True,
        "falsifiable": True,
        "institutionally_legitimate": True,
    }

    current = CurrentState(
        omega_r=0.32,
        theta=0.28,
        b_iso="PRESERVED",
        accumulated_residue=0.10,
    )

    proposal = Proposal(
        description="Commit to irreversible enforcement using a valid but cold governance surface",
        target="enforcement_workflow",
        irreversibility=IrreversibilityClass.IRREVERSIBLE,
        blast_radius=BlastRadius.MODERATE,
        audit_basis="valid_reference_surface_demo",
    )

    result = gate.evaluate(proposal, current)

    print("reference surface valid:", all(reference_surface.values()))
    show(result)
    print("teaching point: a valid surface can still generate an inadmissible commitment under pressure.")
