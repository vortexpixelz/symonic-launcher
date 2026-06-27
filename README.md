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

### Symonic Deck + SPLAT publishing rail

The Deck prototype now has a typed MCORE-1 response surface plus the first SPLAT publishing toolchain: a ReportLab design-guide generator, Markdown report template, JSON Schema, example payload, validator, and an Actions artifact renderer.

Start here:

```txt
apps/deck-api/README.md
tools/README.md
```

### Research-intake reports

SPLAT reports can also hold bounded importance assessments for source documents without promoting their hypotheses into product or research claims.

```txt
reports/SYM-PUB-NEON-PERTURBATION-SHARD-001.md
reports/SYM-PUB-NEON-PERTURBATION-SHARD-001.json
```

## File map

```txt
supabase/migrations/0001_podtic_core.sql
supabase/migrations/0002_podtic_revision_functions.sql
schemas/podtic-1.0.schema.json
schemas/podtic-section-1.0.schema.json
schemas/splat-report-0.1.schema.json
src/podtics/queries.sql
src/podtics/README.md
scripts/seed-podtic-core.sql
apps/deck-api/
apps/deck-web/
tools/create_symonic_design_guide.py
tools/validate_splat_report.py
templates/splat-report.md
examples/splat-report.example.json
reports/SYM-PUB-NEON-PERTURBATION-SHARD-001.md
reports/SYM-PUB-NEON-PERTURBATION-SHARD-001.json
```

## First loop

```txt
create podtic -> add sections -> revise section -> embed revision -> search current section -> publish frozen release
```

Tiny rail first. Cathedral later.
