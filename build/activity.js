// Busiest days for the Admin tab: every time a player's new or better score reaches the scoreboard for the week being
// played, count it on that day of the week and hour (CET, the championship's time), kept in the cache from one site
// update to the next. (It's when the score reached the scoreboard sheet: hosts often add scores in batches.)
// The counts from Oct 6, 2026 (when the scores cache started) were worked out once from the repository's history.
//   node activity.js <index.html> <cache dir>
const fs = require("fs"), path = require("path");
const [page, cache] = process.argv.slice(2);
let h = fs.readFileSync(page, "utf8");
if (!h.includes("var ACTIVITY=null/*ACTIVITY*/")) { console.log("activity: page layout not found, skipped"); process.exit(0); }
const file = path.join(cache, "activity.json"), raw = JSON.parse(fs.readFileSync(path.join(cache, "scores_raw.json"), "utf8"));
let A; try { A = JSON.parse(fs.readFileSync(file, "utf8")); } catch (e) { A = null; }
const now = {};
for (const [w, cards] of Object.entries(raw)) for (const c of cards) {
  if (!c[3] || /^n\/a$/i.test(String(c[3]))) continue;
  for (const e of c[6]) now[`${w}|${c[0]}|${c[1]}|${String(e[0]).replace(/[*~]+$/, "").toLowerCase()}`] = [e[1], e[2]];
}
const weeks = Object.keys(now).map(k => +k.split("|")[0]), top = String(Math.max(...weeks));
const num = x => +x || 0, better = (a, b) => !b || num(a[0]) > num(b[0]) || (num(a[0]) === num(b[0]) && num(a[1]) > num(b[1]));
if (!A) A = { since: new Date().toISOString(), n: 0, days: [0, 0, 0, 0, 0, 0, 0], hours: Array(24).fill(0), last: null };
if (A.last) {   // the first run only remembers the scores, so nothing is counted twice
  const ch = Object.keys(now).filter(k => k.startsWith(top + "|") && better(now[k], A.last[k])).length;
  if (ch) {
    const p = Object.fromEntries(new Intl.DateTimeFormat("en-US", { timeZone: "Europe/Berlin", weekday: "short", hour: "numeric", hourCycle: "h23" }).formatToParts(new Date()).map(x => [x.type, x.value]));
    A.days[["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(p.weekday)] += ch; A.hours[+p.hour % 24] += ch; A.n += ch;
  }
}
A.last = Object.fromEntries(Object.entries(now).filter(([k]) => +k.split("|")[0] >= +top - 2));   // the last 3 weeks are enough
fs.writeFileSync(file, JSON.stringify(A));
h = h.replace("var ACTIVITY=null/*ACTIVITY*/", "var ACTIVITY=" + JSON.stringify({ since: A.since, n: A.n, days: A.days, hours: A.hours }) + "/*ACTIVITY*/");
fs.writeFileSync(page, h);
console.log(`activity: ${A.n} scores counted since ${A.since.slice(0, 10)}`);
