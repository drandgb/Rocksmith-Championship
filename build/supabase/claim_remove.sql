-- Removing an approved claim, with three choices (Admin → Claims → Remove, and Admin → Removed claims):
--   * keep or delete their forum banner (kept banners keep updating every week)
--   * show or hide the ratings the player already gave (hidden ratings stay saved but don't count anywhere)
--   * if the name is claimed again (for example from a different email), give the old ratings to the new account
--     or start fresh (the old ratings are moved to votes_archive)
-- Needs claim_log.sql first. Run this once in Supabase → SQL Editor.

alter table public.votes add column if not exists hidden boolean not null default false;

-- hidden ratings are only visible to admins
drop policy if exists votes_read on public.votes;
create policy votes_read on public.votes for select using (not hidden or public.is_admin());

create table if not exists public.removed_claims (
  player       text primary key,
  hide_ratings boolean not null default false,
  carry_over   boolean not null default true,   -- if the name is claimed again, the new account gets these ratings
  keep_banner  boolean not null default true,
  removed_at   timestamptz not null default now(),
  admin_id     uuid references auth.users on delete set null
);
alter table public.removed_claims enable row level security;
drop policy if exists rc_read on public.removed_claims;
create policy rc_read on public.removed_claims for select to authenticated using (public.is_admin());
grant select on public.removed_claims to authenticated;

alter table public.removed_claims add column if not exists keep_banner boolean not null default true;

-- which removed players keep their banner: readable by anyone, so the banner builder can see it
create or replace view public.kept_banners with (security_invoker = false) as
  select player from public.removed_claims where keep_banner;
grant select on public.kept_banners to anon, authenticated;

create table if not exists public.votes_archive (like public.votes);
alter table public.votes_archive add column if not exists archived_at timestamptz not null default now();
alter table public.votes_archive enable row level security;
drop policy if exists va_read on public.votes_archive;
create policy va_read on public.votes_archive for select to authenticated using (public.is_admin());
grant select on public.votes_archive to authenticated;

-- remove an approved (or pending) claim with the two choices; admins only
drop function if exists public.remove_claim(text, boolean, boolean);
drop function if exists public.set_removed_claim(text, boolean, boolean);
create or replace function public.remove_claim(p_player text, p_hide boolean, p_carry boolean, p_keep boolean) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'admins only'; end if;
  delete from public.claims where player = p_player;            -- the claims log trigger records who did it
  insert into public.removed_claims (player, hide_ratings, carry_over, keep_banner, admin_id)
    values (p_player, p_hide, p_carry, p_keep, auth.uid())
    on conflict (player) do update set hide_ratings = excluded.hide_ratings, carry_over = excluded.carry_over,
                                       keep_banner = excluded.keep_banner, removed_at = now(), admin_id = excluded.admin_id;
  update public.votes set hidden = p_hide where player = p_player;
end $$;

-- change the choices for a removed claim later
create or replace function public.set_removed_claim(p_player text, p_hide boolean, p_carry boolean, p_keep boolean) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'admins only'; end if;
  update public.removed_claims set hide_ratings = p_hide, carry_over = p_carry, keep_banner = p_keep where player = p_player;
  update public.votes set hidden = p_hide where player = p_player;
end $$;
grant execute on function public.remove_claim(text, boolean, boolean, boolean), public.set_removed_claim(text, boolean, boolean, boolean) to authenticated;

-- when a removed name is approved again: hand over the old ratings (shown again) or archive them and start fresh
create or replace function public.reclaim_ratings() returns trigger
language plpgsql security definer set search_path = public as $$
declare rc record;
begin
  if new.status = 'approved' and old.status is distinct from 'approved' then
    select * into rc from public.removed_claims where player = new.player;
    if found then
      if rc.carry_over then
        update public.votes set hidden = false where player = new.player;
      else
        insert into public.votes_archive select v.*, now() from public.votes v where v.player = new.player;
        delete from public.votes where player = new.player;
      end if;
      delete from public.removed_claims where player = new.player;
    end if;
  end if;
  return new;
end $$;
drop trigger if exists claims_reclaim on public.claims;
create trigger claims_reclaim after update on public.claims for each row execute function public.reclaim_ratings();
