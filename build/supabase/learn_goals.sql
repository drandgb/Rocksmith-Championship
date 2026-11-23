-- Learning goals: the ones each player has checked off in the Learning goals tab of their profile. Only you can see or change your own.
-- Run once in the Supabase SQL editor.
create table if not exists public.learn_goals (
  user_id  uuid not null default auth.uid() references auth.users on delete cascade,
  item     text not null,   -- the target's key, like cowboy/maj/A
  done_at  timestamptz not null default now(),
  primary key (user_id, item)
);
alter table public.learn_goals enable row level security;
drop policy if exists lg_read on public.learn_goals;
drop policy if exists lg_insert on public.learn_goals;
drop policy if exists lg_delete on public.learn_goals;
create policy lg_read   on public.learn_goals for select to authenticated using (user_id = auth.uid());
create policy lg_insert on public.learn_goals for insert to authenticated with check (user_id = auth.uid());
create policy lg_delete on public.learn_goals for delete to authenticated using (user_id = auth.uid());
grant select, insert, delete on public.learn_goals to authenticated;

notify pgrst, 'reload schema';
