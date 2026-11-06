-- Big improvements already congratulated: when an admin or host copies a player's Big improvements message (Messages
-- for players), the songs it covered are saved here, so everyone who posts sees it as copied, and a later improvement
-- that week gets a new message with only the new songs. Run once in the Supabase SQL editor.
create table if not exists public.improve_posted (
  week       int  not null,
  item       text not null,   -- player|path|song, lowercase
  at         timestamptz not null default now(),
  user_id    uuid default auth.uid() references auth.users on delete set null,
  by_player  text,
  primary key (week, item)
);
alter table public.improve_posted enable row level security;
drop policy if exists ip_read on public.improve_posted;
drop policy if exists ip_insert on public.improve_posted;
create policy ip_read   on public.improve_posted for select to authenticated using (public.is_admin() or public.is_host());
create policy ip_insert on public.improve_posted for insert to authenticated with check ((public.is_admin() or public.is_host()) and user_id = auth.uid());
grant select, insert on public.improve_posted to authenticated;

notify pgrst, 'reload schema';
