-- Scoreboard sheet links: the link to each week's scoreboard sheet. This Week shows an "Open scoreboard sheet" button for it.
-- The current week's host or an admin sets it on the website (the Host tab); admins can set it for any week.
-- Run once in the Supabase SQL editor.
create table if not exists public.week_sheets (
  week int primary key,
  url text not null check (url ~* '^https?://'),
  set_by text,
  updated_at timestamptz not null default now()
);
alter table public.week_sheets enable row level security;
drop policy if exists ws_read on public.week_sheets;
drop policy if exists ws_insert on public.week_sheets;
drop policy if exists ws_update on public.week_sheets;
drop policy if exists ws_delete on public.week_sheets;
create policy ws_read   on public.week_sheets for select using (true);
create policy ws_insert on public.week_sheets for insert to authenticated with check (public.is_host() or public.is_admin());
create policy ws_update on public.week_sheets for update to authenticated using (public.is_host() or public.is_admin()) with check (public.is_host() or public.is_admin());
create policy ws_delete on public.week_sheets for delete to authenticated using (public.is_host() or public.is_admin());
grant select on public.week_sheets to anon, authenticated;
grant insert, update, delete on public.week_sheets to authenticated;
