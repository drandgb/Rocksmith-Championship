-- Forum post links: the link to each week's forum post. This Week shows an "Open forum post" button for it.
-- The current week's host or an admin sets it on the website (the Host tab); admins can set it for any week.
-- Run once in the Supabase SQL editor.
create table if not exists public.week_posts (
  week int primary key,
  url text not null check (url ~* '^https?://'),
  set_by text,
  updated_at timestamptz not null default now()
);
alter table public.week_posts enable row level security;
drop policy if exists wp_read on public.week_posts;
drop policy if exists wp_insert on public.week_posts;
drop policy if exists wp_update on public.week_posts;
drop policy if exists wp_delete on public.week_posts;
create policy wp_read   on public.week_posts for select using (true);
create policy wp_insert on public.week_posts for insert to authenticated with check (public.is_host() or public.is_admin());
create policy wp_update on public.week_posts for update to authenticated using (public.is_host() or public.is_admin()) with check (public.is_host() or public.is_admin());
create policy wp_delete on public.week_posts for delete to authenticated using (public.is_host() or public.is_admin());
grant select on public.week_posts to anon, authenticated;
grant insert, update, delete on public.week_posts to authenticated;
