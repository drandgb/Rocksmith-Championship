-- Hosts can give ratings for other players (the Host tab's "Ratings for a player"), like admins can.
-- "Host" means an approved player whose name has hosted at least one week. The list of host names is kept in
-- public.hosts; it's filled in automatically whenever an admin opens the site (from the schedule on the page).
-- Needs admin_ratings.sql and rating_log.sql first. Run this once in Supabase → SQL Editor.

create table if not exists public.hosts (player text primary key);
alter table public.hosts enable row level security;
drop policy if exists hosts_read on public.hosts;
drop policy if exists hosts_insert on public.hosts;
create policy hosts_read   on public.hosts for select using (true);
create policy hosts_insert on public.hosts for insert to authenticated with check (public.is_admin());
grant select on public.hosts to anon, authenticated;
grant insert on public.hosts to authenticated;

create or replace function public.is_host() returns boolean
  language sql stable security definer set search_path = public
  as $$ select exists (select 1 from hosts h where lower(h.player) = lower(public.my_player())) $$;
grant execute on function public.is_host() to anon, authenticated;

drop policy if exists votes_insert on public.votes;
drop policy if exists votes_update on public.votes;
drop policy if exists votes_delete on public.votes;
create policy votes_insert on public.votes for insert to authenticated
  with check ((player = public.my_player() or public.is_admin() or public.is_host()) and user_id = auth.uid());
create policy votes_update on public.votes for update to authenticated
  using (player = public.my_player() or public.is_admin() or public.is_host())
  with check ((player = public.my_player() or public.is_admin() or public.is_host()) and user_id = auth.uid());
create policy votes_delete on public.votes for delete to authenticated
  using (player = public.my_player() or public.is_admin() or public.is_host());

-- hosts write to and read the ratings log too
drop policy if exists rl_read on public.rating_log;
drop policy if exists rl_insert on public.rating_log;
create policy rl_read   on public.rating_log for select to authenticated using (public.is_admin() or public.is_host());
create policy rl_insert on public.rating_log for insert to authenticated with check ((public.is_admin() or public.is_host()) and admin_id = auth.uid());
