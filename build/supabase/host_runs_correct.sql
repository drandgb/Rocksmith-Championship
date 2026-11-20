-- Fetch & update log: also log scores corrected with "Check scores against the Score Assistant" (Host tab).
-- Run once in the Supabase SQL editor (after host_runs.sql).
alter table public.host_runs drop constraint if exists host_runs_action_check;
alter table public.host_runs add constraint host_runs_action_check check (action in ('fetch','add','update','rescan','correct'));
notify pgrst, 'reload schema';
