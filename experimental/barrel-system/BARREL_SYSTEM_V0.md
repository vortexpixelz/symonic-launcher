# Barrel System v0

**Status:** experimental design specification  
**Branch:** `experimental/barrel-system`  
**Date:** 2026-06-25

## 0. Purpose

The Barrel System is the first formal layer for running multiple, inspectable analyses over the same durable evidence base.

It exists to prevent a recurring failure mode in research tooling:

```text
same corpus + changing assumptions + undocumented transformations
= conclusions that cannot be meaningfully compared
```

A barrel makes the analytical frame explicit.

> A **barrel** is a versioned, bounded interpretive lens that selects, transforms, and evaluates a defined evidence corpus without changing the underlying corpus itself.

A barrel is not a folder, a tag, a dashboard filter, or an aesthetic workspace.

It is an **analytical instrument**.

## 1. The hard boundary: initial Reddit base corpus

The initial base corpus is intentionally bounded at:

```text
2023-12-31T23:59:59
```

No record created after that timestamp belongs to the v0 base corpus.

### Why the boundary matters

The purpose of the first base is to preserve a pre-2024 social-discourse substrate for comparative analysis.

This does **not** claim that discourse before 2024 was untouched by generative AI, nor that all later discourse is unusable. It establishes a reproducible first study boundary so downstream analytical results do not silently drift with live platform behavior, changing collection conditions, or an expanding corpus.

### Corpus rule

```text
Base corpus is append-only by release.
A barrel may select from a corpus release.
A barrel may never rewrite the records in that release.
```

If source cleanup, deduplication, normalization, or re-ingestion changes what is considered canonical, create a new **corpus release**, preserve its lineage, and state the diff.

## 2. Core model

```text
source records
  -> corpus release
    -> barrel definition revision
      -> barrel run
        -> derived artifacts
          -> Podtic sections / embeddings / reports
            -> frozen release manifest
```

Each layer answers a different question.

| Layer | Question it answers |
|---|---|
| Source record | What was observed or collected? |
| Corpus release | Which exact source universe was eligible? |
| Barrel definition | Under what analytical rules was the universe viewed? |
| Barrel run | What happened when those rules executed at a known time with known software/configuration? |
| Derived artifact | What tables, features, claims, models, graphs, or outputs resulted? |
| Podtic / release | How is the work discussed, revised, cited, and frozen for review? |

## 3. Minimal Barrel object

A v0 barrel must be serializable. YAML, JSON, or a database row are all acceptable implementation formats, but it must represent these fields explicitly.

```yaml
barrel_id: reddit-politics-narrative-volatility-v0
version: 0.1.0
status: draft # draft | runnable | frozen | deprecated

identity:
  title: Reddit Politics Narrative Volatility
  summary: >
    Measures temporal changes in discourse structure and narrative concentration
    within a declared political subreddit set.
  owner: symonic

corpus:
  corpus_id: reddit-pre2024-base
  corpus_release_id: reddit-pre2024-base-r0
  temporal_boundary:
    start: null
    end_inclusive: 2023-12-31T23:59:59

selection:
  include:
    subreddits: []
    languages: [en]
    content_types: [submission, comment]
  exclude:
    deleted: true
    removed: false
    bots: unresolved
  predicates: []

representation:
  unit_of_analysis: comment # comment | submission | author-window | thread | community-window
  temporal_bin: 7d
  text_normalization_profile: reddit-clean-v0
  embedding_model: unresolved
  graph_projection: unresolved

transforms:
  - id: deduplicate
    version: unresolved
  - id: normalize-text
    profile: reddit-clean-v0
  - id: aggregate-time-window
    window: 7d

objectives:
  - id: narrative-volatility
    description: quantify distributional and semantic movement across time bins
  - id: concentration
    description: identify whether discourse concentrates around fewer recurring frames

outputs:
  - time_series
  - feature_table
  - provenance_manifest
  - podtic_sections
  - splat_report

validation:
  null_policy: unresolved
  sensitivity_checks: []
  known_biases:
    - platform sample bias
    - moderation and deletion effects
    - collection incompleteness

release:
  code_ref: unresolved
  config_hash: unresolved
  input_manifest_hash: unresolved
  output_manifest_hash: unresolved
```

### Required v0 invariants

Every barrel must declare:

1. **Which corpus release it uses**
2. **What it includes and excludes**
3. **What the unit of analysis is**
4. **What transformations it applies**
5. **What it is trying to measure or produce**
6. **How it handles unknowns, missingness, and bias**
7. **Which code/configuration revision generated its outputs**

No “default” barrel behavior should be invisible.

## 4. Barrel definition versus Barrel run

Do not collapse the recipe and the execution.

### Barrel definition

The versioned analytical recipe.

Examples:

- `reddit-politics-narrative-volatility@0.1.0`
- `reddit-finance-risk-language@0.1.0`
- `reddit-health-uncertainty-exits@0.1.0`

### Barrel run

One execution of that recipe against one fixed corpus release.

```yaml
barrel_run_id: brun_2026_06_25_001
barrel_id: reddit-politics-narrative-volatility-v0
barrel_version: 0.1.0
corpus_release_id: reddit-pre2024-base-r0
started_at: 2026-06-25T00:00:00Z
finished_at: null
code_ref: experimental/barrel-system
config_hash: sha256:unresolved
input_manifest_hash: sha256:unresolved
output_manifest_hash: sha256:unresolved
status: planned # planned | running | completed | failed | superseded
```

A changed prompt, embedding model, preprocessing rule, threshold, sampling method, or objective is a new barrel revision or a materially distinct run configuration. Do not quietly mutate a result.

## 5. Relationship to existing Launcher primitives

### Corpus release

The corpus is the raw evidence universe and its declared canonicalization state.

### Barrel

The barrel defines an analytical pathway through that evidence universe.

### Podtic

The Podtic is the durable work object that can hold planning, methods, findings, debate, and next actions around a barrel or a barrel run.

### Section revision

A Podtic section revision records changing documentation or interpretation without overwriting prior text.

### Embedding

Embeddings attach to the revision that produced them. They must not float free of the underlying text, corpus release, or barrel configuration.

### Frozen release

A frozen release can pin:

```text
barrel definition revision
+ corpus release
+ input manifest
+ code/config ref
+ selected Podtic section revisions
+ generated artifacts
```

That is the citation unit for a published result.

## 6. First worked barrel: Discourse volatility

The v0 exemplar should not begin with a giant omnibus “politics barrel.”

Start with a smaller, falsifiable barrel that exercises the entire chain:

```text
Barrel: Reddit Discourse Volatility
Scope: one declared subreddit set
Period: records at or before 2023-12-31T23:59:59
Unit: weekly community-level text distribution
Question: when does the community’s language distribution shift sharply,
and what stable/repeating frames persist across those shifts?
```

### Candidate output set

- weekly record counts
- author concentration diagnostics
- lexical / topic / embedding-distribution drift measures
- recurring phrase or frame candidates
- anomaly windows
- direct source samples for each reported anomaly
- methods and limitation section
- machine-readable provenance manifest

### What it must not claim in v0

- causal explanation for a discourse shift
- truth, falsity, or moral status of a claim
- psychological diagnosis of authors
- population-level representativeness beyond the declared source sample
- certainty where sampling, deletion, bot activity, or moderation obscure the data

## 7. Minimum evidence standard for every result

A barrel output is not publishable merely because it has a chart.

For every notable finding, store or link:

```text
finding
  -> barrel run id
  -> corpus release id
  -> selection criteria
  -> transform chain
  -> metric / model version
  -> supporting source sample or aggregate table
  -> limitation note
```

Use claim tiers where appropriate:

- **[ESTABLISHED]** directly supported by the declared source data and method
- **[PLAUSIBLE]** supported but sensitive to assumptions or incomplete coverage
- **[CONJECTURAL]** useful hypothesis, not demonstrated result
- **[ORNAMENTAL]** explanatory language that adds narrative but no evidentiary weight

## 8. Non-goals for v0

The v0 Barrel System does not attempt to solve:

- universal ontology for all research domains
- live Reddit ingestion or continuous monitoring
- perfect bot detection
- causal inference from observational text alone
- automated truth adjudication
- generalized agent orchestration
- multi-tenant permissions or commercial billing
- a polished browser product
- a full UI
- a final embedding/model standard

v0 exists to establish a strict, portable provenance contract before scaling data, models, or interface complexity.

## 9. First implementation slice

Build the smallest vertical slice that can produce one frozen, inspectable result:

```text
1. Create corpus manifest schema
2. Create barrel definition schema
3. Create barrel run manifest schema
4. Add one example barrel definition
5. Add a validator for all three manifests
6. Generate one synthetic or tiny fixture corpus release
7. Execute one simple weekly-volume / lexical-drift barrel run
8. Emit a report plus provenance manifest
9. Attach the report to a Podtic and freeze a release
```

The initial analytical method can be intentionally simple. The goal is not model sophistication. The goal is that a reviewer can answer:

> What did you look at, through which lens, using which exact rules, and what changed between this result and the last one?

## 10. Naming rule

Use names that state the observation, not the desired conclusion.

Good:

```text
reddit-discourse-volatility
reddit-finance-risk-language
reddit-health-uncertainty-exits
reddit-local-event-coordination
```

Bad:

```text
reddit-political-brainwashing
reddit-market-manipulation-detector
reddit-medical-misinformation-truth-engine
```

The barrel should describe the instrument. Conclusions belong in versioned, evidence-linked outputs.

## 11. Decision record

**Decision:** Build Barrel System v0 as a versioned interpretive layer above immutable corpus releases and beneath Podtic/SPLAT publication artifacts.

**Why:** This matches the existing launcher architecture, especially stable identities, append-only revisions, revision-level embeddings, and frozen release manifests.

**Consequence:** Every analytical result carries more metadata up front. That is intentional. The metadata is the guardrail that keeps the system from becoming a confidence machine with a pretty interface.
