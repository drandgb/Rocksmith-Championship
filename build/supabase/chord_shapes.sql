-- Chord shapes for the Learning goals tab: admins' fixes to the built-in chord pictures.
-- Anyone can read them; only admins (rows in public.admins) can add, change or remove them.
-- Run once in the Supabase SQL editor.

create table if not exists public.chord_shapes (
  chord      text primary key,                  -- e.g. 'Am', 'Cmaj7'
  frets      text not null,                     -- low E to high e, comma separated: x = muted, 0 = open, e.g. 'x,3,2,0,1,0'
  fingers    text not null default '------',    -- one character per string: 1-4, T (thumb) or - (none)
  start      int  not null default 1 check (start between 1 and 20),
  set_by     text,                              -- player name of the admin who saved it
  updated_at timestamptz not null default now()
);

alter table public.chord_shapes enable row level security;

drop policy if exists "chord shapes are public" on public.chord_shapes;
create policy "chord shapes are public" on public.chord_shapes
  for select using (true);

drop policy if exists "admins edit chord shapes" on public.chord_shapes;
create policy "admins edit chord shapes" on public.chord_shapes
  for all to authenticated
  using (exists (select 1 from public.admins a where a.user_id = auth.uid()))
  with check (exists (select 1 from public.admins a where a.user_id = auth.uid()));

grant select on public.chord_shapes to anon, authenticated;
grant insert, update, delete on public.chord_shapes to authenticated;

notify pgrst, 'reload schema';
