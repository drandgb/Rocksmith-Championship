-- Difficulty ratings log: every rating a player gives, changes or removes (also when a host or admin does it for them),
-- recorded by the database itself, so nothing on the site can skip it. Admins read it in the Admin tab.
-- Run once in the Supabase SQL editor. Ratings given before this is run are added once, at the time they were last changed.
create table if not exists public.vote_log (
  id          bigint generated always as identity primary key,
  at          timestamptz not null default now(),
  player      text not null,
  week        int,
  path        smallint,
  slot        smallint,
  song        text,
  old_rating  numeric(3,1),
  new_rating  numeric(3,1),
  by_player   text            -- who made the change (differs from player when a host or admin rated for them)
);
alter table public.vote_log enable row level security;
drop policy if exists vl_read on public.vote_log;
create policy vl_read on public.vote_log for select to authenticated using (public.is_admin());
grant select on public.vote_log to authenticated;

create or replace function public.vote_log_trg() returns trigger
  language plpgsql security definer set search_path = public as $$
begin
  if tg_op = 'DELETE' then
    insert into vote_log (player, week, path, slot, song, old_rating, new_rating, by_player)
      values (old.player, old.week, old.path, old.slot, old.song, old.rating, null, my_player());
    return old;
  end if;
  if tg_op = 'UPDATE' and new.rating is not distinct from old.rating then return new; end if;
  insert into vote_log (player, week, path, slot, song, old_rating, new_rating, by_player)
    values (new.player, new.week, new.path, new.slot, new.song,
            case when tg_op = 'UPDATE' then old.rating end, new.rating, my_player());
  return new;
end $$;
drop trigger if exists votes_log on public.votes;
create trigger votes_log after insert or update or delete on public.votes
  for each row execute function public.vote_log_trg();

-- the ratings already given (only the first time this is run)
insert into public.vote_log (at, player, week, path, slot, song, new_rating)
  select updated_at, player, week, path, slot, song, rating from public.votes
  where not exists (select 1 from public.vote_log);

notify pgrst, 'reload schema';
