-- Claims log: add the claims that were approved before the log existed (Admin → Claims log).
-- The approval date of those wasn't recorded, so each is listed as approved on the day the player made the claim. Safe to run more than once: claims already in the log are skipped.
-- Run this once in Supabase → SQL Editor, after claim_log.sql.
insert into public.claim_log (at, admin_id, admin_player, player, action)
select c.created_at, null, null, c.player, 'approved_before_log'
from public.claims c
where c.status = 'approved'
  and not exists (select 1 from public.claim_log l where l.player = c.player and l.action in ('approved', 'approved_before_log'));
