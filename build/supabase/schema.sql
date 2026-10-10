-- Rocksmith Championship stats site: player accounts, profile claims and song ratings.
-- Run this once in the Supabase dashboard: SQL Editor -> New query -> paste -> Run.

-- one claim per account, one account per player name; claims start as pending until an admin approves them
create table if not exists public.claims (
  user_id    uuid primary key references auth.users on delete cascade default auth.uid(),
  player     text not null unique,
  status     text not null default 'pending' check (status in ('pending','approved')),
  created_at timestamptz not null default now()
);

-- site admins (add yourself after your first login, see the bottom of this file)
create table if not exists public.admins (
  user_id uuid primary key references auth.users on delete cascade
);

-- one rating per player per challenge card (week, path 0-2 = Lead/Rhythm/Bass, slot 0-8); voting again replaces it
create table if not exists public.votes (
  player     text not null,
  week       int  not null,
  path       smallint not null check (path between 0 and 2),
  slot       smallint not null check (slot between 0 and 8),
  song       text,                -- the song when it was rated, so ratings follow a song that's moved to another level
  rating     numeric(3,1) not null check (rating between 1 and 10 and rating * 2 = floor(rating * 2)),
  user_id    uuid not null default auth.uid() references auth.users on delete cascade,
  updated_at timestamptz not null default now(),
  primary key (player, week, path, slot)
);

-- (for a project set up before the song column existed)
alter table public.votes add column if not exists song text;

create or replace function public.is_admin() returns boolean
  language sql stable security definer set search_path = public
  as $$ select exists (select 1 from admins where user_id = auth.uid()) $$;

create or replace function public.my_player() returns text
  language sql stable security definer set search_path = public
  as $$ select player from claims where user_id = auth.uid() and status = 'approved' $$;

alter table public.claims enable row level security;
alter table public.admins enable row level security;
alter table public.votes  enable row level security;

-- claims: anyone can see which names are taken; you can only claim for yourself, as pending;
-- only admins approve; you can withdraw your own pending claim, admins can remove any claim
drop policy if exists claims_read   on public.claims;
drop policy if exists claims_insert on public.claims;
drop policy if exists claims_update on public.claims;
drop policy if exists claims_delete on public.claims;
create policy claims_read   on public.claims for select using (true);
create policy claims_insert on public.claims for insert to authenticated with check (user_id = auth.uid() and status = 'pending');
create policy claims_update on public.claims for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy claims_delete on public.claims for delete to authenticated using ((user_id = auth.uid() and status = 'pending') or public.is_admin());

-- admins: you can only see your own admin row
drop policy if exists admins_read on public.admins;
create policy admins_read on public.admins for select to authenticated using (user_id = auth.uid());

-- votes: readable by everyone (the site shows averages once a week is over);
-- only an approved player can vote, and only as themselves
drop policy if exists votes_read   on public.votes;
drop policy if exists votes_insert on public.votes;
drop policy if exists votes_update on public.votes;
drop policy if exists votes_delete on public.votes;
create policy votes_read   on public.votes for select using (true);
create policy votes_insert on public.votes for insert to authenticated with check (player = public.my_player() and user_id = auth.uid());
create policy votes_update on public.votes for update to authenticated using (player = public.my_player()) with check (player = public.my_player() and user_id = auth.uid());
create policy votes_delete on public.votes for delete to authenticated using (player = public.my_player() or public.is_admin());

grant select on public.claims, public.votes to anon, authenticated;
grant insert, update, delete on public.claims, public.votes to authenticated;
grant select on public.admins to authenticated;
grant usage on schema public to anon, authenticated;
grant execute on function public.is_admin(), public.my_player() to anon, authenticated;

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

-- After logging in on the site once, make yourself an admin (put your email in):
--   insert into public.admins (user_id) select id from auth.users where email = 'you@example.com';
--   insert into public.claims (user_id, player, status) select id, 'drand', 'approved' from auth.users where email = 'you@example.com'
--     on conflict (user_id) do update set player = excluded.player, status = 'approved';
