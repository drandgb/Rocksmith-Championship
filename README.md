[README.md](https://github.com/user-attachments/files/33099096/README.md)
# 🎸 Rocksmith 2014 Championship Stats

A stats companion for the **Rocksmith 2014 Championship**, the weekly CDLC challenge run on the [CustomsForge](https://customsforge.com/forum/38-rocksmith-championship/) forums. It covers winners, players, hosts, songs and the full scoreboard history, with medals for all of them, in one page.

**Live site:** https://drandgb.github.io/Rocksmith-Championship/

Quick links in the page header:
- [Championship forum](https://customsforge.com/forum/38-rocksmith-championship/)
- [Scoreboard sheet](https://docs.google.com/spreadsheets/d/1WN-m8wF0lVkQ4cLWHBa009SkqDoPk0xN-C4-llcrXXs/edit?gid=871655614#gid=871655614)
- [Request a song](https://script.google.com/macros/s/AKfycbwy6vF3XYDZ_s1WeqiHTgBcVgbF8cr2AUQjKH3aRSZYuh32Erc-IstP5Gos-1i_evkm/exec)

The whole app is one self-contained `index.html`. It has no build step, no server and no dependencies apart from Google Fonts.

---

## Tabs

### 📅 This Week
- The page the site opens on (links ending in #winners, #players, #hosts, #songs or #scoreboard open that tab instead). Shows the current week; use ‹ › to step back through earlier weeks.
- **Back from a break**: who played after missing last week, with the week they last played.
- **New this week**: first-time players, with the rank they started at on each path.
- **Anniversaries**: active players who first joined in this calendar week in an earlier year. ✓ playing means they played that week.
- **Streaks at stake**: active play streaks with no score yet this week (on past weeks: streaks that ended).
- **New medals** collected this week. Click one to ring it and show what it is for. While a week is still running, player medals are provisional and win medals are added once it ends.
- An **Open scoreboard** button opens the week shown on the Scoreboard.
- Boxes with something in them get a glowing rim: gold for New medals, red for Rivals, green for New this week, a starry rim for Anniversaries, a tropical rim (with a swaying palm) for Back from a break, amber for Streaks at stake and a gloomy rainy blue for Streaks that ended.
- **Rivals**, split into Lead, Rhythm and Bass (dead-even pairs get a glowing rim): each player's closest match within their own rank on that path: the opponent with the smallest average % gap on the ranked challenges they both played. Playing up or down and God challenges don't count.

### 📊 Rankings
- **Rodman’s Rankings**, straight from the *Rodman´s Rankings* tab of the scoreboard sheet: the leaderboard for the last 10 weeks (1st–4th place on a challenge scores 10/5/3/1 points), for every path and level, with each player's rank change since last week.
- Filter by **All paths / Lead / Rhythm / Bass**. Click a name to open their Player lookup.

### 🏆 Winners
- Switch between **All paths / Lead / Rhythm / Bass**.
- **Seasons**: pick a year (or All time) to see that year's Hall of fame, Most wins, Win rates and Rank changes. Winner lookup follows the season too.
- **Hall of fame** podium for the most challenge wins.
- **🔥 Hot streaks**: players who won a challenge in each of the last 2+ weeks. 🔥🔥 means 5+ weeks and 🔥🔥🔥 means 10+.
- **Most wins** and **Win rates** (top 20). Hover a win-rate bar to see wins vs. entries.
- **Winner lookup**:
  - **Stats:** weeks with a win, total wins, best week, longest win streak, triple crowns, close wins (won on the tiebreak) and Lead, Rhythm and Bass rivals (the player who was most often their closest match within the same rank on that path; click to highlight those weeks).
  - **Medals:** 🥇🥈🥉 gold, silver and bronze medals (how many times they finished 1st, 2nd or 3rd on a challenge), 💎 God diamonds (the same for God challenges), 🏆 win-week trophies (one cup per win; the number is how many weeks they won that many), ⚡ win-streak bolts (2, 3, 4, 5, 10, 15, 20, 25, 30, 40, 50… weeks in a row), 👑 triple crowns (won Lead, Rhythm and Bass in the same week) and 🟰 close-win medals.
  - **Week chart:** heat colors for 1, 2 and 3+ wins.
  - **Year filter:** click a year label to see that year's stats only.
- **Rank changes**: class promotions ↗ and demotions ↘ over the past year.

### 🎸 Players
- Players per week, with a 10-week average.
- Hall of fame, perfect attendance, most active in the past year, and active and all-time play streaks.
- Longest careers, highest play rates, and players new in the past year.
- **Player lookup**:
  - **Stats:** weeks played, first and latest week, active and best streak, play rate.
  - **Medals:** perfect-attendance gem, class gems (one for every class up to the highest reached, so Advanced also gives Beginner and Intermediate; dated by the first rank-up into that class when there is a record; gems are always collected in order, so a date later than a higher class's date is left off as a missing record), lunar-year medallions (zodiac animal, colored by element) and play-streak embers (2, 3, 4, 5, 10 … 50 weeks in a row) and yearly streak flames.
  - **Year filter:** click a year label to see that year's stats only.

### 🎙️ Hosts
- Hall of fame and **Coming up** schedule, with holidays and a *HOST NEEDED* tag for open weeks.
- **Host leaderboard** with active and inactive tags.
- **Host lookup**:
  - **Stats:** weeks hosted, share, most weeks in a row, years hosting and scheduled weeks.
  - **Medals:** 🎙️ total weeks, 🔗 weeks in a row, and yearly lunar host medallions.
  - **Year filter:** click a year label to see that year's stats only, including the host's rank among that year's hosts.
- Hosting timeline and **Week log**. Click any holiday to see only the weeks with that holiday.

### 🎵 Songs
- Most featured and most played bands. Bands by difficulty, plus the easiest and toughest bands:

  | Level | Rating |
  |---|---|
  | Beginner | under 4 |
  | Intermediate | 4–5.5 |
  | Advanced | 6–7.5 |
  | Masterclass | 8–9.5 |
  | God tier | 10+ |

- **Picked by**: pick a host to see only the songs from the weeks they hosted (their song picks). A multi-week God challenge counts for the host of its first week. Every list and Band lookup follow it. Host lookup has a **Song picks ›** button that opens this.
- **Band lookup** with level, path and song filters.
- **Most played songs**: hover to see who played each song, grouped by week.
- **Most replayed songs**.

### 📋 Scoreboard
- Every challenge card for weeks 440 onward, by path and level.
- Medals go only to eligible players. Players playing down are faded, renamed players show as *"as OldName"*, and rank-ups are tagged.
- Click a song or band name to open it in Band lookup.
- **Back to latest week** appears when you're on an older week.

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

Two GitHub Actions do this. Each one downloads the sheet, rebuilds `index.html` and commits only if the data changed; GitHub Pages republishes a minute or two later.

| Action | When | What it re-reads |
|---|---|---|
| **Quick update (current week)** ([`quick-update.yml`](.github/workflows/quick-update.yml)) | Every hour | The 2 newest week tabs, plus `Schedule` and `PlayersList`. Older weeks come from the saved results in `build/data/cache/`. |
| **Full rescan (whole sheet)** ([`full-rescan.yml`](.github/workflows/full-rescan.yml)) | Sundays | Every week tab, so corrections to older weeks show up. |

The page's *Last updated* time is the last time either Action checked the sheet (read from GitHub when the page loads), shown in the viewer's own time zone.

Run either one by hand from **Actions → (pick one) → Run workflow**.

What it reads from the sheet (it must stay shared as *Anyone with the link can view*):

| Tab | Used for |
|---|---|
| `WeekNNN` tabs | Scores, wins, medals, classes (from name colors) and who played each week |
| `PlayersList` | Lead / Rhythm / Bass classes. Every name on a scoreboard counts as a player, listed or not; brand-new names are listed in the build log in case one is a typo |
| `Rodman´s Rankings` | The Rankings page |
| `Schedule` | Week numbers, start dates and hosts, including upcoming bookings (*Week \| Start Date \| Host*) |

Attendance and play streaks only count weeks where a player actually submitted a score: a score that simply carries over on a multi-week God challenge (identical to the week before) doesn't count.

History that doesn't change (attendance from the old Metrics workbook and songs from before week 440) is saved in `build/data/`. When the two disagree, the scoreboard sheet wins.

### Update the site straight from the sheet (optional, recommended)

GitHub's hourly schedule often runs late. A small Apps Script in the scoreboard sheet can start the quick update itself a few minutes after any edit. The script is in [`build/apps-script/update-website.gs`](build/apps-script/update-website.gs).

1. **Make a GitHub token.** On GitHub go to *Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token*.
   - **Repository access:** *Only select repositories* → `drandgb/Rocksmith-Championship`.
   - **Permissions → Repository permissions → Actions:** *Read and write*. Nothing else is needed.
   - Pick an expiration (for example, 1 year) and copy the token.
2. **Add the script.** In the scoreboard sheet, open *Extensions → Apps Script*. If the project already has code, leave it alone and add a new file with **+ → Script** named `update-website`. Paste in `update-website.gs` and save.
3. **Save the token.** In the Apps Script editor, open *Project Settings* (gear icon) → *Script properties* → *Add script property*. Name: `GITHUB_TOKEN`, value: the token.
4. **Turn it on.** Back in the editor, pick `installTriggers` in the function list and click *Run*. Approve the permissions Google asks for.

After that, edits to the sheet start a site update within about 5 minutes, and the update is live 2–3 minutes later. A burst of edits only causes one update. Reload the sheet to see a new **Website → Update website now** menu for an instant update.

Anyone who can edit the script can see the token, but it can only start Actions in this repo. To turn it off, delete its three triggers (`markChanged`, `updateIfChanged`, `addWebsiteMenu`) under *Triggers* (clock icon) in the Apps Script editor.

To build by hand: `./build/build.sh` (downloads the sheet) or `./build/build.sh path/to/scoreboard.xlsx`; add `MODE=quick` in front for a quick update. You need Python 3 with `openpyxl`.

---

## Credits

- Data comes from the Rocksmith 2014 Championship scoreboards, player list and song lists maintained by the challenge hosts on CustomsForge.
- Thanks to every host and player who has kept the challenge running week after week since 2013. 🤘

*Unofficial fan project. Not affiliated with Ubisoft or Rocksmith.*
