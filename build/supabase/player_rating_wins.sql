-- A player's own rating always wins (Host tab → "Ratings for a player").
-- Once a player rates a song themselves, hosts and admins can't change or remove that rating; only the player can.
-- Ratings a host or admin gave for the player stay editable until the player rates the song themselves.
-- "Their own" means the rating was saved from the player's own login (or from a login they've since deleted).
-- Run this once in Supabase → SQL Editor. Safe to run again.

create or replace function public.protect_own_rating() returns trigger
language plpgsql security definer set search_path = public as $$
declare owner uuid;
begin
  -- only someone changing another player's rating directly from the page; the claim-removal steps are left alone
  if auth.uid() is null or pg_trigger_depth() > 1 then return coalesce(new, old); end if;
  if lower(old.player) = lower(coalesce(public.my_player(), '')) then return coalesce(new, old); end if;
  if tg_op = 'UPDATE' and new.user_id is distinct from auth.uid() then return new; end if;   -- e.g. hiding a removed claim's ratings
  select user_id into owner from claims where lower(player) = lower(old.player) and status = 'approved';
  if old.user_id is null or old.user_id = owner then
    raise exception '% rated this song themselves, so only they can change it.', old.player;
  end if;
  return coalesce(new, old);
end $$;

drop trigger if exists votes_protect_own on public.votes;
create trigger votes_protect_own before update or delete on public.votes
  for each row execute function public.protect_own_rating();
