// Scoreboard fix log: compares the Admin tab's scoreboard checks with the previous site update and records the
// issues that went away (fixed in the sheet), then puts the log into the page.
//   node fixlog.js <index.html> <cache dir>
// The checks themselves are typoScan() from the page, so the log always matches what the Admin tab shows.
// The first run only records the current issues; nothing is logged until something is fixed after that.
const fs = require("fs"), path = require("path");
const [page, cache] = process.argv.slice(2);
let h = fs.readFileSync(page, "utf8");
const m = h.match(/SB=(\{[\s\S]*?\});\s*\n/);
const a = h.indexOf("const ZERO_FROM"), b = h.indexOf("function typoSection");
if (!m || a < 0 || b < 0 || !h.includes("var FIXLOG=[]/*FIXLOG*/")) { console.log("fixlog: page layout not found, skipped"); process.exit(0); }
const SB = eval("(" + m[1] + ")");
var TYPO_CACHE = null;
eval(h.slice(a, b).replace("function typoScan", "globalThis.typoScan=function"));
const { out } = typoScan();

// one entry per issue, keyed so the same issue is recognised between updates
const now = {};
for (const [k, list] of Object.entries(out)) for (const x of list) {
  let key, e;
  if (x.forms) {
    const t = x.forms.map(f => `“${f.t}”`).join(" vs ");
    key = k + "|" + x.forms.map(f => f.t).sort().join("|"); e = { k, t };
  } else {
    key = [k, x.w, x.p, x.lv, x.song, x.n].join("|");
    e = { k, w: x.w, p: x.p, lv: x.lv, n: x.n, t: x.n + ": " + (x.note || x.song) };
  }
  now[key] = e;
}
const prevFile = path.join(cache, "typo_prev.json"), logFile = path.join(cache, "fixlog.json");
const read = f => { try { return JSON.parse(fs.readFileSync(f, "utf8")); } catch (e) { return null; } };
const prev = read(prevFile), log = read(logFile) || [];
let added = 0;
if (prev) {
  const d = new Date().toISOString();
  for (const [key, e] of Object.entries(prev)) if (!(key in now)) { log.push({ d, ...e }); added++; }
}
const keep = log.slice(-300);
fs.writeFileSync(prevFile, JSON.stringify(now));
fs.writeFileSync(logFile, JSON.stringify(keep));
h = h.replace("var FIXLOG=[]/*FIXLOG*/", "var FIXLOG=" + JSON.stringify(keep).replace(/</g, "\\u003c") + "/*FIXLOG*/");
fs.writeFileSync(page, h);
console.log(`fixlog: ${Object.keys(now).length} open issues, ${added} newly fixed` + (prev ? "" : " (first run: baseline only)"));
