---
artifact_id: SYM-INT-YYYY-NN
artifact_type: splat_report
title: "Specific noun phrase"
handling: INTERNAL # PUBLIC | PRIVATE | INTERNAL
status: stage # stage | review-ready | sent | released | retired
owner: ""
version: v0.1
created_at: "YYYY-MM-DDThh:mm:ssZ"
updated_at: "YYYY-MM-DDThh:mm:ssZ"
splat_mode: horizon # horizon | vanishing_point | orthogonal | transversal | depth | atmospheric | value
claim_tier: plausible # established | plausible | conjectural | ornamental
recipient: ""
decision_horizon: ""
receipt_manifest: ""
next_action: ""
---

# {{ title }}

> **Decision thesis:** Write the one sentence this artifact needs its reader to act on.

| Field | Value |
|---|---|
| Handling | `{{ handling }}` |
| SPLAT mode | `{{ splat_mode }}` |
| Status | `{{ status }}` |
| Version | `{{ version }}` |
| Decision horizon | `{{ decision_horizon }}` |
| Receipt manifest | `{{ receipt_manifest }}` |

## S — Signal

What changed, matters, or needs attention? State the signal in one reader-facing sentence.

## P — Proof

What direct receipt, observation, method, or reproducible result supports the signal?

- Receipt:
- Method / retrieval context:
- Result:
- Claim tier:

## L — Limit

What remains uncertain, excluded, contradicted, or not established?

- Strongest counterpoint:
- Known blind spot:
- What this does **not** prove:

## A — Action

What should happen next, who owns it, and by when?

- Owner:
- Action:
- Decision horizon:
- Release / hold / revise condition:

## T — Trace

How can the reader return to the source, version, and surrounding context?

```text
artifact_id:
version:
source path / URL / commit:
receipt manifest:
related podtics:
related issues / PRs:
```

---

## Mode lens

### Horizon SPLAT
State the landscape, watch window, and change since the last scan.

### Vanishing-Point SPLAT
Write the one decision question every input must converge on.

### Orthogonal SPLAT
Expose the source-to-claim path. Make the proof line inspectable.

### Transversal SPLAT
Freeze the comparison dimensions. Match the rows before interpreting differences.

### Depth SPLAT
Separate foreground action, middle-ground mechanism, and background context.

### Atmospheric SPLAT
Calibrate confidence, coverage, noise, and the trigger for a closer look.

### Value SPLAT
Name the highlight, midtone, core shadow, and cast shadow of the proposed action.
