# Podtic storage core

This module is the first storage rail for the Podtic system.

The core idea is simple:

> A podtic is stable. A section is stable. Section content is not stable.

So the database separates identity from history.

## Identity layers

### `podtics`

The canonical top-level object.

Use this for durable identity, metadata, status, domain, title, and payload summary.

### `podtic_sections`

The logical section identity.

A section has a stable key like:

```txt
mechanism:revision-identity
synthesis:first-loop
subject:etienne-decroux
comparison:physical-abstraction-vs-characterization
```

A section should survive edits. Links, comments, and graph edges can safely point to it.

### `podtic_section_revisions`

The immutable content history.

Every save creates a new row. Do not update `content_md` in place.

Only one revision per section may be current:

```sql
create unique index one_current_revision_per_section
on podtic_section_revisions(section_id)
where is_current = true;
```

This gives us rollback, diffing, audit history, and stable embedding rebuilds.

## Why embeddings attach to revisions

Embeddings represent meaning. Meaning changes when text changes.

Therefore embeddings attach to `revision_id`, not `section_id`.

Bad:

```txt
section_id -> embedding
```

Good:

```txt
section_id -> revision_id -> embedding
```

Default retrieval joins only to `is_current = true`, but published releases can hydrate old frozen revision IDs exactly.

## Release model

A release is a frozen manifest.

`podtic_releases` stores the release header. `podtic_release_sections` stores the exact section revision IDs included in the release.

That means a public podtic can be cited without the rug moving underneath it later.

## First product loop

Ship this loop first:

```txt
create podtic
  -> add sections
  -> revise section
  -> embed revision
  -> search current section
  -> publish frozen release
```

This is not the final ontology. This is the runway.

## Local order of operations

Apply migrations:

```bash
supabase db reset
```

Or manually run:

```txt
supabase/migrations/0001_podtic_core.sql
supabase/migrations/0002_podtic_revision_functions.sql
```

Then seed:

```bash
psql "$DATABASE_URL" -f scripts/seed-podtic-core.sql
```

Then inspect:

```sql
select * from podtics;
select * from podtic_sections;
select section_id, version_no, is_current, title from podtic_section_revisions order by section_id, version_no;
select * from podtic_releases;
```

## Guardrail

Do not overwrite history. The little gremlin rule is:

> Rollback is a new revision, not a deletion spell.
