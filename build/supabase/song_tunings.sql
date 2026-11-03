-- Tuning fixes: an admin corrects a song's tuning on a path when the Song Selection List has it wrong or missing.
-- An admin can also set a capo fret. The site shows the fix instead of the list's tuning, everywhere. Run once in the Supabase SQL editor.
create table if not exists public.song_tunings (
  song text not null,                 -- the song's key: "artist - title", lowercased, punctuation as spaces
  path smallint not null check (path between 0 and 2),
  tuning text not null check (char_length(tuning) between 1 and 40),
  set_by text,
  updated_at timestamptz not null default now(),
  primary key (song, path)
);
-- the capo fret, when the song needs one (safe to run again on an existing table)
alter table public.song_tunings add column if not exists capo smallint check (capo between 1 and 12);
alter table public.song_tunings enable row level security;
drop policy if exists stn_read on public.song_tunings;
drop policy if exists stn_insert on public.song_tunings;
drop policy if exists stn_update on public.song_tunings;
drop policy if exists stn_delete on public.song_tunings;
create policy stn_read   on public.song_tunings for select using (true);
create policy stn_insert on public.song_tunings for insert to authenticated with check (public.is_admin());
create policy stn_update on public.song_tunings for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy stn_delete on public.song_tunings for delete to authenticated using (public.is_admin());
grant select on public.song_tunings to anon, authenticated;
grant insert, update, delete on public.song_tunings to authenticated;
