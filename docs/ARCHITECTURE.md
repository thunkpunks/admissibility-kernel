# Architecture

The public architecture of `admissibility-kernel` is intentionally small.

It exists to make one seam inspectable:

```text
proposed commitment → conservative projection → admissibility decision → inspection record
```

---

## Core modules

```text
neverthought_admissibility/
  outcome.py      Outcome taxonomies
  projection.py   Proposal, CurrentState, ProjectedState, ObservedState
  gate.py         Pre-Commitment Admissibility Gate
  tpi.py          Transformability Preservation Invariant
  viability.py    Recursive Viability Kernel
  records.py      Inspection records
```

---

## Three-state separation

```text
S_t          Current state before proposed transition
Ŝ_{t+1|p}   Projected state after conservative proposal projection
S_{t+1|o}   Observed state after execution, if execution occurs
```

The gate evaluates **Ŝ_{t+1|p}**.

That is the architectural point. The system does not merely audit the present or explain the past. It evaluates the projected consequence of commitment before execution.

---

## Evaluation path

```text
Proposal + CurrentState
→ ProposalEvaluator.project(...)
→ ProjectedState
→ TransformabilityPreservationInvariant.assess(...)
→ AdmissibilityGate.route(...)
→ GateResult
→ AdmissibilityDecisionRecord
```

---

## Public proxy values

The numerical values in this repository are public proxies. They make the kernel runnable and teachable. They are not calibrated operational thresholds.

The protected contribution is the separation of concerns and the admissibility grammar, not the toy floor value in a demonstration file. Yes, that had to be said, because someone somewhere will absolutely confuse the two.
