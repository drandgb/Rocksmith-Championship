-- Week Maker (profile tab for players who've hosted a week): each host's favorite tab authors, options and current proposed week,
-- so the same proposal shows on all their devices until they shuffle. Only you can see or change your own.
-- Run once in the Supabase SQL editor.

create table if not exists public.week_maker (
  user_id    uuid primary key default auth.uid() references auth.users(id) on delete cascade,
  favs       jsonb not null default '[]'::jsonb,   -- favorite tab authors
  opts       jsonb not null default '{}'::jsonb,   -- {"bonus": true/false, "god": true/false, "never": [songs never to suggest], "oldFill": true/false}
  proposal   jsonb,                                -- the proposed week (songs per class and path)
  updated_at timestamptz not null default now()
);

alter table public.week_maker enable row level security;

drop policy if exists wm_select on public.week_maker;
create policy wm_select on public.week_maker for select to authenticated using (user_id = auth.uid());
drop policy if exists wm_insert on public.week_maker;
create policy wm_insert on public.week_maker for insert to authenticated with check (user_id = auth.uid());
drop policy if exists wm_update on public.week_maker;
create policy wm_update on public.week_maker for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());

grant select, insert, update on public.week_maker to authenticated;

notify pgrst, 'reload schema';
