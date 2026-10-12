-- Claims log: every claim an admin approves, rejects or removes, with who did it and when (Admin → Claims log).
-- Written by a trigger on the claims table, so it can't be skipped or faked from the page. Only admins can read it.
-- Run this once in Supabase → SQL Editor.
create table if not exists public.claim_log (
  id           bigint generated always as identity primary key,
  at           timestamptz not null default now(),
  admin_id     uuid references auth.users on delete set null,
  admin_player text,
  player       text not null,
  action       text not null   -- approved, rejected (a pending claim deleted) or removed (an approved claim deleted)
);
alter table public.claim_log enable row level security;
drop policy if exists cl_read on public.claim_log;
create policy cl_read on public.claim_log for select to authenticated using (public.is_admin());
grant select on public.claim_log to authenticated;

create or replace function public.log_claim() returns trigger
language plpgsql security definer set search_path = public as $$
declare me text;
begin
  if not public.is_admin() then return coalesce(new, old); end if;   -- players withdrawing their own claim aren't logged
  select player into me from public.claims where user_id = auth.uid() and status = 'approved';
  if tg_op = 'UPDATE' and new.status = 'approved' and old.status is distinct from 'approved' then
    insert into public.claim_log (admin_id, admin_player, player, action) values (auth.uid(), me, new.player, 'approved');
  elsif tg_op = 'DELETE' then
    insert into public.claim_log (admin_id, admin_player, player, action)
      values (auth.uid(), me, old.player, case when old.status = 'approved' then 'removed' else 'rejected' end);
  end if;
  return coalesce(new, old);
end $$;
drop trigger if exists claims_log on public.claims;
create trigger claims_log after update or delete on public.claims for each row execute function public.log_claim();
