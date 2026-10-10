-- Host sign-ups: a verified host (an approved player who has hosted before) signs up for an upcoming week,
-- or an admin signs someone up. One host per week. The schedule sheet stays the source of truth: once the
-- sheet names a host for that week, the site shows the sheet's host.
create table if not exists public.host_signups (
  week       int primary key,
  player     text not null,
  user_id    uuid not null default auth.uid() references auth.users on delete cascade,
  created_at timestamptz not null default now()
);
alter table public.host_signups enable row level security;
drop policy if exists hs_read   on public.host_signups;
drop policy if exists hs_insert on public.host_signups;
drop policy if exists hs_delete on public.host_signups;
create policy hs_read   on public.host_signups for select using (true);
create policy hs_insert on public.host_signups for insert to authenticated with check (user_id = auth.uid() and (player = public.my_player() or public.is_admin()));
create policy hs_delete on public.host_signups for delete to authenticated using (player = public.my_player() or public.is_admin());
grant select on public.host_signups to anon, authenticated;
grant insert, delete on public.host_signups to authenticated;
