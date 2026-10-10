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
-- admins can also give or change ratings on behalf of any player (from the Admin tab)
create policy votes_insert on public.votes for insert to authenticated with check ((player = public.my_player() or public.is_admin()) and user_id = auth.uid());
create policy votes_update on public.votes for update to authenticated using (player = public.my_player() or public.is_admin()) with check ((player = public.my_player() or public.is_admin()) and user_id = auth.uid());
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


-- Verification animals: each player who claims a profile gets an animal no one else has. Only they and admins
-- can see it, so an admin can ask "what's your animal?" to check an account (or a host sign-up) is really theirs.
create table if not exists public.player_animals (
  user_id uuid primary key references auth.users on delete cascade,
  animal  text not null unique
);
alter table public.player_animals enable row level security;
drop policy if exists pa_read on public.player_animals;
create policy pa_read on public.player_animals for select to authenticated using (user_id = auth.uid() or public.is_admin());
grant select on public.player_animals to authenticated;

create or replace function public.give_animal(uid uuid) returns void
language plpgsql security definer set search_path = public as $$
declare a text;
begin
  if exists (select 1 from player_animals where user_id = uid) then return; end if;
  select x into a from unnest(array['Aardvark','Alpaca','Armadillo','Axolotl','Badger','Bat','Bear','Beaver','Bee','Bison','Boar','Butterfly','Camel','Cat','Chameleon','Cheetah','Chicken','Chipmunk','Cow','Crab','Crocodile','Deer','Dodo','Dog','Dolphin','Donkey','Dove','Dragon','Duck','Eagle','Elephant','Flamingo','Fox','Frog','Giraffe','Goat','Gorilla','Hamster','Hedgehog','Hippo','Horse','Hummingbird','Jellyfish','Kangaroo','Koala','Ladybug','Leopard','Lion','Lizard','Llama','Lobster','Mammoth','Monkey','Moose','Mouse','Octopus','Orangutan','Otter','Owl','Ox','Panda','Parrot','Peacock','Penguin','Pig','Poodle','Rabbit','Raccoon','Ram','Rhino','Rooster','Scorpion','Seal','Shark','Sheep','Shrimp','Skunk','Sloth','Snail','Snake','Spider','Squid','Swan','Tiger','Turkey','Turtle','T-Rex','Unicorn','Whale','Wolf','Zebra']) x
    where x not in (select animal from player_animals) order by random() limit 1;
  if a is null then  -- every animal is taken: add a number
    loop a := (array['Aardvark','Alpaca','Armadillo','Axolotl','Badger','Bat','Bear','Beaver','Bee','Bison','Boar','Butterfly','Camel','Cat','Chameleon','Cheetah','Chicken','Chipmunk','Cow','Crab'])[1 + floor(random()*20)::int] || ' ' || (10 + floor(random()*90)::int);
      exit when not exists (select 1 from player_animals where animal = a); end loop;
  end if;
  insert into player_animals (user_id, animal) values (uid, a) on conflict do nothing;
end $$;
revoke execute on function public.give_animal(uuid) from public, anon, authenticated;

create or replace function public.claims_animal() returns trigger
language plpgsql security definer set search_path = public as $$
begin perform give_animal(new.user_id); return new; end $$;
drop trigger if exists claims_animal on public.claims;
create trigger claims_animal after insert on public.claims for each row execute function public.claims_animal();

-- give animals to players who claimed before this existed
do $$ declare r record; begin for r in select user_id from public.claims loop perform public.give_animal(r.user_id); end loop; end $$;

-- After logging in on the site once, make yourself an admin (put your email in):
--   insert into public.admins (user_id) select id from auth.users where email = 'you@example.com';
--   insert into public.claims (user_id, player, status) select id, 'drand', 'approved' from auth.users where email = 'you@example.com'
--     on conflict (user_id) do update set player = excluded.player, status = 'approved';
