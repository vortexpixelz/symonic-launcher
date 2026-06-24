-- Write helpers for append-only podtic section revisions.

create or replace function create_podtic_section_revision(
  p_section_id uuid,
  p_title text,
  p_content_md text,
  p_content_json jsonb,
  p_citations jsonb,
  p_change_summary text,
  p_schema_uri text,
  p_created_by uuid default null
)
returns uuid
language plpgsql
as $$
declare
  v_current_id uuid;
  v_current_version int;
  v_new_id uuid;
begin
  select id, version_no
  into v_current_id, v_current_version
  from podtic_section_revisions
  where section_id = p_section_id
    and is_current = true
  for update;

  if v_current_id is not null then
    update podtic_section_revisions
    set is_current = false,
        valid_to = now()
    where id = v_current_id;
  else
    v_current_version := 0;
  end if;

  insert into podtic_section_revisions (
    section_id,
    version_no,
    is_current,
    title,
    content_md,
    content_json,
    citations,
    change_summary,
    parent_revision_id,
    schema_uri,
    created_by,
    valid_from
  ) values (
    p_section_id,
    v_current_version + 1,
    true,
    p_title,
    p_content_md,
    coalesce(p_content_json, '{}'::jsonb),
    coalesce(p_citations, '[]'::jsonb),
    p_change_summary,
    v_current_id,
    p_schema_uri,
    p_created_by,
    now()
  )
  returning id into v_new_id;

  update podtics
  set updated_at = now()
  where id = (
    select podtic_id
    from podtic_sections
    where id = p_section_id
  );

  return v_new_id;
end;
$$;

create or replace function rollback_podtic_section_revision(
  p_target_revision_id uuid,
  p_change_summary text default 'Rollback from historical revision',
  p_created_by uuid default null
)
returns uuid
language plpgsql
as $$
declare
  v_target podtic_section_revisions%rowtype;
begin
  select *
  into v_target
  from podtic_section_revisions
  where id = p_target_revision_id;

  if not found then
    raise exception 'Target revision not found: %', p_target_revision_id;
  end if;

  return create_podtic_section_revision(
    v_target.section_id,
    v_target.title,
    v_target.content_md,
    v_target.content_json,
    v_target.citations,
    p_change_summary,
    v_target.schema_uri,
    p_created_by
  );
end;
$$;

create or replace function publish_podtic_release(
  p_podtic_id uuid,
  p_release_version text,
  p_release_notes text default null,
  p_released_by uuid default null
)
returns uuid
language plpgsql
as $$
declare
  v_release_id uuid;
begin
  insert into podtic_releases (
    podtic_id,
    release_version,
    release_notes,
    released_by
  ) values (
    p_podtic_id,
    p_release_version,
    p_release_notes,
    p_released_by
  )
  returning id into v_release_id;

  insert into podtic_release_sections (
    release_id,
    section_id,
    revision_id,
    position
  )
  select
    v_release_id,
    s.id,
    r.id,
    row_number() over (order by s.created_at, s.stable_key)::int
  from podtic_sections s
  join podtic_section_revisions r
    on r.section_id = s.id
   and r.is_current = true
  where s.podtic_id = p_podtic_id
    and s.archived_at is null;

  update podtics
  set status = 'published',
      updated_at = now()
  where id = p_podtic_id;

  return v_release_id;
end;
$$;
