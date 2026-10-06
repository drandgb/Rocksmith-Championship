# Player list, attendance and players-per-week.
# Attendance history (old Metrics workbook) is saved for weeks 2-675. From week 440 on, anyone on that week's
# scoreboard also counts as played (the scoreboard fills in players the Metrics workbook missed); from week 676 on
# the scoreboard is the only source. Week 565's scoreboard tab is incomplete, so history is kept rather than replaced.
# A score that just carries over on a multi-week God challenge (identical to last week's) doesn't count as playing.
import openpyxl, json, collections, sys

ALIAS = {'AndreCardoso': 'ALSRC', 'BetterCallJamie': 'FlatCap Jay', 'jasmith85': 'FlatCap Jay', 'aand14': 'drand',
         'mattimatti': 'mattibassi', 'Tinman86': 'TinMan86'}
DROP = {'#REF!', 'Player Name'}
SB_START = 440
data_week = int(open("data_week.txt").read())
H = json.load(open("presence_hist.json"))
hist, HIST_END = H["players"], H["through_week"]     # name -> [tiers, bits for weeks 2..HIST_END]
parts_hist = json.load(open("parts_hist.json"))     # players per week, weeks 2..439
sb = json.load(open("scores.json"))

# PlayersList tab: name, Lead, Rhythm, Bass, ... (only used for classes; every name on a scoreboard counts as a player)
wb = openpyxl.load_workbook("board.xlsx", read_only=True, data_only=True)
tiers = {}
for r in wb["PlayersList"].iter_rows(min_row=2, values_only=True):
    if not r or not r[0]: continue
    n = str(r[0]).strip()
    if n in ALIAS: continue
    t = "".join((str(x).strip().upper()[:1] if x not in (None, "") else "?") for x in r[1:4])
    tiers[n] = t

canon = {}
for n in hist: canon.setdefault(n.lower(), n)
for n in tiers: canon[n.lower()] = n                 # the PlayersList spelling wins

n_hist = min(HIST_END, data_week) - 1
nbits = data_week - 1                                # weeks 2..data_week
pres = collections.defaultdict(lambda: bytearray(b"0" * nbits))
for n, (t, bits) in hist.items():
    c = canon[n.lower()]
    b = pres[c]
    for i, ch in enumerate(bits[:n_hist]):
        if ch == "1": b[i] = ord("1")

def is_god(level):
    l = (level or "").lower()
    return l.startswith("god") or "tribute" in l

def god_entries(w):
    # (path, song, name, %, streak) for every entry on a God / tribute card that week. The score column is left out:
    # hosts sometimes blank a carried-over score (0 one week, empty the next), which isn't a new submission
    out = set()
    for card in sb["weeks"].get(str(w), []):
        if not is_god(card[2]): continue
        for e in card[6]:
            out.add((card[0], card[3].strip().lower(), sb["names"][e[0]].rstrip("*~").strip(), e[1], e[2]))
    return out

unknown = collections.Counter()
for w in range(SB_START, data_week + 1):
    seen = set()
    prev_god = god_entries(w - 1)
    for card in sb["weeks"].get(str(w), []):
        for e in card[6]:
            # a multi-week God challenge keeps last week's scores on the board; an identical entry is not a new
            # submission, so it doesn't count as playing this week
            if is_god(card[2]) and (card[0], card[3].strip().lower(), sb["names"][e[0]].rstrip("*~").strip(), e[1], e[2]) in prev_god:
                continue
            raw = sb["names"][e[0]].rstrip("*~").strip()
            raw = ALIAS.get(raw, raw)
            if raw in DROP or not raw: continue
            c = canon.get(raw.lower())
            if c is None:                            # first time this name shows up anywhere: a new player
                c = canon[raw.lower()] = raw; unknown[raw] = w
            seen.add(c)
    for c in seen: pres[c][w - 2] = ord("1")
# players per week: saved Metrics counts before the scoreboard era, then counted from attendance
parts = list(parts_hist[:SB_START - 2]) + [sum(1 for b in pres.values() if b[w - 2] == ord("1")) for w in range(SB_START, data_week + 1)]

players = []
for n, b in pres.items():
    bits = b.decode()
    ws = [i + 2 for i, ch in enumerate(bits) if ch == "1"]
    if not ws: continue
    best = run = 0; prev = None
    for w in ws:
        run = run + 1 if prev == w - 1 else 1; prev = w; best = max(best, run)
    act = 0; w = data_week
    while w >= 2 and bits[w - 2] == "1": act += 1; w -= 1
    first = ws[0]
    padded = bits + "0" * (-len(bits) % 4)
    hx = "".join(format(int(padded[i:i + 4], 2), "x") for i in range(0, len(padded), 4))
    t = tiers.get(n) or (hist.get(n) or [None])[0]
    players.append([n, first, ws[-1], len(ws), round(len(ws) / (data_week - first + 1), 4), act, best, hx, t])

json.dump(players, open("players.json", "w"), separators=(",", ":"))
json.dump(parts, open("parts.json", "w"))
print(f"players {len(players)}, weeks 2-{data_week}")
if unknown:   # worth a glance in the build log, in case one of these is a typo of an existing name
    print("New player names (first week seen):", ", ".join(f"{n} ({w})" for n, w in sorted(unknown.items(), key=lambda x: x[1])))
