# symonic-launcher

Modular, opcode-first launcher substrate for Linux — built on Pop Launcher IPC protocol. MCORE-1 agent skills, ternary opcode dispatch, and Symonic plugin mesh.

## Current scaffold

### Podtic storage core

The first committed storage rail is a Postgres/Supabase + pgvector core for Podtics.

It includes:

- canonical podtic records
- stable logical section identities
- append-only section revisions
- revision-level embeddings
- source links and citations
- graph edges between podtics
- frozen release manifests
- query cookbook
- seed script
- JSON Schema Draft 2020-12 schemas

Start here:

```txt
src/podtics/README.md
```

## File map

```txt
supabase/migrations/0001_podtic_core.sql
supabase/migrations/0002_podtic_revision_functions.sql
schemas/podtic-1.0.schema.json
schemas/podtic-section-1.0.schema.json
src/podtics/queries.sql
src/podtics/README.md
scripts/seed-podtic-core.sql
```

## First loop

```txt
create podtic -> add sections -> revise section -> embed revision -> search current section -> publish frozen release
```

Tiny rail first. Cathedral later.
