-- Scoreboard checks, "Requires manual correction": corrected entries from the Score Assistant that a fetch skipped because
-- they're lower than what the scoreboard sheet has (for example a streak that was misread too high the first time).
-- The website saves them when a fetch reports them; each disappears once the sheet has the corrected values.
-- Run once in the Supabase SQL editor.
create table if not exists public.score_fix (
  key        text primary key check (char_length(key) <= 600),
  week       int not null,
  path       int not null check (path between 0 and 2),
  level      text check (char_length(level) <= 60),
  song       text check (char_length(song) <= 300),
  player     text not null check (char_length(player) <= 80),
  sheet      jsonb,
  fetched    jsonb,
  by_hand    boolean not null default false,
  at         timestamptz not null default now(),
  user_id    uuid default auth.uid() references auth.users on delete set null,
  by_player  text
);
alter table public.score_fix enable row level security;
drop policy if exists sf_read   on public.score_fix;
drop policy if exists sf_insert on public.score_fix;
create policy sf_read   on public.score_fix for select to authenticated using (true);
create policy sf_insert on public.score_fix for insert to authenticated
  with check (user_id = auth.uid() and (public.is_admin() or by_player = public.my_player()));
grant select, insert on public.score_fix to authenticated;

notify pgrst, 'reload schema';
