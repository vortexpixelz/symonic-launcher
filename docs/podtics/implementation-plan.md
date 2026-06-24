# Podtic implementation plan

Issue: #2

## Objective

Turn the Podtic architecture into an executable storage loop.

The first loop is deliberately narrow:

```txt
create podtic -> add sections -> revise section -> embed revision -> search current section -> publish frozen release
```

## Phase 1: Storage rail

- [x] Add core migration.
- [x] Add section revision write functions.
- [x] Add release manifest function.
- [x] Add JSON schemas.
- [x] Add query cookbook.
- [x] Add seed script.
- [x] Add docs.

## Phase 2: Application service

Build a small service layer around the SQL rail.

Required methods:

- `createPodtic(input)`
- `createSection(input)`
- `reviseSection(input)`
- `rollbackSection(input)`
- `publishPodtic(input)`
- `searchCurrentSections(input)`
- `hydrateRelease(input)`

## Phase 3: Embedding worker

Add a worker that accepts a `revision_id`, computes an embedding, and writes to `section_revision_embeddings`.

Do not compute embeddings from floating current text without writing the exact revision ID.

## Phase 4: Validation

Add JSON Schema validation before writing podtic payloads or section revision `content_json`.

Each stored revision must include the exact `schema_uri` it validated against.

## Phase 5: Tests

Add tests for:

- one current revision per section
- update creates a new row
- rollback creates a new row
- release freezes exact revisions
- search ignores archived sections
- semantic search returns revision and parent podtic IDs

## Design note

This should stay boring at the storage layer.

The weird magic belongs in Podtic authoring, retrieval, and synthesis. The database is the stone floor under the ritual circle.
