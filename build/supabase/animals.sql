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
