Status: public learning kernel.

For the canonical reference runtime, see:
thunkpunks-constitutional_runtime_substrate

For observability/evidence tooling, see:
Tracebench

This repository is an educational inspection surface, not a production governance engine, certification system, or deployment runtime.

# Admissibility Kernel

**A public learning kernel for context-to-consequence, pre-commitment admissibility governance.**

**Mebs Loghdey / Neverthought**

This repository introduces a small, inspectable kernel for asking one question before a system crosses a consequential boundary:

> **Can this proposed commitment proceed without destroying the systemâ€™s future capacity for legitimate transformation?**

In its shortest public form:

> **What must remain possible after the system acts?**

Most AI systems move from context to output. More consequential systems move from context to action. Neverthought inserts a missing step:

```text
Context â†’ Consequence â†’ Admissibility â†’ Commitment
```

The kernel does not optimise for speed, confidence, compliance theatre, or a more impressive-looking dashboard for someoneâ€™s quarterly governance ritual. It evaluates whether a proposed transition remains admissible under pressure.

It returns one of four outcomes:

```text
EXECUTE | TRANSFORM | DEFER | REJECT
```

Each outcome produces an inspection record. The record is not a score, certification, legal conclusion, or safety guarantee. It is a structured account of why a proposed commitment was executed, reshaped, withheld, or refused.

---

## Why this exists

As AI systems move from response generation into workflow execution, institutional decisioning, agentic automation, and operational control, the critical question changes.

The question is no longer only:

> Was the output correct?

It becomes:

> Was the commitment admissible?

A system can produce a plausible answer while collapsing optionality. It can comply with a rule while making recovery harder. It can execute a valid instruction while narrowing the future space of legitimate action.

The admissibility kernel provides a public, inspectable grammar for reasoning about that boundary.

---

## Human before the loop

This repository is part of Neverthoughtâ€™s **human-before-the-loop** doctrine.

Human-before-the-loop is not a nicer phrase for human-in-the-loop. Human-in-the-loop usually means a person approves, corrects, or overrides a process that is already moving. Human-before-the-loop means judgement enters before automation begins narrowing the field.

```text
Human-before-the-loop asks:
What must remain possible?

The admissibility kernel asks:
Is this commitment allowed without destroying it?
```

The human role is not to rubber-stamp machine action. The human role is to establish the interpretive, institutional, and consequence-aware conditions under which automation is allowed to start.

---

## The context-to-consequence pipeline

This is the public spine of the repo, the website, and the self-service build-and-learn environment:

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

This repo implements a public-safe, executable learning surface for steps 3â€“7. The website and bench explain, simulate, and teach the full journey.

---

## Start here

If you are new to the repo, follow this path:

1. Read the governing question above.
2. Run `examples/01_basic_gate.py`.
3. Inspect the generated decision record.
4. Compare `EXECUTE`, `TRANSFORM`, `DEFER`, and `REJECT`.
5. Read [`CLAIM_BOUNDARY.md`](CLAIM_BOUNDARY.md).
6. Read [`docs/CONTEXT_TO_CONSEQUENCE.md`](docs/CONTEXT_TO_CONSEQUENCE.md).
7. Read [`docs/HUMAN_BEFORE_THE_LOOP.md`](docs/HUMAN_BEFORE_THE_LOOP.md).

The goal is not to make you overstate a small Python package. review carefully. The goal is to learn the professional grammar of consequence-aware commitment before action.

---

## What this is

`admissibility-kernel` is a public inspection and learning repository for pre-commitment governance in agentic systems.

It evaluates proposed actions **before** execution and keeps three concerns separate:

1. **Local admissibility** â€” does this proposed action satisfy invariant conditions at the point of evaluation?
2. **Recursive viability** â€” can a sequence of locally admissible actions remain governable over a horizon?
3. **Transformability preservation** â€” does the action preserve enough recoverable future transformation, or does it foreclose futures that cannot be recovered?

The public code uses illustrative thresholds and public proxy observables. It is designed to make the architecture legible without exposing calibrated runtime mechanics.

---

## What this is not

This repository is not:

- a certification system;
- a regulatory compliance product;
- a production deployment engine;
- a legal, safety, or readiness determination engine;
- a replacement for human judgement;
- the full internal EIG / Semantic Ruliad implementation;
- a disclosure of calibrated thresholds, proof mechanics, commercial adapters, bench internals, or deployment envelopes.

See [`CLAIM_BOUNDARY.md`](CLAIM_BOUNDARY.md) and [`docs/PUBLIC_CLAIM_CEILING.md`](docs/PUBLIC_CLAIM_CEILING.md).

---

## Public inspection standard

Every public artefact in this repository follows this standard:

```text
claim â†’ evidence object â†’ inspection path â†’ claim limit
```

A local proof object proves only the local claim attached to it. A passing example does not certify a real system, authorise a deployment, or bless an institutionâ€™s governance posture with unsupported configuration claims.

---

## Three named assets

### 1. Pre-Commitment Admissibility Gate â€” PCAG

Evaluates a proposed transition before execution using conservative projection.

The gate acts on **Åœ_{t+1|p}**, the conservatively projected next state under the proposal. It does not evaluate only the current state, and it does not wait until after execution.

Outputs:

```text
EXECUTE | TRANSFORM | DEFER | REJECT
```

### 2. Recursive Viability Kernel â€” RVK

Evaluates whether a sequence of locally admissible transitions remains governable under recursive composition.

A system can pass every local gate and still become globally non-viable through residue compaction, authority cooling, branch contamination, optionality exhaustion, deferred-collapse masking, transform churn, or local-pass/global-fail.

Outputs:

```text
VIABLE | CONDITIONALLY_VIABLE | DEFER_REQUIRED | NON_VIABLE
```

### 3. Transformability Preservation Invariant â€” TPI

Evaluates whether a transition preserves the recoverable set of legitimate future transformations above a viability floor.

Outputs:

```text
PRESERVED | CONTRACTED_WITHIN_BOUNDS | TRANSFORM_REQUIRED | DEFER_REQUIRED | VIOLATED
```

---

## Core observables

| Symbol | Name | Public role |
|---|---|---|
| Î©áµ£ | Recoverable optionality | Future manoeuvre space; must stay above viability floor |
| Î˜ | Topology temperature | Renegotiability proxy; cold topology blocks irreversible mutation |
| B_iso | Branch isolation integrity | Whether counterfactual futures remain inspectable |
| R | Residue | Accumulated unresolved pressure from DEFER and HOLD-like outcomes |

These observables are public proxies. Calibrated runtime components are outside this repository.

---

## Three-state separation

The gate enforces strict separation between:

```text
S_t          Current state before the proposed transition
Åœ_{t+1|p}   Projected state after conservative proposal projection
S_{t+1|o}   Observed state after execution, if execution occurs
```

Admissibility is evaluated on **Åœ_{t+1|p}**.

Evaluating only on `S_t` is current-state auditing. Evaluating only on `S_{t+1|o}` is post-hoc forensics. Neither is pre-commitment governance.

---

## DEFER and TRANSFORM are first-class outcomes

**DEFER** is a controlled non-transition:

```text
DEFER(S_t, u_t) = S_t + DeferRecord(unresolved_conditions, required_evidence, residue)
```

No commitment boundary is crossed. The state does not execute the proposed transition. The DeferRecord states why commitment was withheld and what would resolve it.

**TRANSFORM** is a constrained reframing operator. A transformed proposal is valid only if its projected Î©áµ£ is at least as high as the original proposalâ€™s projected Î©áµ£. A transform that reduces recoverable optionality is not a legitimate reframing.

Refusal, deferral, and transformation are not automation failures. They are governance outputs.

---

## Relation to adjacent work

Execution-boundary governance asks:

> Where does the system physically stop?

Reference-surface validation asks:

> Is the governed surface externally grounded, current, falsifiable, and institutionally legitimate?

This repository asks a different question:

> Can this proposed commitment proceed without destroying the systemâ€™s future capacity for legitimate transformation?

The kernel does not merely check whether an action is authorised relative to a rule. It evaluates whether the proposed transition preserves recoverable optionality, recursive viability, and transformability under pressure.

See [`docs/ADJACENT_WORK_BOUNDARY.md`](docs/ADJACENT_WORK_BOUNDARY.md) and [`docs/REFERENCE_SURFACE_RELATION.md`](docs/REFERENCE_SURFACE_RELATION.md).

---

## Install

```bash
python -m pip install -e .
```

## Run tests

```bash
python -m pytest -q
```

Expected result:

```text
23 passed
```

## Run examples

```bash
python examples/01_basic_gate.py
python examples/02_defer_when_context_is_insufficient.py
python examples/03_transform_when_branch_isolation_fails.py
python examples/04_reject_when_future_transformation_is_destroyed.py
python examples/05_valid_surface_inadmissible_commitment.py
```

## Import

```python
from neverthought_admissibility import AdmissibilityGate, Proposal, CurrentState
```

---

## Repository status

Version: **v0.1.0 Public Inspection Release**

This is the first public room of the Neverthought system: a learning instrument, an inspection surface, and a claim boundary for consequence-aware commitment before action.

Commercial deployments, calibrated runtime components, proof-generation mechanics, certification envelopes, private adapters, and internal policy machinery are outside this public layer.

---

## Search identity

**Mebs Loghdey / Neverthought â€” context-to-consequence pre-commitment admissibility governance.**

Core terms:

- context-to-consequence governance
- human-before-the-loop
- pre-commitment admissibility
- admissibility kernel
- consequence-aware AI governance
- recursive viability
- transformability preservation
- recoverable optionality
- topology temperature
- governed execution
- public inspection record
- decision record governance
- epistemic integrity governance

---

## Public surfaces

Primary site:

> **https://neverthought.org**

Bench / self-service learning surface:

> **https://bench.neverthought.org**

Current public repo route:

> **https://github.com/thunkpunks/admissibility-kernel**

Profile-level identity route template:

> [`docs/GITHUB_IDENTITY_ROUTE.md`](docs/GITHUB_IDENTITY_ROUTE.md)

Website bridge:

> [`docs/WEBSITE_BRIDGE.md`](docs/WEBSITE_BRIDGE.md)

---

## Attribution

**Author:** Mebs Loghdey  
**Email:** mebsloghdey@gmail.com  
**Organisation:** Neverthought  
**Framework:** Epistemic Integrity Governance / Semantic Ruliad  


