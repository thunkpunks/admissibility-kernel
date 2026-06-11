# TraceClaim

TraceClaim is a minimal evidence-to-claim provenance object.

It sits between observation and admissibility:

Tracebench packet
-> TraceClaim
-> admissibility-kernel candidate
-> admissibility review

TraceClaim asks:

What can be claimed from this evidence, and what must not be claimed?

It does not decide admissibility.
It does not issue receipts.
It does not certify authority.
It does not infer intent, causality, or governance status.

TraceClaim preserves the boundary:

observation != claim
claim != commitment
commitment != authority
