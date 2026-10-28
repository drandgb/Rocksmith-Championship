// Weekly score log for the "Your week" tab: each player's first score and best score on every challenge of the
// current week (with their place), and who passed whom. The scoreboard sheet only keeps each player's best score,
// so this is built up from one site update to the next and kept in the cache.
//   node weeklog.js <index.html> <cache dir>
// Places count only players who can win the challenge (their own class), as on the Scoreboard.
const fs = require("fs"), path = require("path");
const [page, cache] = process.argv.slice(2);
let h = fs.readFileSync(page, "utf8");
const m = h.match(/SB=(\{[\s\S]*?\});\s*\n/);
if (!m || !h.includes("var WEEKLOG={}/*WEEKLOG*/")) { console.log("weeklog: page layout not found, skipped"); process.exit(0); }
const SB = eval("(" + m[1] + ")");
const canWin = e => (e[4] === 0 || e[4] === 9) && !/~$/.test(SB.names[e[0]]);   // FreeBirds can't win
const nm = i => String(SB.names[i]).replace(/[*~]+$/, "");
const file = path.join(cache, "weeklog.json");
let log; try { log = JSON.parse(fs.readFileSync(file, "utf8")); } catch (e) { log = {}; }
const now = new Date().toISOString().slice(0, 16) + "Z";
const weeks = Object.keys(SB.weeks).map(Number).sort((a, b) => b - a).slice(0, 2);   // this week and last week (late fixes)
let events = 0;
for (const w of weeks) {
  const W = log[w] = log[w] || { rec: {}, ev: [], seen: false };
  const first = !W.seen; W.seen = true;   // the first time a week is seen, record scores but no "passed" events
  for (const c of SB.weeks[w] || []) {
    if (!c[3] || /^n\/a$/i.test(c[3])) continue;
    const card = c[0] + "|" + c[1];
    let place = 0; const now_ = {};
    c[6].forEach((e, i) => { const n = nm(e[0]); const pl = canWin(e) ? ++place : 0; if (!(n in now_)) now_[n] = [e[1], e[2], pl, i + 1]; });
    // passed: a player's place got worse because someone else is now above them
    for (const [n, cur] of Object.entries(now_)) {
      const r = W.rec[card + "|" + n]; if (!r || first) continue;
      const before = r[1][2], after = cur[2];
      if (before && after && after > before) {
        const above = Object.entries(now_).filter(([o, x]) => o !== n && x[2] && x[2] < after);
        const wasAbove = new Set(Object.keys(now_).filter(o => { const ro = W.rec[card + "|" + o]; return ro && ro[1][2] && ro[1][2] < before; }));
        above.filter(([o]) => !wasAbove.has(o)).forEach(([o, x]) => {
          // from/to: place among the card's class; fp/tp: position on the card (#), as shown on the Scoreboard
          W.ev.push({ t: now, p: c[0], s: c[1], lv: c[2], song: c[3], n, from: before, to: after, fp: r[1][4], tp: cur[3], by: o, bp: x[0], bs: x[1], mp: cur[0], ms: cur[1] }); events++;
        });
      }
    }
    // first and best (latest) score and place for everyone on the card
    for (const [n, cur] of Object.entries(now_)) {
      // [%, streak, place among players of the card's class (0 = other class), time, position on the card]
      const k = card + "|" + n, r = W.rec[k], x = [cur[0], cur[1], cur[2], now, cur[3]];
      if (!r) W.rec[k] = [x, x]; else if (r[1][0] !== cur[0] || r[1][1] !== cur[1] || r[1][2] !== cur[2] || r[1][4] !== cur[3]) r[1] = x;
    }
  }
}
// keep the last 3 weeks
Object.keys(log).map(Number).sort((a, b) => b - a).slice(3).forEach(w => delete log[w]);
fs.writeFileSync(file, JSON.stringify(log));
const out = {}; Object.entries(log).forEach(([w, W]) => out[w] = { rec: W.rec, ev: W.ev });
h = h.replace("var WEEKLOG={}/*WEEKLOG*/", "var WEEKLOG=" + JSON.stringify(out).replace(/</g, "\\u003c") + "/*WEEKLOG*/");
fs.writeFileSync(page, h);
console.log(`weeklog: weeks ${weeks.join(", ")}, ${events} new passes`);
