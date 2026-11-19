-- Fetch scores and Update website log (Host tab): each time a host or an admin presses one of those buttons, the
-- website adds a row here with the result and the script's step-by-step lines. Run once in the Supabase SQL editor.
create table if not exists public.host_runs (
  id         bigint generated always as identity primary key,
  at         timestamptz not null default now(),
  user_id    uuid default auth.uid() references auth.users on delete set null,
  by_player  text,
  action     text not null check (action in ('fetch','add','update','rescan')),
  ok         boolean not null default false,
  summary    text check (char_length(summary) <= 500),
  lines      jsonb not null default '[]'::jsonb check (jsonb_typeof(lines) = 'array' and pg_column_size(lines) <= 20000)
);
create index if not exists host_runs_at on public.host_runs (at desc);
alter table public.host_runs enable row level security;
drop policy if exists hr_read on public.host_runs;
drop policy if exists hr_insert on public.host_runs;
create policy hr_read   on public.host_runs for select to authenticated using (true);
create policy hr_insert on public.host_runs for insert to authenticated
  with check (user_id = auth.uid() and (public.is_admin() or by_player = public.my_player()));
grant select, insert on public.host_runs to authenticated;

notify pgrst, 'reload schema';
