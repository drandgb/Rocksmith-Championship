# Fill the page template with the built data and write ../index.html
import json, datetime, os, hashlib, re
d = datetime.date.fromisoformat(os.environ["BUILD_DATE"]) if os.environ.get("BUILD_DATE") else datetime.date.today()
sb = json.load(open("scores.json"))
t = open("template.html").read()
h = lambda b: hashlib.md5(b).hexdigest()[:10]   # fingerprints the refresh bar uses to say "new scores" or "site update"
cv = h(t.encode() + open("render.py", "rb").read()); sc = h(json.dumps([sb["names"], sb["weeks"]], sort_keys=True).encode())   # only the scores (the rest of scores.json, like the score-check times, changes every run)
for key, f in [("__WEEKS__", "weeks.json"), ("__PLAYERS__", "players.json"), ("__PARTS__", "parts.json"),
               ("__SCORES__", "scores.json"), ("__WINS__", "wins.json"), ("__SONGS_OLD__", "songs_old.json"), ("__RANKINGS__", "rankings.json"), ("__OFFICIAL__", "official.json")]:
    assert t.count(key) == 1, f"{key} must appear exactly once in template.html (found {t.count(key)}): another placeholder shares its name"
    t = t.replace(key, open(f).read())
# "Site last updated" / "Scores last updated": kept from the previous page until the page code (cv) or the scores (sc) change
out = os.environ.get("OUT", "../../index.html")
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
prev = open(out).read() if os.path.exists(out) else ""
pm = lambda pat: (re.search(pat, prev) or [None, ""])[1]
p_sc, p_cv, p_built = pm(r'data-sc="([^"]*)"'), pm(r'data-cv="([^"]*)"'), pm(r'id="builtat" data-iso="([^"]*)"')
site_iso = now if p_cv != cv else (pm(r'id="siteat" data-iso="([^"]*)"') or p_built or now)
scores_iso = now if p_sc != sc else (pm(r'id="scoresat" data-iso="([^"]*)"') or p_built or now)
day = lambda iso: (lambda x: f"{x:%B} {x.day}, {x.year}")(datetime.datetime.fromisoformat(iso))
t = (t.replace("__SITE_ISO__", site_iso).replace("__SITE_DAY__", day(site_iso))
      .replace("__SCORES_ISO__", scores_iso).replace("__SCORES_DAY__", day(scores_iso))
      .replace("__BUILT__", f"{d:%B} {d.day}, {d.year}")
      .replace("__SCHASH__", sc).replace("__CODEHASH__", cv)
      .replace("__BUILT_ISO__", now)
      .replace("__SHEET_EDITED__", (json.load(open("cache/sheet_edited.json")) if os.path.exists("cache/sheet_edited.json") else ""))
      .replace("__TUNINGS__", open("tunings.json").read() if os.path.exists("tunings.json") else "{}")
      .replace("__YEAREND__", open("yearend.json").read() if os.path.exists("yearend.json") else "[]")
      .replace("__PLNEW__", open("plist_new.json").read() if os.path.exists("plist_new.json") else "{}")
      .replace("__LEVEL__", open("level.json").read() if os.path.exists("level.json") else "null")
      .replace("__DATAWEEK__", open("data_week.txt").read().strip())
      .replace("__SBMAX__", str(max(map(int, sb["weeks"]))))
      # medal leaders worked out by a first build of the page in headless Chrome (build.sh); null if that step was skipped
      .replace("__MLPRE__", open("ml_pre.json").read() if os.path.exists("ml_pre.json") else "null"))
left = sorted(set(re.findall(r"__[A-Z][A-Z0-9_]*__", t)))
assert not left, f"placeholders left unfilled in the page: {', '.join(left)}"
open(out, "w").write(t)
print("wrote", out, f"({len(t)//1024} KB)")
