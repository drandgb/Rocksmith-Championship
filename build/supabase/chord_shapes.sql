-- Chord fixes for the Learning goals chord pictures: admins can change a chord's shape in the chord diagram maker,
-- and everyone sees the fixed shape. Run once in the Supabase SQL editor.
create table if not exists public.chord_shapes (
  chord       text primary key,          -- like Am7
  frets       text not null,             -- low E to high e, comma-separated: x = muted, 0 = open
  fingers     text not null default '------',   -- one character per string: 1-4, T or -
  start       int  not null default 1,   -- the first fret shown
  set_by      text,
  updated_at  timestamptz not null default now()
);
alter table public.chord_shapes enable row level security;
drop policy if exists cs_read on public.chord_shapes;
drop policy if exists cs_write on public.chord_shapes;
create policy cs_read  on public.chord_shapes for select to anon, authenticated using (true);
create policy cs_write on public.chord_shapes for all to authenticated using (public.is_admin()) with check (public.is_admin());
grant select on public.chord_shapes to anon, authenticated;
grant insert, update, delete on public.chord_shapes to authenticated;

notify pgrst, 'reload schema';
