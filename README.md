[README.md](https://github.com/user-attachments/files/33080801/README.md)
# Rocksmith 2014 Championship Stats

A stats companion for the **Rocksmith 2014 Championship**, the weekly CDLC challenge run on the [CustomsForge](https://customsforge.com) forums. It covers winners, players, hosts, songs and the full scoreboard history in one page.

**Live site:** https://YOUR-USERNAME.github.io/rocksmith-championship/

The whole app is a single self-contained `index.html`. It has no build step, no server and no dependencies apart from Google Fonts.

---

## What's inside

### 🏆 Winners
- Switch between **All / Lead / Rhythm / Bass**.
- **Hall of fame** podium for the most challenge wins.
- **🔥 Hot streaks**: players who won in each of the last 3+ weeks. 🔥🔥 means 5+ weeks and 🔥🔥🔥 means 10+.
- **Most wins** and **Win rates** (top 20, minimum 25 entries).
- **Winner lookup**:
  - Stats: weeks with a win, total wins, best week, longest win streak, triple crowns and closest win.
  - Medals:
    - 🏆 trophies for wins in a single week
    - ⚡ one bolt for each week of the win streak
    - 🎖️ total-win ribbons
    - 👑 triple crowns for winning Lead, Rhythm and Bass in the same week (gold for regular challenges, purple for bonus)
  - A week-by-week grid. Click a week to open it on the Scoreboard. Click *Best week*, *Longest win streak*, *Closest win* or a crown to highlight those weeks.
- **Rank changes**: class promotions (↗) and demotions (↘) over the past year.

### 🎸 Players
- Players per week, with a 10-week average.
- Hall of fame, perfect attendance, most active in the past year, and active and all-time play streaks.
- Longest careers, highest play rates, and players new in the past year.
- **Player lookup**:
  - Medals:
    - Perfect-attendance gem
    - Class gem for the highest class reached
    - Lunar-year medallions with zodiac animals, colored by element
    - Play-streak flames
  - A presence grid linked to the Scoreboard.

### 🎙️ Hosts
- Hall of fame.
- **Coming up** schedule, with holidays and a *HOST NEEDED* tag for open weeks.
- Leaderboard with active and inactive tags.
- Timeline and week log.

### 🎵 Songs
- Most featured and most played bands.
- Bands by difficulty:

  | Level | Rating |
  |---|---|
  | Beginner | under 4 |
  | Intermediate | 4–5.5 |
  | Advanced | 6–7.5 |
  | Masterclass | 8–9.5 |
  | God tier | 10+ |

- Easiest and toughest bands.
- **Band lookup** with level and path filters.
- Most played songs (by unique players) and most replayed songs.

### 📋 Scoreboard
- Every challenge card for weeks 440 onward, by path and level.
- Medals go only to eligible players.
- Players playing down are faded, renamed players show as *"as OldName"*, and rank-ups are tagged.

---

## How wins are counted

A win counts only when the player was **eligible**, meaning they were playing at or below their own class for that path. A player playing down can top a card without getting the win. In that case the win goes to the highest eligible player. This rule applies everywhere: win totals, streaks, medals, triple crowns and closest wins.

Class history is read from the font colors and sizes in the original Google Sheets. Each player's class per path is inferred from runs of at least 3 weeks.

---

## Updating the site

1. Replace `index.html` in this repo with the new version. Use **Add file → Upload files** and commit.
2. GitHub Pages redeploys automatically within a minute or two.

The footer of the page shows the date the data was last updated.

---

## Credits

- Data comes from the Rocksmith 2014 Championship scoreboards and song lists maintained by the challenge hosts on CustomsForge.
- Thanks to every host and player who has kept the challenge running week after week. 🤘

*Unofficial fan project. Not affiliated with Ubisoft or Rocksmith.*
