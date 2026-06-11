Status: public learning kernel.
 - the canonical reference runtime, see:
thunkpunks-constitutional_runtime_substrate
 - observability/evidence tooling, see:
Tracebench

This repository is an educational inspection surface, - a production governance engine, certification system, or deployment runtime.

# Admissibility Kernel
 - public learning kernel - context-to-consequence, pre-commitment admissibility governance.**

**Mebs Loghdey / Neverthought**

This repository introduces a small, inspectable kernel - asking - question before a system crosses a consequential boundary:

> **Can this proposed commitment proceed without destroying - system's future capacity - legitimate transformation?**

In - shortest public form:

> **What must remain possible after - system acts?**

Most AI systems move from context to output. More consequential systems move from context to action. Neverthought inserts a missing step:

```text
Context -> Consequence -> Admissibility -> Commitment - 
 - kernel does - optimise - speed, confidence, compliance theatre, or a more impressive-looking dashboard - someone's quarterly governance ritual. It evaluates whether a proposed transition remains admissible under pressure.

It returns - of four outcomes:

```text
EXECUTE | TRANSFORM | DEFER | REJECT - 

Each outcome produces an inspection record. - record is - a score, certification, legal conclusion, or safety guarantee. It is a structured account of - a proposed commitment - executed, reshaped, withheld, or refused.
 - 

## - this exists

As AI systems move from response generation into workflow execution, institutional decisioning, agentic automation, - operational control, - critical question changes.
 - question is no longer only:

> - the output correct?

It becomes:

> - the commitment admissible?

A system - produce a plausible answer while collapsing optionality. It - comply with a rule while making recovery harder. It - execute a valid instruction while narrowing - future space of legitimate action.
 - admissibility kernel provides a public, inspectable grammar - reasoning about that boundary.
 - 

## Human before - loop

This repository is part of Neverthought's **human-before-the-loop** doctrine.

Human-before-the-loop is - a nicer phrase - human-in-the-loop. Human-in-the-loop usually means a person approves, corrects, or overrides a process that is already moving. Human-before-the-loop means judgement enters before automation begins narrowing - field.

```text
Human-before-the-loop asks:
What must remain possible?
 - admissibility kernel asks:
Is this commitment allowed without destroying -  - 
 - human role is - to rubber-stamp machine action. - human role is to establish - interpretive, institutional, - consequence-aware conditions under which automation is allowed to start.
 - 

## - context-to-consequence pipeline

This is - public spine of - repo, - website, - the self-service build-and-learn environment:

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
   Does - commitment preserve legitimate future transformation?

6. Governed action
   EXECUTE / TRANSFORM / DEFER / REJECT

7. Inspection record
   - was this outcome reached, - what remains reviewable? - 

This repo implements a public-safe, executable learning surface - steps 3-7. - website - bench explain, simulate, - teach - full journey.
 - 

## Start here

If - are - to - repo, follow this path:

1. Read - governing question above.
2. - `examples/01_basic_gate.py`.
3. Inspect - generated decision record.
4. Compare `EXECUTE`, `TRANSFORM`, `DEFER`, - `REJECT`.
5. Read [`CLAIM_BOUNDARY.md`](CLAIM_BOUNDARY.md).
6. Read [`docs/CONTEXT_TO_CONSEQUENCE.md`](docs/CONTEXT_TO_CONSEQUENCE.md).
7. Read [`docs/HUMAN_BEFORE_THE_LOOP.md`](docs/HUMAN_BEFORE_THE_LOOP.md).
 - goal is to learn - professional grammar of consequence-aware commitment before action.
 - 

## What this - 
`admissibility-kernel` is a public inspection - learning repository - pre-commitment governance in agentic systems.

It evaluates proposed actions **before** execution - keeps three concerns separate:

1. **Local admissibility** - does this proposed action satisfy invariant conditions at - point of evaluation?
2. **Recursive viability** - can a sequence of locally admissible actions remain governable over a horizon?
3. **Transformability preservation** - does - action preserve enough recoverable future transformation, or does it foreclose futures that cannot be recovered?
 - public code uses illustrative thresholds - public proxy observables. It is designed to make - architecture legible without exposing calibrated runtime mechanics.
 - 

## What this is - 

This repository is not:
 - certification system; - regulatory compliance product; - production deployment engine; - legal, safety, or readiness determination engine; - replacement - human judgement;
- - full internal - / Semantic Ruliad implementation; - disclosure of calibrated thresholds, proof mechanics, commercial adapters, bench internals, or deployment envelopes.
 - [`CLAIM_BOUNDARY.md`](CLAIM_BOUNDARY.md) - [`docs/PUBLIC_CLAIM_CEILING.md`](docs/PUBLIC_CLAIM_CEILING.md).
 - 

## Public inspection standard

Every public artefact in this repository follows this standard:

```text
claim -> evidence object -> inspection path -> claim limit - 

A local proof object proves only - local claim attached to - A passing example does - certify a real system, authorise a deployment, or certify an institution's governance posture.
 - 

## Three named assets
 - 1. Pre-Commitment Admissibility Gate - PCAG

Evaluates a proposed transition before execution using conservative projection.
 - gate acts on **Åœ_{t+1|p}**, - conservatively projected next state under - proposal. It does - evaluate only - current state, - it does - wait until after execution.

Outputs:

```text
EXECUTE | TRANSFORM | DEFER | REJECT - 
 - 2. Recursive Viability Kernel - RVK

Evaluates whether a sequence of locally admissible transitions remains governable under recursive composition.

A system - pass every local gate - still become globally non-viable through residue compaction, authority cooling, branch contamination, optionality exhaustion, deferred-collapse masking, transform churn, or local-pass/global-fail.

Outputs:

```text
VIABLE | CONDITIONALLY_VIABLE | DEFER_REQUIRED | NON_VIABLE - 
 - 3. Transformability Preservation Invariant - TPI

Evaluates whether a transition preserves - recoverable - of legitimate future transformations above a viability floor.

Outputs:

```text
PRESERVED | CONTRACTED_WITHIN_BOUNDS | TRANSFORM_REQUIRED | DEFER_REQUIRED | VIOLATED - 
 - 

## Core observables

| Symbol | Name | Public role |
|---|---|---|
| Omega_i | Recoverable optionality | Future manoeuvre space; must stay above viability floor |
| Î˜ | Topology temperature | Renegotiability proxy; cold topology blocks irreversible mutation |
| B_iso | Branch isolation integrity | Whether counterfactual futures remain inspectable | - | Residue | Accumulated unresolved pressure from DEFER - HOLD-like outcomes |

These observables - public proxies. Calibrated runtime components - outside this repository.
 - 

## Three-state separation
 - gate enforces strict separation between:

```text -  -     Current state before - proposed transition
Åœ_{t+1|p}   Projected state after conservative proposal projection
S_{t+1|o}   Observed state after execution, if execution occurs - 

Admissibility is evaluated on **Åœ_{t+1|p}**.

Evaluating only on `S_t` is current-state auditing. Evaluating only on `S_{t+1|o}` is post-hoc forensics. Neither is pre-commitment governance.
 - 

## DEFER - TRANSFORM - first-class outcomes

**DEFER** is a controlled non-transition:

```text
DEFER(S_t, u_t) = - + DeferRecord(unresolved_conditions, required_evidence, residue) - 

No commitment boundary is crossed. - state does - execute - proposed transition. - DeferRecord states - commitment - withheld - what would resolve - 

**TRANSFORM** is a constrained reframing operator. A transformed proposal is valid only if - projected Omega_i is at least as high as - original proposal's projected Omega_i. A transform that reduces recoverable optionality is - a legitimate reframing.

Refusal, deferral, - transformation - not automation failures. They - governance outputs.
 - 

## Relation to adjacent work

Execution-boundary governance asks:

> Where does - system physically stop?

Reference-surface validation asks:

> Is - governed surface externally grounded, current, falsifiable, - institutionally legitimate?

This repository asks a different question:

> - this proposed commitment proceed without destroying - system's future capacity - legitimate transformation?
 - kernel does - merely check whether an action is authorised relative to a rule. It evaluates whether - proposed transition preserves recoverable optionality, recursive viability, - transformability under pressure.
 - [`docs/ADJACENT_WORK_BOUNDARY.md`](docs/ADJACENT_WORK_BOUNDARY.md) - [`docs/REFERENCE_SURFACE_RELATION.md`](docs/REFERENCE_SURFACE_RELATION.md).
 - 

## Install

```bash
python -m - install -e . - 

## - tests

```bash
python -m pytest - ```

Expected result:

```text
23 passed - 

## - examples

```bash
python examples/01_basic_gate.py
python examples/02_defer_when_context_is_insufficient.py
python examples/03_transform_when_branch_isolation_fails.py
python examples/04_reject_when_future_transformation_is_destroyed.py
python examples/05_valid_surface_inadmissible_commitment.py - 

## Import

```python
from neverthought_admissibility import AdmissibilityGate, Proposal, CurrentState - 
 - 

## Repository status

Version: **v0.1.0 Public Inspection Release**

This is - first public room of - Neverthought system: a learning instrument, an inspection surface, - a claim boundary - consequence-aware commitment before action.

Commercial deployments, calibrated runtime components, proof-generation mechanics, certification envelopes, private adapters, - internal policy machinery - outside this public layer.
 - 

## Search identity

**Mebs Loghdey / Neverthought - context-to-consequence pre-commitment admissibility governance.**

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
 - 

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
 - 

## Attribution

**Author:** Mebs Loghdey  
**Email:** mebsloghdey@gmail.com  
**Organisation:** Neverthought  
**Framework:** Epistemic Integrity Governance / Semantic Ruliad  



