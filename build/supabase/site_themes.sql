-- Website theme schedule: admins pick a title theme (Halloween ghost, Christmas tree, ...) for a range of dates, or
-- "none" to switch the automatic one off. Dates not covered use the automatic holiday themes.
-- Run once in the Supabase SQL editor.
create table if not exists public.site_themes (
  id bigint generated always as identity primary key,
  theme text not null,
  starts date not null,
  ends date not null,
  set_by text,
  created_at timestamptz not null default now(),
  constraint site_themes_range check (ends >= starts)
);
alter table public.site_themes enable row level security;
drop policy if exists st_read on public.site_themes;
drop policy if exists st_insert on public.site_themes;
drop policy if exists st_update on public.site_themes;
drop policy if exists st_delete on public.site_themes;
create policy st_read   on public.site_themes for select using (true);
create policy st_insert on public.site_themes for insert to authenticated with check (public.is_admin());
create policy st_update on public.site_themes for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy st_delete on public.site_themes for delete to authenticated using (public.is_admin());
grant select on public.site_themes to anon, authenticated;
grant insert, update, delete on public.site_themes to authenticated;
