-- Redraw all banners: an admin presses the button in Admin → Player banners, which adds a row here. The banner job
-- (every 10 minutes) sees a newer request than its last one and redraws every forum banner. Run once in the Supabase SQL editor.
create table if not exists public.banner_redraw (
  id         bigint generated always as identity primary key,
  at         timestamptz not null default now(),
  user_id    uuid default auth.uid() references auth.users on delete set null,
  by_player  text
);
alter table public.banner_redraw enable row level security;
drop policy if exists br_read on public.banner_redraw;
drop policy if exists br_insert on public.banner_redraw;
create policy br_read   on public.banner_redraw for select using (true);   -- the banner job reads it with the public key
create policy br_insert on public.banner_redraw for insert to authenticated with check (public.is_admin() and user_id = auth.uid());
grant select on public.banner_redraw to anon, authenticated;
grant insert on public.banner_redraw to authenticated;

notify pgrst, 'reload schema';
