-- Scoreboard checks: issues a host or an admin dismissed (not a real problem). The row stays in the checks, greyed out
-- and not counted, and the Scoreboard fix log shows who dismissed it and when. Run once in the Supabase SQL editor.
create table if not exists public.check_dismiss (
  key        text primary key check (char_length(key) <= 600),
  kind       text not null check (char_length(kind) <= 20),
  week       int,
  label      text check (char_length(label) <= 400),
  at         timestamptz not null default now(),
  user_id    uuid default auth.uid() references auth.users on delete set null,
  by_player  text
);
alter table public.check_dismiss enable row level security;
drop policy if exists cd_read   on public.check_dismiss;
drop policy if exists cd_insert on public.check_dismiss;
drop policy if exists cd_delete on public.check_dismiss;
create policy cd_read   on public.check_dismiss for select to authenticated using (true);
create policy cd_insert on public.check_dismiss for insert to authenticated
  with check (user_id = auth.uid() and (public.is_admin() or by_player = public.my_player()));
create policy cd_delete on public.check_dismiss for delete to authenticated
  using (public.is_admin() or user_id = auth.uid());
grant select, insert, delete on public.check_dismiss to authenticated;

notify pgrst, 'reload schema';
