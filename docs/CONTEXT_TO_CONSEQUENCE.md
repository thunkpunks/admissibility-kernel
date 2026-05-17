# Context to Consequence

The public spine of this repository is:

```text
Context → Consequence → Admissibility → Commitment
```

Most AI systems move too quickly from context to output, and increasingly from output to action. The missing layer is consequence-aware admissibility: the discipline of asking what an action would make harder, impossible, irreversible, or illegitimate before it is allowed to happen.

---

## The conversion chain

```text
1. Context
   What is happening?

2. Interpretation
   What is being claimed, assumed, omitted, or misunderstood?

3. Proposed commitment
   What action, decision, escalation, mutation, or automation is being considered?

4. Consequence awareness
   What would this commitment close down, distort, accelerate, or make harder to reverse?

5. Admissibility decision
   Does the commitment preserve legitimate future transformation?

6. Governed action
   EXECUTE / TRANSFORM / DEFER / REJECT

7. Inspection record
   Why was this outcome reached, and what remains reviewable?
```

The repository implements a public-safe kernel for steps 3–7. The website and bench teach the larger interpretive discipline around steps 1–7.

---

## Why “context to consequence” matters

“Context” includes the situation, institutional setting, domain constraints, assumptions, omissions, ambiguity, and human judgement.

“Consequence” includes what the proposed action changes, what it closes down, what becomes harder to repair, and what future options remain.

The Neverthought move is not simply to understand context. It is to prevent context from becoming automated consequence without an admissibility check.

---

## The kernel’s role

The kernel receives a proposed commitment and a current state. It conservatively projects the consequences, evaluates public proxy observables, and returns:

```text
EXECUTE | TRANSFORM | DEFER | REJECT
```

It then produces an inspection record that makes the decision reviewable.

The record is the bridge object between learning, engineering, governance, and future commercial deployment.
