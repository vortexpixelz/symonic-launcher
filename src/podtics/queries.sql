-- Podtic retrieval cookbook
-- These are query patterns for the first product loop.

-- 1. Current sections for one podtic.
select
  p.id as podtic_id,
  p.slug,
  p.title as podtic_title,
  s.id as section_id,
  s.stable_key,
  s.section_type,
  r.id as revision_id,
  r.version_no,
  r.title as section_title,
  r.content_md,
  r.citations
from podtics p
join podtic_sections s
  on s.podtic_id = p.id
 and s.archived_at is null
join podtic_section_revisions r
  on r.section_id = s.id
 and r.is_current = true
where p.slug = :slug
order by s.created_at, s.stable_key;

-- 2. Lexical search across podtic metadata and current section text.
select
  p.id as podtic_id,
  p.slug,
  p.title,
  s.id as section_id,
  r.id as revision_id,
  r.title as section_title,
  ts_rank(
    to_tsvector('english', coalesce(p.title, '') || ' ' || coalesce(p.abstract, '') || ' ' || coalesce(p.thesis, '') || ' ' || coalesce(r.content_md, '')),
    plainto_tsquery('english', :query)
  ) as rank
from podtics p
join podtic_sections s
  on s.podtic_id = p.id
 and s.archived_at is null
join podtic_section_revisions r
  on r.section_id = s.id
 and r.is_current = true
where p.status <> 'archived'
  and to_tsvector('english', coalesce(p.title, '') || ' ' || coalesce(p.abstract, '') || ' ' || coalesce(p.thesis, '') || ' ' || coalesce(r.content_md, ''))
      @@ plainto_tsquery('english', :query)
order by rank desc
limit :match_count;

-- 3. Semantic search over current section revisions.
-- Pass :query_embedding as extensions.vector(768).
select
  p.id as podtic_id,
  p.slug,
  p.title as podtic_title,
  p.domain,
  s.id as section_id,
  s.stable_key,
  s.section_type,
  r.id as revision_id,
  r.version_no,
  r.title as section_title,
  r.content_md,
  r.citations,
  1 - (e.embedding <=> :query_embedding) as similarity
from section_revision_embeddings e
join podtic_section_revisions r
  on r.id = e.revision_id
 and r.is_current = true
join podtic_sections s
  on s.id = r.section_id
 and s.archived_at is null
join podtics p
  on p.id = s.podtic_id
where p.status in ('draft', 'review', 'published')
  and (:domain is null or p.domain = :domain)
order by e.embedding <=> :query_embedding
limit :match_count;

-- 4. Hydrate graph neighbors for a podtic.
select
  e.relation,
  e.weight,
  e.evidence,
  neighbor.id,
  neighbor.slug,
  neighbor.title,
  neighbor.domain,
  neighbor.status
from podtic_edges e
join podtics neighbor
  on neighbor.id = e.to_podtic_id
where e.from_podtic_id = :podtic_id
order by coalesce(e.weight, 0) desc, e.relation;

-- 5. Release manifest with frozen revisions.
select
  rel.release_version,
  rel.released_at,
  p.slug,
  p.title as podtic_title,
  rs.position,
  s.stable_key,
  s.section_type,
  r.id as revision_id,
  r.version_no,
  r.title as section_title,
  r.content_md,
  r.citations
from podtic_releases rel
join podtics p
  on p.id = rel.podtic_id
join podtic_release_sections rs
  on rs.release_id = rel.id
join podtic_sections s
  on s.id = rs.section_id
join podtic_section_revisions r
  on r.id = rs.revision_id
where p.slug = :slug
  and rel.release_version = :release_version
order by rs.position;
