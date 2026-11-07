# 🎸 Rocksmith 2014 Championship Stats

A stats companion for the **Rocksmith 2014 Championship**, the weekly CDLC challenge run on the [CustomsForge](https://customsforge.com/forum/38-rocksmith-championship/) forums. It covers this week, seasons, player levels, rankings, winners, players, hosts, songs and the full scoreboard history, with medals for all of them, in one page.

**Live site:** https://drandgb.github.io/Rocksmith-Championship/

Quick links in the page header:
- [Play here](https://customsforge.com/forum/38-rocksmith-championship/) (the championship forum)
- [Scoreboard sheet](https://docs.google.com/spreadsheets/d/1WN-m8wF0lVkQ4cLWHBa009SkqDoPk0xN-C4-llcrXXs/edit?gid=871655614#gid=871655614)
- [Request a song](https://script.google.com/macros/s/AKfycbwy6vF3XYDZ_s1WeqiHTgBcVgbF8cr2AUQjKH3aRSZYuh32Erc-IstP5Gos-1i_evkm/exec)

The whole app is one self-contained `index.html`, with no server. It loads Google Fonts, plus the Supabase login library from jsdelivr for player accounts.

---

## Tabs

### 📅 This Week
- **🎯 Within reach** (at the top, for a signed-in player who played this week or last): their next goals close by: the next play streak (and whether it's a new medal), beating their longest play streak, a weeks-played milestone, the season place just above them, the next win streak medal when they're on one, and for hosts the next hosting medals and their place in this year's Host of the year race.
- The page the site opens on (links ending in #winners, #players, #hosts, #songs or #scoreboard open that tab instead). Shows the current week; use ‹ › to step back through earlier weeks.
- **Back from a break**: who played after missing last week, with the week they last played.
- **New this week**: first-time players, with the rank they started at on each path.
- **Anniversaries**: active players who first joined in this calendar week in an earlier year. ✓ playing means they played that week.
- **Streaks at stake**: active play streaks with no score yet this week (on past weeks: streaks that ended).
- **New medals** collected this week. Click one to ring it and show what it is for. While a week is still running, player medals are provisional and win medals are added once it ends.
- An **Open scoreboard** button opens the week shown on the Scoreboard.
- Boxes with something in them get a glowing rim: gold for New medals, red for Rivals, green for New this week, a starry rim for Anniversaries, a tropical rim (with a swaying palm) for Back from a break, amber for Streaks at stake and a gloomy rainy blue for Streaks that ended.
- **Countdown** to the week's close, in your own time zone and CET (CEST in summer). Only the next week's host, who closes the week, or an admin can set it, from the Host tab.
- **♟ Elo gains**: who gained rating with the week's scores, with each player's rank among active players. A player new to the ranking (just reached 20 games) shows *entered #N*, and the hover on a rank says why it moved, or stayed put while others moved: who they passed, who passed them, and who entered or left the ranking above them.
- **Medal leaders**: a note at the top of New medals when someone took (or, while the week runs, would take) the lead in a medal count.
- **Rivals**, split into Lead, Rhythm and Bass (dead-even pairs get a glowing rim). While the week runs, a green ▲ shows who leads so far; once it is over, each pair gets a 🏆 winner: whoever beat the other on more of their shared challenges (level on challenges is a tie). Rivals are each player's closest match within their own rank on that path: the opponent with the smallest average % gap on the ranked challenges they both played. Playing up or down and God challenges don't count. Each pair lists every challenge they both played (main song and bonus) with both players' %, the higher one in green.

### 🏁 Season
- The current season (or any past one from the picker): each path's standings by class, with season points, games played and each class's most improved player (the biggest player level gain over the season, with games in at least half its weeks).
- The week boxes show the season's progress; click a finished week to see the standings after that week, or the current week to go back.
- Lead, Rhythm and Bass boxes pick the class shown for each path; when you're logged in, a **Your classes** box shows just your own class on each path.
- **Season champions**: every finished season's winners by path and class.

### 📈 Level
- **Rodman’s Player Level** for every player on each path, from the *PlayerLevel* tab of the scoreboard sheet, with the site's own estimate for the weeks since. Switch between the last 6 months and a single year, and see the level bands for each class and how players moved through them over time.

### 📊 Rankings
- **Rodman’s Rankings**, straight from the *Rodman´s Rankings* tab of the scoreboard sheet: the leaderboard for the last 10 weeks (1st–4th place on a challenge scores 10/5/3/1 points), for every path and level, with each player's rank change since last week.
- Lead, Rhythm and Bass boxes (like the tier boxes in the player lookup) pick the level shown for each path: click one to cycle All → Beginner → Intermediate → Advanced → Masterclass; “Show all levels” resets them.
- Filter by **All paths / Lead / Rhythm / Bass**. Click a name to open their Player lookup.

### 🏆 Winners
- Switch between **All paths / Lead / Rhythm / Bass**.
- **Seasons**: pick a year (or All time) to see that year's Hall of fame, Most wins, Win rates and Rank changes. Winner lookup follows the season too.
- **Hall of fame** podium for the most challenge wins.
- **🔥 Hot streaks**: players who won a challenge in each of the last 2+ weeks. Their 🔥 next to their name glows brighter the longer the streak.
- **Most wins** and **Win rates** (top 20). Hover a win-rate bar to see wins vs. entries.
- **Winner lookup**:
  - **Stats:** weeks with a win, total wins, best week, longest win streak, triple crowns, close wins (won on the tiebreak) and Lead, Rhythm and Bass rivals (the player who was most often their closest match within the same rank on that path; click to highlight those weeks).
  - **Medals:** 🏆 season champion cups (a winged gold cup whose flame is the class color, glowing brighter the higher the class) and the season most improved cup in the four class colors, 🥇🥈🥉 gold, silver and bronze medals (how many times they finished 1st, 2nd or 3rd on a challenge), Uncrowned medals (the top score on a board while playing up or as a FreeBird, so it couldn't win), 💎 God diamonds in a golden laurel wreath (the same for God challenges), 🏆 win-week trophies (one cup per win; the number is how many weeks they won that many), 🔥 win-streak flames (2, 3, 4, 5, 10, 15, 20, 25, 30, 40, 50… weeks in a row), 👑 triple crowns (a jeweled crown: won Lead, Rhythm and Bass in the same week) and 🟰 close-win medals, and ⚔️ rivalry wins (beat their closest rival of the week).
  - **Week chart:** heat colors for 1, 2 and 3+ wins. Click *Weeks with a win* or *Best week* to highlight those weeks; when several weeks tie for best, the one with the hardest win (difficulty rating), then the widest margin, is shown.
  - **Year filter:** click a year label to see that year's stats only.
- **Rank changes**: class promotions ↗ and demotions ↘ over the past year.

### 🎸 Players
- Players per week, with a 10-week average. **See table** lists every week's count (this week so far at the top); click a count to highlight the weeks with the same number (more in green, fewer in red), or a week to open its Scoreboard.
- Hall of fame, perfect attendance, most active in the past year, and active and all-time play streaks.
- Longest careers, highest play rates, and players new in the past year.
- **Player lookup**:
  - **Stats:** weeks played, first and latest week, active and best streak, play rate.
  - **Highest score** and **highest note streak** on any scoreboard challenge, with the song and week; click either to open it on the Scoreboard (on phones, the first tap shows the details).
  - **Skill rating:** the second-best song rating they've scored 95% or better on in the last 6 months, on each path, with a year-by-year table. **Elo** ratings and ranks on each path too.
  - **Medals:** perfect-attendance gem, 🏺 kintsugi gem once the perfect run is broken (the number is how many weeks they played without missing after joining), 💯 perfectionist medals (100% scores; the God one is the Perfect God medal), one per class in that class's gem colour (Beginner yellow, Intermediate green, Advanced blue, Masterclass purple, God red), counting every 100% score whatever the place, 𝄞 played guitar and 𝄢 played bass medals (weeks with at least one Lead or Rhythm score, or at least one Bass score, any level), ✅ completionist medal (weeks with a score on every challenge, every song on every path; a multi-week God challenge already played earlier in its run counts) and Lead, Rhythm and Bass completionist medals (every challenge on that one path), class gems (one for every class up to the highest reached, so Advanced also gives Beginner and Intermediate; dated by the first rank-up into that class when there is a record; gems are always collected in order, so a date later than a higher class's date is left off as a missing record), lunar-year medallions (zodiac animal, colored by element) and ⚡ play-streak bolts (2, 3, 4, 5, 10 … 50 weeks in a row) and yearly streak bolts (with that year's zodiac animal).
  - **Year filter:** click a year label to see that year's stats only.
- **⚔️ Head-to-head:** pick any two players to see every challenge they both played and who finished higher (accuracy, then streak, then score): the overall record, who averaged higher accuracy, the record on each path with both Elo ratings, and their latest 10 challenges together. It starts with the player you looked up against the player they've shared the most challenges with in the past year.

### 🎙️ Hosts
- **Year:** pick a year (or All time) at the top to see only that year in the Hall of fame, leaderboards, timeline, Week log and Host lookup.
- Hall of fame and **Coming up** schedule, with holidays and a *HOST NEEDED* tag for open weeks.
- **Host leaderboard** with active and inactive tags.
- **Host lookup**:
  - **Stats:** weeks hosted, share, most weeks in a row, years hosting and scheduled weeks.
  - **Medals:** 🎙️ total weeks, 🔗 weeks in a row, 👑 Host of the year (most weeks hosted in a calendar year, shared on a tie, awarded once the year is over), and yearly lunar host medallions.
  - **Year filter:** click a year label to see that year's stats only, including the host's rank among that year's hosts.
- Hosting timeline and **Week log**. Click any holiday to see only the weeks with that holiday.

### 🎵 Songs
- Songs in Most popular, Most replayed and the Band lookup table have an **Ignition** pill with the song's most recent Ignition4 link from the scoreboard sheet.
- Official Rocksmith songs (on-disc and DLC) get a grey **Official** pill instead (hover: not available on Ignition), on the Songs page and Scoreboard cards. The list of official songs is `build/data/official.json`.
- Most featured and most popular bands (different players in total, or players per challenge). Bands by difficulty, plus the easiest and toughest bands:

  | Level | Rating |
  |---|---|
  | Beginner | under 4 |
  | Intermediate | 4–5.5 |
  | Advanced | 6–7.5 |
  | Masterclass | 8–9.5 |
  | God tier | 10+ |

- **Selected by**: pick a host to see only the songs from the weeks they hosted (their song picks). A multi-week God challenge counts for the host of its first week. Every list and Band lookup follow it. Host lookup has a **Song picks ›** button that opens this.
- **Band lookup** with level, path and song filters.
- **Song lookup**: search by title or tag, or filter by tuning. Songs can carry technique tags, and the tuning comes from the Song Selection List (with any fixes made on the site, including a capo).
- **Most popular songs**: the songs the most players have posted a score on, or (Per challenge) the most players per challenge; hover to see who played each song, grouped by week.
- **Most replayed songs**.

### 📋 Scoreboard
- An **Ignition** pill (download, comment and like icons) on each card links to the song on Ignition4 (CustomsForge), taken from the song title's link on the scoreboard sheet.
- Lead, Rhythm and Bass boxes pick the path; click the selected path again to cycle its level (All → Beginner → Intermediate → Advanced → Masterclass → God → All). Bonus songs show with their level.
- Every challenge card for weeks 440 onward, by path and level. **All cards** shows the whole week in Lead, Rhythm and Bass columns, with each class starting at the same height; **Your cards** (when logged in or highlighting a player) shows the cards in that player's own class on each path, played or not yet.
- Each card shows the song's tuning. Admins, and that week's host, can click it to fix the tuning or set a capo.
- Medals go only to eligible players. Players playing down are faded, renamed players show as *"as OldName"*, and rank-ups are tagged.
- Click a song or band name to open it in Band lookup.
- **Back to latest week** appears when you're on an older week.

### ❓ FAQ
- Answers in five groups: how to play (joining, posting a score, when the week ends), the rules (classes, moving up or down, winners, FreeBirds, how songs are picked), using the site, the stats (wins, rankings, seasons, Elo, skill rating, player level, rivals, medals) and your profile.

---

## Getting around

- **Hover any name** on any tab to see all of that person's medals: player, win and host.
- **Click a medal** in any lookup to highlight the week it was collected (streak medals highlight the whole run of weeks) (rank-change pills in Player lookup do the same). Click a streak, best week, crown or legend item to highlight those weeks.
- **Click a week** in a lookup chart, Rank changes, the Week log or the host leaderboard to open it on the Scoreboard.
- **Jump between lookups**: Player, Winner and Host lookup link to each other.
- **"Filters on" bubble**: shows which filters are active on the current tab. Click ✕ to clear one, or *Clear all*.

---

## How wins are counted

A win counts only when the player was **eligible**, meaning they were playing at or below their own class for that path. A player playing down can top a card without getting the win. In that case the win goes to the highest eligible player.

God challenges (and tributes) run for 2 or more weeks in a row with the same song. Only the **final week** of the run counts: that's when its winner and entries are counted. Earlier weeks are marked *Continues next week* on the Scoreboard.

This rule applies everywhere: win totals, win rates, streaks, medals, triple crowns and close wins.

Class history is read from the font colors and sizes in the original Google Sheets. Each player's class per path is inferred from runs of at least 3 weeks.

---

## Updating the site

The site rebuilds itself from the **[scoreboard sheet](https://docs.google.com/spreadsheets/d/1WN-m8wF0lVkQ4cLWHBa009SkqDoPk0xN-C4-llcrXXs/edit)**:

Two GitHub Actions do this (two more keep the forum banners up to date and back up the sheet). Each of the two downloads the sheet, rebuilds `index.html` and commits only if the data changed; GitHub Pages republishes a minute or two later.

| Action | When | What it re-reads |
|---|---|---|
| **Quick update (current week)** ([`quick-update.yml`](.github/workflows/quick-update.yml)) | Every hour | The 2 newest week tabs, plus `Schedule` and `PlayersList`. Older weeks come from the saved results in `build/data/cache/`. |
| **Full rescan (whole sheet)** ([`full-rescan.yml`](.github/workflows/full-rescan.yml)) | Sundays | Every week tab, so corrections to older weeks show up. |
| **Scoreboard sheet backup** ([`sheet-backup.yml`](.github/workflows/sheet-backup.yml)) | Sundays | The whole sheet, saved as a file. Each weekly copy is kept for 90 days (about the last 13 weeks) under that run on the Actions tab; the first copy of each year is also kept for good under *Releases*. |
| **Check a draft** ([`site-check.yml`](.github/workflows/site-check.yml)) | Every push to a draft branch | Builds the page with the draft's code from the current sheet and checks it (below). Nothing is committed. |
| **Forum banners for new players** ([`banners.yml`](.github/workflows/banners.yml)) | Every 10 minutes | Nothing from the sheet: makes a forum banner for anyone whose profile claim was just approved. Commits nothing when nobody is new. |

The page's *Last updated* time is the last time either Action checked the sheet (read from GitHub when the page loads), shown in the viewer's own time zone.

Run either one by hand from **Actions → (pick one) → Run workflow**.

Before an update goes live, `build/check_page.py` opens the new page in headless Chrome at computer and phone widths and opens every tab. If a tab is empty or the page's code hits an error, the site keeps its last good page and the run is marked as failed, so GitHub emails you.

What it reads from the sheet (it must stay shared as *Anyone with the link can view*):

| Tab | Used for |
|---|---|
| `WeekNNN` tabs | Scores, wins, medals, classes (from name colors) and who played each week |
| `PlayersList` | Lead / Rhythm / Bass classes. Every name on a scoreboard counts as a player, listed or not; brand-new names are listed in the build log in case one is a typo |
| `Rodman´s Rankings` | The Rankings page |
| `Schedule` | Week numbers, start dates and hosts, including upcoming bookings (*Week \| Start Date \| Host*) |
| `PlayerLevel` | The Level tab (Rodman’s Player Level) |

Song tunings and the *Songs Played* list come from the Song Selection List spreadsheet.

Attendance and play streaks only count weeks where a player actually submitted a score: a score that simply carries over on a multi-week God challenge (identical to the week before) doesn't count.

History that doesn't change (attendance from the old Metrics workbook and songs from before week 440) is saved in `build/data/`. When the two disagree, the scoreboard sheet wins.

### Update the site straight from the sheet (optional, recommended)

GitHub's hourly schedule often runs late. A small Apps Script in the scoreboard sheet can start the quick update itself a few minutes after any edit. The script is in [`build/apps-script/updateWebsite.gs`](build/apps-script/updateWebsite.gs).

1. **Make a GitHub token.** On GitHub go to *Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token*.
   - **Repository access:** *Only select repositories* → `drandgb/Rocksmith-Championship`.
   - **Permissions → Repository permissions → Actions:** *Read and write*. Nothing else is needed.
   - Pick an expiration (for example, 1 year) and copy the token.
2. **Add the script.** In the scoreboard sheet, open *Extensions → Apps Script*. If the project already has code, leave it alone and add a new file with **+ → Script** named `updateWebsite`. Paste in `updateWebsite.gs` and save.
3. **Save the token.** In the Apps Script editor, open *Project Settings* (gear icon) → *Script properties* → *Add script property*. Name: `drandWebsiteToken`, value: the token.
4. **Turn it on.** Back in the editor, pick `installTriggers` in the function list and click *Run*. Approve the permissions Google asks for.

The script also sends the time of the last edit, which the site shows as **Sheet last edited** in its footer.

After that, edits to the sheet start a site update within about 5 minutes, and the update is live 2–3 minutes later. A burst of edits only causes one update. For buttons, add `.addItem('Update website now (drand)', 'updateWebsiteNow')` and `.addItem('Full rescan (drand)', 'fullRescanNow')` to the sheet's existing **Rocksmith CS** menu code (before `.addToUi()`), then reload the sheet.

Anyone who can edit the script can see the token, but it can only start Actions in this repo. To turn it off, delete its two triggers (`markChanged` and `updateIfChanged`) under *Triggers* (clock icon) in the Apps Script editor.

To build by hand: `./build/build.sh` (downloads the sheet) or `./build/build.sh path/to/scoreboard.xlsx`; add `MODE=quick` in front for a quick update. You need Python 3 with `openpyxl`.

---

## Credits

- Data comes from the Rocksmith 2014 Championship Google Sheets (scoreboards, player list and schedule), maintained by the challenge hosts.
- Thanks to every host and player who has kept the challenge running week after week since 2013. 🤘


## Player accounts and song ratings (optional)

Players can log in with an emailed link (no password) and claim their player profile. An approved player gives one rating per song per path: by clicking the difficulty number of a challenge on the Scoreboard, or a song's Lead/Rhythm/Bass rating box in Most popular, Most replayed or Band lookup. A rating counts for that song on that path in every week it's used. Once a song has ratings, its badges show the players' average (with a stronger fill; your own rated ones get a green ✓); hovering shows the host's initial rating for every week and every player's rating. Verified hosts (approved players who have hosted before) can sign up for an open week shown under Coming up (at least the next 9 weeks), from the HOST NEEDED pills on the Hosts page or the This Week banner; admins can sign anyone up and see all sign-ups in the Admin tab. The schedule sheet stays the source of truth: once it names a host for a week, that's who the site shows. It's off until a Supabase project is connected:

1. Create a free project at supabase.com.
2. In **Authentication → URL Configuration**, set the Site URL (and a Redirect URL) to `https://drandgb.github.io/Rocksmith-Championship/`.
3. In **Authentication → Emails → SMTP settings**, connect an email sender for the login emails.
4. In **SQL Editor**, run `build/supabase/schema.sql`, then `admin_ratings.sql`, `rating_log.sql`, `claim_log.sql`, `claim_remove.sql` and `host_ratings.sql` from the same folder, in that order (ratings on a player's behalf, the Ratings log, the Claims log, the choices when removing a claim, and letting hosts rate for other players). The other files there each add one feature and can be run in any order after those: `admin_manage.sql` (adding admins, unlinking an email), `animals.sql`, `host_signups.sql`, `week_close.sql` (the week close countdown), `site_themes.sql` (the website theme schedule), `song_tags.sql`, `song_tunings.sql` (tuning fixes, capos and the Tuning log), `vote_log.sql` (the Difficulty ratings log), `banner_redraw.sql` (the Redraw all banners button), `improve_posted.sql` (which Big improvements messages were already copied) and `player_rating_wins.sql`.
5. Put the project URL and the anon/publishable key into `SUPA_URL` and `SUPA_KEY` in `build/template.html` (both are public by design; never use the service_role key).
6. Log in on the site once, then run the two lines at the bottom of `schema.sql` with your email to make yourself an admin. Admins approve or remove profile claims from the 👤 account dialog.

Rules (enforced by the database): one account per player name, one name per account, claims start pending until an admin approves them, and only an approved player can rate, once per song per path (rating again replaces it). Anyone who has hosted (and admins) can also rate for a player who sent their ratings another way, from the Host tab, which also lists the open weeks to sign up for and the Ratings log. Every claim an admin approves, rejects or removes is listed in the Claims log; the Admin tab also has a Tuning log and a Difficulty ratings log (every rating given, changed or removed). This week's host sees likely typos in last week's and this week's scoreboard in the Host tab, with a 🔧 badge. Approved players also get **Your week** (their first and best score on each challenge this week, and an alert when someone passes them) and a yearly **Restringed** recap. An approved player's own profile also has a private **Rank-up readiness** section: for each path below Masterclass it says whether their last 12 weeks look Ready for the next class (played up to it at least twice and beat at least 30% of its regulars on average) and how past rank-ups with and without that record turned out. When removing an approved claim, the admin chooses whether the player's forum banner stays, whether their ratings stay shown, and whether a new account claiming the same name gets those ratings.

### Forum banners

Every approved player gets a forum signature banner (700×150): their name and classes, weeks played, wins, their player level on each path (with the gain this season), this season's standing on each path, and up to 8 win medals in this order: gold God diamonds, season champion and most improved cups, gold medals, triple crown, Uncrowned and close win; then silver God diamonds, silver medals and Uncrowned silver; then the bronze ones, the longest win streak medal and rivalry wins (most-won first within each kind). A #1, #2 or #3 tag marks a medal they're in the top 3 for among active players. The **Forum banner** tab in the 👤 dialog shows it, with the image link and site link to paste into the forum signature. Admins can preview any player's banner, and use **Redraw all banners** after a design change.

`build/banners.py` draws them with headless Chrome into `cards/<name>.png`. Every banner is redrawn when a new week's results arrive (as part of the quick update); newly approved players get theirs within about 10 minutes (the banner Action above), and banners of players who are no longer approved are deleted.

Each banner also has a share link, `cards/<name>.html` (copied from the Forum banner tab): posted in Discord, Reddit or a message, it shows the banner as the link preview and opens the player's stats on the site. The site's own link preview picture, `cards/og/site.png` (the four season trophies with the weeks, players and scores covered), is drawn with the banners each week.

---

*Unofficial fan project. Not affiliated with CustomsForge, Ubisoft or Rocksmith.*
