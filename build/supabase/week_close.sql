-- Week close countdown: a host (or admin) sets when the current week will close; This Week and the Scoreboard count down to it.
-- Run once in the Supabase SQL editor.
create table if not exists public.week_close (
  week int primary key,
  ends_at timestamptz not null,
  set_by text,
  updated_at timestamptz not null default now()
);
alter table public.week_close enable row level security;
drop policy if exists wc_read on public.week_close;
drop policy if exists wc_insert on public.week_close;
drop policy if exists wc_update on public.week_close;
drop policy if exists wc_delete on public.week_close;
create policy wc_read   on public.week_close for select using (true);
create policy wc_insert on public.week_close for insert to authenticated with check (public.is_host() or public.is_admin());
create policy wc_update on public.week_close for update to authenticated using (public.is_host() or public.is_admin()) with check (public.is_host() or public.is_admin());
create policy wc_delete on public.week_close for delete to authenticated using (public.is_host() or public.is_admin());
grant select on public.week_close to anon, authenticated;
grant insert, update, delete on public.week_close to authenticated;
