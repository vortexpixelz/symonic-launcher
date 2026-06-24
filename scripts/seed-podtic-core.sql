-- Seed script for the Podtic core loop.
-- Run after migrations 0001 and 0002.

with inserted_source as (
  insert into sources (
    source_type,
    title,
    url,
    citation_text,
    source_meta
  ) values (
    'web',
    'Draft 2020-12 JSON Schema',
    'https://json-schema.org/draft/2020-12',
    'JSON Schema Draft 2020-12 metaschema and documentation.',
    '{"authority":"json-schema.org"}'::jsonb
  )
  returning id
), inserted_podtic as (
  insert into podtics (
    slug,
    title,
    domain,
    status,
    abstract,
    thesis,
    payload,
    schema_version
  ) values (
    'podtic-storage-core',
    'Podtic Storage Core',
    'knowledge-systems',
    'draft',
    'A storage pattern for revision-safe, retrieval-native podtics.',
    'Podtics need stable logical identity, append-only section revisions, and revision-level embeddings.',
    '{"title":"Podtic Storage Core","podtic_type":"concept"}'::jsonb,
    'podtic/1.0'
  )
  returning id
), source_link as (
  insert into podtic_source_links (podtic_id, source_id, locator, note)
  select inserted_podtic.id, inserted_source.id, 'draft-2020-12', 'Schema validation source.'
  from inserted_podtic, inserted_source
  returning podtic_id, source_id
), section_identity as (
  insert into podtic_sections (podtic_id, stable_key, section_type)
  select id, 'mechanism:revision-identity', 'mechanism'
  from inserted_podtic
  returning id
), first_revision as (
  select create_podtic_section_revision(
    section_identity.id,
    'Revision Identity',
    'A podtic section is a stable logical object. Its content changes through immutable revisions, not in-place edits.',
    '{"mechanism":"stable identity plus immutable snapshots"}'::jsonb,
    jsonb_build_array(jsonb_build_object('source_id', source_link.source_id, 'locator', 'draft-2020-12')),
    'Initial mechanism draft.',
    'https://symonic.dev/schemas/podtic-section-1.0.schema.json'
  ) as revision_id
  from section_identity, source_link
), second_revision as (
  select create_podtic_section_revision(
    section_identity.id,
    'Revision Identity',
    'A podtic section is a stable logical object. Each save creates a new immutable revision, preserving audit history while keeping a current pointer for retrieval.',
    '{"mechanism":"stable identity plus immutable snapshots","retrieval_default":"current_only"}'::jsonb,
    jsonb_build_array(jsonb_build_object('source_id', source_link.source_id, 'locator', 'draft-2020-12')),
    'Clarify current pointer and audit behavior.',
    'https://symonic.dev/schemas/podtic-section-1.0.schema.json'
  ) as revision_id
  from section_identity, source_link
), synthesis_section as (
  insert into podtic_sections (podtic_id, stable_key, section_type)
  select id, 'synthesis:first-loop', 'synthesis'
  from inserted_podtic
  returning id
), synthesis_revision as (
  select create_podtic_section_revision(
    synthesis_section.id,
    'First Loop',
    'The first shippable loop is create podtic, add sections, revise section, embed revision, search current section, and publish a frozen release.',
    '{"loop":["create","section","revise","embed","search","publish"]}'::jsonb,
    '[]'::jsonb,
    'Initial synthesis draft.',
    'https://symonic.dev/schemas/podtic-section-1.0.schema.json'
  ) as revision_id
  from synthesis_section
)
select publish_podtic_release(
  inserted_podtic.id,
  'v0.1.0',
  'First frozen podtic storage release manifest.'
) as release_id
from inserted_podtic;
