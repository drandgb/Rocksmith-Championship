-- Ratings log: every rating an admin gives, changes or removes on behalf of a player (Admin → Ratings for a player).
-- Only admins can write to it or read it.
create table if not exists public.rating_log (
  id           bigint generated always as identity primary key,
  at           timestamptz not null default now(),
  admin_id     uuid default auth.uid() references auth.users on delete set null,
  admin_player text,
  player       text not null,
  path         smallint,
  song         text,
  old_rating   numeric(3,1),
  new_rating   numeric(3,1)
);
alter table public.rating_log enable row level security;
drop policy if exists rl_read on public.rating_log;
drop policy if exists rl_insert on public.rating_log;
create policy rl_read   on public.rating_log for select to authenticated using (public.is_admin());
create policy rl_insert on public.rating_log for insert to authenticated with check (public.is_admin() and admin_id = auth.uid());
grant select, insert on public.rating_log to authenticated;
