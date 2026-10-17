// Original host ratings: each challenge's difficulty rating from the scoreboard sheet the first time a site update sees
// it. If the rating in the sheet is changed later (for example by drandTools' "Update ratings from website"), the
// host's original rating still counts as the host's own rating for the song, until the host rates it themselves.
//   node hostorig.js <index.html> <cache dir>
// The page only gets the originals that now differ from the sheet (HOSTORIG), so it stays small.
const fs = require("fs"), path = require("path");
const [page, cache] = process.argv.slice(2);
let h = fs.readFileSync(page, "utf8");
const m = h.match(/SB=(\{[\s\S]*?\});\s*\n/);
if (!m || !h.includes("var HOSTORIG={}/*HOSTORIG*/")) { console.log("hostorig: page layout not found, skipped"); process.exit(0); }
const SB = eval("(" + m[1] + ")");
const file = path.join(cache, "hostorig.json");
let orig; try { orig = JSON.parse(fs.readFileSync(file, "utf8")); } catch (e) { orig = {}; }
let added = 0; const diff = {};
for (const [w, ch] of Object.entries(SB.weeks)) for (const c of ch) {
  if (!c[3] || /^n\/a$/i.test(c[3]) || typeof c[4] !== "number") continue;
  const k = w + "|" + c[0] + "|" + c[1];
  if (!(k in orig)) { orig[k] = c[4]; added++; }
  else if (orig[k] !== c[4]) diff[k] = orig[k];
}
fs.writeFileSync(file, JSON.stringify(orig));
h = h.replace("var HOSTORIG={}/*HOSTORIG*/", "var HOSTORIG=" + JSON.stringify(diff) + "/*HOSTORIG*/");
fs.writeFileSync(page, h);
console.log(`hostorig: ${added} new, ${Object.keys(diff).length} changed in the sheet since`);
