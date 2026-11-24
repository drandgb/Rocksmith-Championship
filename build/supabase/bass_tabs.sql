-- Bass tabs for the Learning goals tab's "Try playing this song" (bass): a short tab admins add for each song.
-- Anyone can read them; only admins (rows in public.admins) can add, change or remove them.
-- Run once in the Supabase SQL editor.

create table if not exists public.bass_tabs (
  song       text primary key,                                  -- the song as listed on the site, e.g. 'Queen - Another One Bites the Dust'
  tab        text not null check (char_length(tab) <= 1500),    -- the tab as typed, shown in a fixed-width font
  set_by     text,                                              -- player name of the admin who saved it
  updated_at timestamptz not null default now()
);

alter table public.bass_tabs enable row level security;

drop policy if exists "bass tabs are public" on public.bass_tabs;
create policy "bass tabs are public" on public.bass_tabs
  for select using (true);

drop policy if exists "admins edit bass tabs" on public.bass_tabs;
create policy "admins edit bass tabs" on public.bass_tabs
  for all to authenticated
  using (exists (select 1 from public.admins a where a.user_id = auth.uid()))
  with check (exists (select 1 from public.admins a where a.user_id = auth.uid()));

grant select on public.bass_tabs to anon, authenticated;
grant insert, update, delete on public.bass_tabs to authenticated;

notify pgrst, 'reload schema';
