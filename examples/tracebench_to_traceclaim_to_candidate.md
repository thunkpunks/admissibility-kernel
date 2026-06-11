# Example: Tracebench packet -> TraceClaim -> Admissibility Candidate

1. Tracebench observes repeated retry behavior after tool failure.

2. TraceClaim bounds the claim:

- supports: observable recurrence after tool failure
- does_not_support: intent, root cause, admissibility, safety
- omissions: no production logs, no user interview, no runtime receipt
- caveats: trace-only evidence
- downstream_use: may be submitted as context for admissibility review

3. Admissibility candidate references tc_001.

The TraceClaim supports the candidate. It does not decide the candidate.
