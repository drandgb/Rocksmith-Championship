-- Let admins give or change ratings on behalf of any player (the Admin tab's "Ratings for a player").
drop policy if exists votes_insert on public.votes;
drop policy if exists votes_update on public.votes;
create policy votes_insert on public.votes for insert to authenticated with check ((player = public.my_player() or public.is_admin()) and user_id = auth.uid());
create policy votes_update on public.votes for update to authenticated using (player = public.my_player() or public.is_admin()) with check ((player = public.my_player() or public.is_admin()) and user_id = auth.uid());
