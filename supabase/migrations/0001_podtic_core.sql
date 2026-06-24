-- Podtic core storage rail
-- Postgres/Supabase + pgvector + append-only section revisions

create extension if not exists pgcrypto;
create extension if not exists vector with schema extensions;

create table if not exists podtics (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  title text not null,
  domain text,
  status text not null default 'draft',
  abstract text,
  thesis text,
  payload jsonb not null default '{}'::jsonb,
  schema_version text not null default 'podtic/1.0',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint podtics_status_check check (status in ('draft', 'review', 'published', 'archived'))
);

create table if not exists podtic_sections (
  id uuid primary key default gen_random_uuid(),
  podtic_id uuid not null references podtics(id) on delete cascade,
  stable_key text not null,
  section_type text not null,
  created_at timestamptz not null default now(),
  archived_at timestamptz,
  unique (podtic_id, stable_key)
);

create table if not exists podtic_section_revisions (
  id uuid primary key default gen_random_uuid(),
  section_id uuid not null references podtic_sections(id) on delete cascade,
  version_no int not null,
  is_current boolean not null default false,
  title text,
  content_md text not null,
  content_json jsonb not null default '{}'::jsonb,
  citations jsonb not null default '[]'::jsonb,
  change_summary text,
  parent_revision_id uuid references podtic_section_revisions(id),
  schema_uri text not null,
  created_by uuid,
  created_at timestamptz not null default now(),
  valid_from timestamptz not null default now(),
  valid_to timestamptz,
  unique (section_id, version_no),
  constraint section_revision_valid_window_check check (valid_to is null or valid_to >= valid_from)
);

create unique index if not exists one_current_revision_per_section
on podtic_section_revisions(section_id)
where is_current = true;

create table if not exists section_revision_embeddings (
  revision_id uuid primary key references podtic_section_revisions(id) on delete cascade,
  embedding_model text not null,
  embedding extensions.vector(768) not null,
  created_at timestamptz not null default now()
);

create table if not exists podtic_edges (
  id uuid primary key default gen_random_uuid(),
  from_podtic_id uuid not null references podtics(id) on delete cascade,
  to_podtic_id uuid not null references podtics(id) on delete cascade,
  relation text not null,
  weight numeric(6,3),
  evidence jsonb not null default '[]'::jsonb,
  unique (from_podtic_id, to_podtic_id, relation),
  constraint podtic_edges_weight_check check (weight is null or (weight >= 0 and weight <= 1))
);

create table if not exists sources (
  id uuid primary key default gen_random_uuid(),
  source_type text not null,
  title text,
  url text,
  doi text,
  citation_text text,
  source_meta jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists podtic_source_links (
  podtic_id uuid not null references podtics(id) on delete cascade,
  source_id uuid not null references sources(id) on delete cascade,
  locator text not null default '',
  note text,
  primary key (podtic_id, source_id, locator)
);

create table if not exists podtic_releases (
  id uuid primary key default gen_random_uuid(),
  podtic_id uuid not null references podtics(id) on delete cascade,
  release_version text not null,
  release_notes text,
  released_at timestamptz not null default now(),
  released_by uuid,
  unique (podtic_id, release_version)
);

create table if not exists podtic_release_sections (
  release_id uuid not null references podtic_releases(id) on delete cascade,
  section_id uuid not null references podtic_sections(id) on delete restrict,
  revision_id uuid not null references podtic_section_revisions(id) on delete restrict,
  position int not null,
  primary key (release_id, section_id),
  unique (release_id, position)
);

create index if not exists podtics_domain_idx on podtics(domain);
create index if not exists podtics_status_idx on podtics(status);
create index if not exists podtic_sections_podtic_type_idx on podtic_sections(podtic_id, section_type);
create index if not exists podtic_section_revisions_current_idx on podtic_section_revisions(section_id, is_current);
create index if not exists podtic_edges_from_relation_idx on podtic_edges(from_podtic_id, relation);
create index if not exists podtic_edges_to_relation_idx on podtic_edges(to_podtic_id, relation);

comment on table podtics is 'Canonical podtic identity and top-level metadata.';
comment on table podtic_sections is 'Stable logical section identities across time.';
comment on table podtic_section_revisions is 'Append-only immutable section content snapshots.';
comment on table section_revision_embeddings is 'Embeddings tied to exact section revisions.';
comment on table podtic_releases is 'Immutable published podtic release manifests.';
