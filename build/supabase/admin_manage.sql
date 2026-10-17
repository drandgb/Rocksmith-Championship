-- Admins managed from the site (Admin → Admins): any admin can make a player with an approved claim an admin, or
-- remove an admin, except the owner (drand), who can't be removed. Every change is written to the Claims log.
-- Also marks the older approvals in the Claims log (from claim_log_backfill.sql) as approved by drand, the only
-- admin back then.
-- Needs claim_log.sql first. Run this once in Supabase → SQL Editor.

alter table public.admins add column if not exists owner    boolean not null default false;
alter table public.admins add column if not exists added_at timestamptz;
alter table public.admins add column if not exists added_by uuid references auth.users on delete set null;

-- the owner: the admin whose approved claim is drand
update public.admins set owner = true
where user_id in (select user_id from public.claims where player = 'drand' and status = 'approved');

-- the admins, with their player names (admins only)
create or replace function public.list_admins()
returns table (player text, owner boolean, added_at timestamptz, added_by text, is_me boolean)
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'admins only'; end if;
  return query
    select c.player, a.owner, a.added_at, cb.player, a.user_id = auth.uid()
    from admins a
    left join claims c  on c.user_id = a.user_id and c.status = 'approved'
    left join claims cb on cb.user_id = a.added_by and cb.status = 'approved'
    order by a.owner desc, c.player;
end $$;
grant execute on function public.list_admins() to authenticated;

-- make a player an admin (p_on = true) or remove them (false); admins only, and never the owner
create or replace function public.set_admin(p_player text, p_on boolean)
returns void
language plpgsql security definer set search_path = public as $$
declare target uuid; me text;
begin
  if not public.is_admin() then raise exception 'admins only'; end if;
  select user_id into target from claims where player = p_player and status = 'approved';
  if target is null then raise exception '% has no approved claim', p_player; end if;
  select player into me from claims where user_id = auth.uid() and status = 'approved';
  if p_on then
    if exists (select 1 from admins where user_id = target) then return; end if;
    insert into admins (user_id, added_at, added_by) values (target, now(), auth.uid());
    insert into claim_log (admin_id, admin_player, player, action) values (auth.uid(), me, p_player, 'admin_added');
  else
    if exists (select 1 from admins where user_id = target and owner) then raise exception 'the owner can''t be removed'; end if;
    delete from admins where user_id = target;
    if found then insert into claim_log (admin_id, admin_player, player, action) values (auth.uid(), me, p_player, 'admin_removed'); end if;
  end if;
end $$;
grant execute on function public.set_admin(text, boolean) to authenticated;

-- older approvals: approved by drand, the only admin before the log started
update public.claim_log set admin_player = 'drand' where action = 'approved_before_log' and admin_player is null;
