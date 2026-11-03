-- Tuning fixes: an admin (or a host, for their week's cards) corrects a song's tuning on a path when the Song Selection List has it wrong or missing.
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
-- hosts too (the site only offers it on the weeks they host; needs host_ratings.sql for is_host())
create policy stn_insert on public.song_tunings for insert to authenticated with check (public.is_admin() or public.is_host());
create policy stn_update on public.song_tunings for update to authenticated using (public.is_admin() or public.is_host()) with check (public.is_admin() or public.is_host());
create policy stn_delete on public.song_tunings for delete to authenticated using (public.is_admin() or public.is_host());
grant select on public.song_tunings to anon, authenticated;
grant insert, update, delete on public.song_tunings to authenticated;

-- Tuning log: every fix, capo or reset, and who made it (admins read it in the Admin tab)
create table if not exists public.tuning_log (
  id          bigint generated always as identity primary key,
  at          timestamptz not null default now(),
  user_id     uuid default auth.uid() references auth.users on delete set null,
  by_player   text,
  week        int,
  song        text,
  path        smallint,
  old_tuning  text,
  old_capo    smallint,
  new_tuning  text,
  new_capo    smallint,
  reset       boolean not null default false
);
alter table public.tuning_log enable row level security;
drop policy if exists tl_read on public.tuning_log;
drop policy if exists tl_insert on public.tuning_log;
create policy tl_read   on public.tuning_log for select to authenticated using (public.is_admin());
create policy tl_insert on public.tuning_log for insert to authenticated with check ((public.is_admin() or public.is_host()) and user_id = auth.uid());
grant select, insert on public.tuning_log to authenticated;

-- make the site see the new columns and tables right away
notify pgrst, 'reload schema';
