# The Songs Played sheet (in the Song Selection List spreadsheet), by week: refreshes songsel_byweek.json so the
# scoreboard checks can compare the scoreboard's song names with it.
# Reads the sheet's public CSV export; if it can't be read (for example the spreadsheet isn't shared for viewing),
# the last copy in build/data/cache (or the original snapshot) is used and the page says how old it is.
import urllib.parse
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

# Tunings: the Song Selection List tab has Tuning Lead / Tuning Rhythm / Tuning Bass columns (P, Q, R). Songs leave that tab
# once they're played, so every tuning ever read is kept in the cache (a song's newest reading wins), and the other tabs that
# have Tuning columns are read too. For each song (artist - title) the most recently added row with a tuning wins.
# Written to tunings.json for the page; if nothing can be read, the saved copy is used.
def _key(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
tcache = "cache/tunings.json"
tunings = json.load(open(tcache)) if os.path.exists(tcache) else {}
TUNE_TABS = ["Song Selection List", "SSL - Played", "SSL - spare arrangements", "Xmas Song Selection List", "Only Bass Songs", "Only Guitar Songs", "Extra  Base"]
def read_tunings(tab):
    turl = f"https://docs.google.com/spreadsheets/d/{SSL_ID}/gviz/tq?tqx=out:csv&headers=0&sheet={urllib.parse.quote(tab)}"
    text = urllib.request.urlopen(turl, timeout=60).read().decode("utf-8")
    if text.lstrip().startswith("<"): raise ValueError("not shared (got a sign-in page)")
    rows = list(csv.reader(io.StringIO(text)))
    hdr = next((i for i, r in enumerate(rows[:8]) if any("tuning" in (c or "").lower() or "tunig" in (c or "").lower() for c in r)), None)
    if hdr is None: return {}
    h = [(c or "").lower() for c in rows[hdr]]
    col = lambda *names: next((i for i, c in enumerate(h) if any(n in c for n in names)), None)
    ca, ct, cd = col("artist"), col("title"), col("date added")
    cl, cr, cb = col("tuning lead", "tunig lead"), col("tuning rhythm", "tunig rhythm"), col("tunig bass", "tuning bass")
    fresh = {}
    for n, r in enumerate(rows[hdr + 1:]):
        g = lambda i: (r[i].strip() if i is not None and i < len(r) else "")
        a, t = g(ca), g(ct)
        tl = [g(cl), g(cr), g(cb)]
        if not a or not t or not any(tl): continue
        k = _key(f"{a} - {t}")
        when = (g(cd), n)
        if k not in fresh or when >= fresh[k][0]: fresh[k] = (when, tl)
    return {k: v[1] for k, v in fresh.items()}
# the NewWeek tab (and its saved copies) lists each week's songs per path with their tuning: a block per path whose first
# cell is "Lead", "Rhythm" or "Bass", then one row per class: Artist, Song Title (or "Artist - Song Title"), Rating, Tuning
NEWWEEK_TABS = ["NewWeek", "Bak_NewWeek", "Backup of NewWeek 20241025"]
def read_newweek(tab):
    turl = f"https://docs.google.com/spreadsheets/d/{SSL_ID}/gviz/tq?tqx=out:csv&headers=0&sheet={urllib.parse.quote(tab)}"
    text = urllib.request.urlopen(turl, timeout=60).read().decode("utf-8")
    if text.lstrip().startswith("<"): raise ValueError("not shared (got a sign-in page)")
    return newweek_rows(list(csv.reader(io.StringIO(text))))
def newweek_rows(rows):
    out, path, cols = {}, None, None
    for r in rows:
        c = [(x or "").strip() for x in r]
        low = [x.lower() for x in c]
        p = next((i for i, x in enumerate(low[:3]) if x in ("lead", "rhythm", "bass")), None)
        if p is not None:
            path = ["lead", "rhythm", "bass"].index(low[p])
            if "tuning" in low: cols = {"a": next((i for i, x in enumerate(low) if x.startswith("artist")), None),
                                        "t": next((i for i, x in enumerate(low) if x == "song title"), None),
                                        "u": low.index("tuning")}
            continue
        if path is None or not cols: continue
        g = lambda i: c[i] if i is not None and i < len(c) else ""
        tu = g(cols["u"])
        if not tu or tu.lower() in ("none", "tuning"): continue
        a, t = g(cols["a"]), g(cols["t"])
        if cols["t"] is None and " - " in a: a, t = a.split(" - ", 1)
        if not a or not t: continue
        out.setdefault(_key(f"{a} - {t}"), ["", "", ""])[path] = tu
    return out
read_any = False
for tab in NEWWEEK_TABS[::-1]:   # the live NewWeek tab last, so its readings win
    try:
        got = read_newweek(tab); read_any = True
        for k, v in got.items():
            old = tunings.get(k, ["", "", ""])
            tunings[k] = [v[i] or old[i] for i in range(3)]
        print(f"songsel: {len(got)} songs with tunings in {tab}")
    except Exception as e:
        print(f"songsel: couldn't read tunings from {tab}:", e)
for tab in reversed(TUNE_TABS):   # the main tab last, so its readings win
    try:
        got = read_tunings(tab); read_any = True
        for k, v in got.items():   # keep what an earlier reading knew for a path this one leaves blank
            old = tunings.get(k, ["", "", ""])
            tunings[k] = [v[i] or old[i] for i in range(3)]
        print(f"songsel: {len(got)} songs with tunings in {tab}")
    except Exception as e:
        print(f"songsel: couldn't read tunings from {tab}:", e)
if read_any:
    json.dump(tunings, open(tcache, "w"))
print(f"songsel: {len(tunings)} songs with tunings in all")
json.dump(tunings, open("tunings.json", "w"))
