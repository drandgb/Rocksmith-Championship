-- Bass tabs for the Learning goals tab's "Try playing this song" (bass): a short tab admins add for each song,
-- and the song's key and scale when an admin changes them from the built-in ones.
-- Anyone can read them; only admins (rows in public.admins) can add, change or remove them.
-- Run in the Supabase SQL editor. Safe to run again: it adds the key and scale columns to an existing table.

create table if not exists public.bass_tabs (
  song       text primary key,                                  -- the song as listed on the site, e.g. 'Queen - Another One Bites the Dust'
  tab        text check (char_length(tab) <= 1500),             -- the tab, shown in a fixed-width font (empty when only the key changed)
  root       text,                                              -- changed key's root note, e.g. 'D' or 'F#' (empty = the built-in one)
  scale      text check (scale in ('major','minor','pmajor','pminor')),   -- changed scale (empty = the built-in one)
  set_by     text,                                              -- player name of the admin who saved it
  updated_at timestamptz not null default now()
);

-- for a table made before the key and scale were added
alter table public.bass_tabs add column if not exists root text;
alter table public.bass_tabs add column if not exists scale text;
alter table public.bass_tabs alter column tab drop not null;
alter table public.bass_tabs drop constraint if exists bass_tabs_scale_check;
alter table public.bass_tabs add constraint bass_tabs_scale_check check (scale in ('major','minor','pmajor','pminor'));

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
