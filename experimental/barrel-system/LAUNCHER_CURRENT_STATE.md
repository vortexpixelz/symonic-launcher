# Symonic Launcher — Current Development State

**Capture date:** 2026-06-25  
**Branch:** `experimental/barrel-system`  
**Purpose:** establish an evidence-based baseline before the Barrel System is designed or integrated.

## Executive read

`symonic-launcher` is currently a **research substrate**, not yet a finished desktop launcher or browser product.

Its implemented core is three connected rails:

1. **Podtic storage core**: a Postgres/Supabase + pgvector schema for durable, revisioned research artifacts.
2. **Symonic Deck**: a typed response contract and FastAPI adapter that renders MCORE-1 validation results as structured document segments.
3. **SPLAT publishing rail**: schemas, templates, validation, and rendering infrastructure for publishable reports.

The repo already contains the beginnings of a coherent provenance-first system. It does **not yet** show a Barrel System, semantic silo browser, generalized launcher command surface, or an end-to-end product loop connecting Podtics, Deck, and publishing through one user-facing interface.

## What is present

### 1. Podtic storage core

The first committed persistence rail separates durable identity from changing content:

```text
podtic identity
  -> stable logical section identity
    -> append-only section revisions
      -> revision-level embeddings
```

Implemented design commitments:

- canonical Podtic records
- stable logical section identities
- immutable section revision history
- embeddings attached to revisions, not sections
- source links and citations
- graph edges between Podtics
- frozen release manifests
- Postgres/Supabase migrations, schemas, seed material, and query cookbook

The governing invariant is:

> A Podtic is stable. A section is stable. Section content is not stable.

This makes rollback, citation, diffing, and reproducible retrieval first-class rather than cleanup tasks.

### 2. Symonic Deck API

`apps/deck-api` is a Python/FastAPI service that exposes an MCORE-1 validation operation.

Current surface:

```text
GET  /api/v1/health
POST /api/v1/mcore/validate-pattern
GET  /api/v1/openapi.json
GET  /api/v1/docs
GET  /lab
```

The response contract emits typed segments:

```text
FIELD  = contextual input
PROOF  = positive result
CUT    = constraint, error, or invalidity
```

Each segment carries a label, raw text, semantic role, and provenance record. Display color is explicitly treated as a rendering convention, never as evidence or truth logic.

The current implemented operation validates an MCORE metrical pattern by parsing trits, checking overflow, constructing a constituent tree, and returning an explicit `valid`, `invalid`, or `overflow` status.

### 3. Deck front-end direction

The repository documents a TypeScript document surface in `apps/deck-web`, intended as the polished client, with a Gradio lab mounted at `/lab` as a rapid research workbench.

The specified split is:

```text
TypeScript document surface -> FastAPI Deck adapter -> mcore-py
```

This is a useful product boundary: the client renders a known structured state; it does not infer facts from prose.

### 4. SPLAT publishing rail

The repository also contains a publishing/tooling track for SPLAT reports:

- JSON Schema for report payloads
- example report payload
- Markdown report template
- validator
- ReportLab design-guide generator
- GitHub Actions artifact renderer

This indicates that reporting and artifact production are already being treated as product primitives, not afterthoughts.

## Current first-loop, as documented

```text
create podtic
  -> add sections
  -> revise section
  -> embed revision
  -> search current section
  -> publish frozen release
```

This is the strongest concrete loop in the codebase today.

## What is not yet evidenced in this repository

The following should be treated as **design targets**, not completed capabilities, until implementation evidence is added:

- Barrel System domain model
- barrels as reusable interpretive lenses over a common corpus
- pre-2024 Reddit corpus ingestion or storage
- semantic-silo browser
- browser/network/privacy substrate
- launcher command registry or runtime orchestration
- generalized MCORE operation routing beyond metrical-pattern validation
- Podtic-to-Deck-to-SPLAT end-to-end UI workflow
- authentication, permissions, multi-user controls, or deployment topology
- production readiness, benchmarks, or CI test status

## Design implications for Barrel System

The existing architecture already gives Barrel System four useful primitives:

| Existing primitive | Barrel System implication |
|---|---|
| Stable Podtic identity | A barrel can reference a durable research object without pinning mutable text. |
| Append-only section revisions | Barrel interpretations can be revised without erasing prior analysis. |
| Revision-level embeddings | Similarity and retrieval can be tied to the exact version of the source or interpretation. |
| Frozen releases | A published barrel result can cite an exact corpus/definition/revision set. |

The Barrel System should therefore begin as a **versioned interpretive layer over evidence**, not as a loose tag, folder, or dashboard filter.

## Working definition, provisional

> A **barrel** is a versioned, bounded interpretive lens that selects, transforms, and evaluates a defined evidence corpus without changing the underlying corpus itself.

A barrel should eventually make explicit:

- corpus boundary
- temporal boundary
- inclusion/exclusion rules
- feature or representation choices
- transformation pipeline
- scoring or analytical objectives
- outputs and release manifest
- provenance for every derived claim

## Next artifact

Create `experimental/barrel-system/BARREL_SYSTEM_V0.md` with:

1. the minimal barrel object model;
2. the fixed corpus boundary of **2023-12-31 23:59:59** for the initial Reddit base;
3. the relationship among corpus, barrel, Podtic, section revision, embedding, and frozen release;
4. one worked example barrel; and
5. explicit non-goals for v0.

## Guardrail

Do not treat an interpretive barrel as a neutral container.

A barrel is an analytical instrument. Its inclusion rules, transformations, and objectives influence what becomes visible. Those choices must be versioned and reviewable alongside the results.
