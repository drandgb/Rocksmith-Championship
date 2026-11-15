-- Song tags: players tag a song on each path (Lead 0, Rhythm 1, Bass 2) with short words, like techniques.
-- Everyone can read them; a player with an approved claim adds and removes their own.
-- Run once in the Supabase SQL editor (needs schema.sql's my_player()).
create table if not exists public.song_tags (
  id bigint generated always as identity primary key,
  song text not null,                 -- the song's key: lowercase letters and digits of "Artist - Title"
  path smallint not null check (path between 0 and 2),
  tag text not null check (char_length(tag) between 1 and 24),
  player text,
  user_id uuid not null default auth.uid(),
  created_at timestamptz not null default now(),
  unique (song, path, tag, user_id)
);
create index if not exists song_tags_song on public.song_tags (song);
alter table public.song_tags enable row level security;
drop policy if exists sgt_read on public.song_tags;
drop policy if exists sgt_insert on public.song_tags;
drop policy if exists sgt_delete on public.song_tags;
create policy sgt_read   on public.song_tags for select using (true);
create policy sgt_insert on public.song_tags for insert to authenticated
  with check (user_id = auth.uid() and public.my_player() is not null and player = public.my_player());
create policy sgt_delete on public.song_tags for delete to authenticated using (user_id = auth.uid() or public.is_admin());
grant select on public.song_tags to anon, authenticated;
grant insert, delete on public.song_tags to authenticated;

-- Tag log: every tag added or removed, and who did it (admins read it in the Admin tab).
-- Safe to run this whole file again on an existing setup: it only adds what's missing.
create table if not exists public.tag_log (
  id        bigint generated always as identity primary key,
  at        timestamptz not null default now(),
  user_id   uuid default auth.uid() references auth.users on delete set null,
  player    text,
  song      text,                     -- the song as shown on the site ("Artist - Title")
  path      smallint,
  tag       text,
  removed   boolean not null default false
);
alter table public.tag_log enable row level security;
drop policy if exists tgl_read on public.tag_log;
drop policy if exists tgl_insert on public.tag_log;
create policy tgl_read   on public.tag_log for select to authenticated using (public.is_admin());
create policy tgl_insert on public.tag_log for insert to authenticated with check (user_id = auth.uid() and public.my_player() is not null);
grant select, insert on public.tag_log to authenticated;

-- make the site see the new table right away
notify pgrst, 'reload schema';
