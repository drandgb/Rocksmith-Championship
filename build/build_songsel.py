# The Songs Played sheet (in the Song Selection List spreadsheet), by week: refreshes songsel_byweek.json so the
# scoreboard checks can compare the scoreboard's song names with it.
# Reads the sheet's public CSV export; if it can't be read (for example the spreadsheet isn't shared for viewing),
# the last copy in build/data/cache (or the original snapshot) is used and the page says how old it is.
import csv, io, json, os, re, urllib.request, datetime
SSL_ID = os.environ.get("SSL_ID", "1HzgY90kLwyGqzJ-R64v8lmpeQMMhhxwGwUlenepIgms")
url = f"https://docs.google.com/spreadsheets/d/{SSL_ID}/gviz/tq?tqx=out:csv&sheet=Songs%20Played"
cached = "cache/songsel_byweek.json"
base = json.load(open(cached if os.path.exists(cached) else "songsel_byweek.json"))
info = {"live": False, "from": None}
try:
    text = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
    if text.lstrip().startswith("<"): raise ValueError("not shared (got a sign-in page)")
    rows = list(csv.reader(io.StringIO(text)))
    fresh = {}
    for r in rows:
        if len(r) < 2: continue
        m = re.fullmatch(r"\s*(\d+)(?:\.0+)?\s*", r[0] or "")
        if not m or not r[1].strip(): continue
        fresh.setdefault(str(int(m.group(1))), []).append(r[1].strip())
    if len(fresh) < 100: raise ValueError(f"only {len(fresh)} weeks found")
    base = fresh
    info = {"live": True, "from": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes")}
    print(f"songsel: read Songs Played, {len(fresh)} weeks")
except Exception as e:
    prev = json.load(open("cache/songsel_info.json")) if os.path.exists("cache/songsel_info.json") else {}
    info = {"live": False, "from": prev.get("from")}
    print("songsel: couldn't read Songs Played, using the saved copy:", e)
json.dump(base, open("songsel_byweek.json", "w"))
json.dump(base, open(cached, "w"))
json.dump({**info, "last": max(map(int, base))}, open("cache/songsel_info.json", "w"))

# Tunings: the Song Selection List tab has Tuning Lead / Tuning Rhythm / Tuning Bass columns (P, Q, R). For each song
# (artist - title) the most recently added row with a tuning wins. Written to tunings.json for the page; if the tab can't
# be read, the last saved copy is used.
def _key(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
tcache = "cache/tunings.json"
tunings = json.load(open(tcache)) if os.path.exists(tcache) else {}
try:
    turl = f"https://docs.google.com/spreadsheets/d/{SSL_ID}/gviz/tq?tqx=out:csv&headers=0&sheet=Song%20Selection%20List"
    text = urllib.request.urlopen(turl, timeout=60).read().decode("utf-8")
    if text.lstrip().startswith("<"): raise ValueError("not shared (got a sign-in page)")
    rows = list(csv.reader(io.StringIO(text)))
    hdr = next((i for i, r in enumerate(rows[:6]) if any("tuning" in (c or "").lower() for c in r)), None)
    if hdr is None: raise ValueError("no Tuning columns found")
    h = [(c or "").lower() for c in rows[hdr]]
    col = lambda *names: next((i for i, c in enumerate(h) if any(n in c for n in names)), None)
    ca, ct, cd = col("artist"), col("title"), col("date added")
    cl, cr, cb = col("tuning lead"), col("tuning rhythm"), col("tunig bass", "tuning bass")
    fresh = {}
    for n, r in enumerate(rows[hdr + 1:]):
        g = lambda i: (r[i].strip() if i is not None and i < len(r) else "")
        a, t = g(ca), g(ct)
        tl = [g(cl), g(cr), g(cb)]
        if not a or not t or not any(tl): continue
        k = _key(f"{a} - {t}")
        when = (g(cd), n)
        if k not in fresh or when >= fresh[k][0]: fresh[k] = (when, tl)
    tunings = {k: v[1] for k, v in fresh.items()}
    json.dump(tunings, open(tcache, "w"))
    print(f"songsel: {len(tunings)} songs with tunings")
except Exception as e:
    print("songsel: couldn't read tunings, using the saved copy:", e)
json.dump(tunings, open("tunings.json", "w"))
