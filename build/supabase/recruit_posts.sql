-- Recruitment posts: links to the recruitment posts already made (Reddit and other places), so admins can see
-- where and when the championship was last advertised. Admins add and remove them on the website (the Admin tab).
-- Run once in the Supabase SQL editor.
create table if not exists public.recruit_posts (
  id bigint generated always as identity primary key,
  url text not null unique check (url ~* '^https?://'),
  week int,
  set_by text,
  created_at timestamptz not null default now()
);
alter table public.recruit_posts enable row level security;
drop policy if exists rp_read on public.recruit_posts;
drop policy if exists rp_insert on public.recruit_posts;
drop policy if exists rp_delete on public.recruit_posts;
create policy rp_read   on public.recruit_posts for select to authenticated using (public.is_admin());
create policy rp_insert on public.recruit_posts for insert to authenticated with check (public.is_admin());
create policy rp_delete on public.recruit_posts for delete to authenticated using (public.is_admin());
grant select, insert, delete on public.recruit_posts to authenticated;
