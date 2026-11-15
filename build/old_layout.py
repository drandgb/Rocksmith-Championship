# Reader for the older scoreboard layouts (weeks 2-435), used by parse_weeks.py.
#   weeks 14-435: "Name / % / Streak [/ Score]" headers on row 8, level labels on row 7, songs on row 6,
#                 Lead / Rhythm / Bass section titles on row 5
#   weeks 2-13:   "Points / Name" pairs on row 7, classes on row 6, songs on row 5; the score is text such as
#                 "143,241 (98.90)" (score, %) or "100.00% (789)" (%, streak)
# A name listed without a score is a class roster entry, not someone who played, so it is left out.
import re
NA = {"", "n/a", "na", "not available", '"not available"', "-", "x", "zzz", "tba", "tbd"}
BASE = {"B": 0, "I": 2, "A": 4, "M": 6}
def level(l):
    l = l.lower()
    if l.startswith("god") or l.startswith("gog"): return "G"
    if "master" in l or l == "hard": return "M"
    if l.startswith("adv") or "advanced" in l: return "A"
    if l.startswith("int") or "inter" in l or l == "medium": return "I"
    if "begin" in l or l.startswith("beg") or l == "easy": return "B"
def fnum(v):
    if isinstance(v, bool): return None
    if isinstance(v, (int, float)): return v
    if isinstance(v, str):
        s = v.strip().rstrip("%").replace(" ", "")
        if re.fullmatch(r"\d+,\d{1,2}", s): s = s.replace(",", ".")      # 97,5
        s = s.replace(",", "")
        try: return float(s)
        except ValueError: return None
def points(v):
    # -> (%, streak, score) from the text of an early "Points" cell
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return (v, None, None) if 0 < v <= 100 else (None, None, v)
    s = str(v or "").strip()
    m = re.fullmatch(r"([\d.,]+)\s*%?\s*\(\s*([\d.,]+)\s*%?\s*\)?", s)
    if m:
        a, b = m.group(1), m.group(2)
        if "%" in s.split("(")[0] or (fnum(a) is not None and fnum(a) <= 100 and "," not in a and "." in a and "." not in b):
            return (fnum(a), fnum(b), None)                              # 100.00% (789)
        return (fnum(b), None, fnum(a.replace(",", "")))                 # 143,241 (98.90)
    p = fnum(s)
    if p is not None and 0 < p <= 100: return (p, None, None)
    return (None, None, None)
def color(f):
    c = f.color
    if c is None: return None
    return c.rgb if c.type == "rgb" else "theme"
def slots(cards):
    # cards of one path, left to right: [level, label] -> slot 0-8 for each (None = no room). A level's first card takes
    # its usual slot and its second the bonus slot next to it; a third takes the nearest free slot (the label says what it is)
    used, out = set(), []
    for lv, label in cards:
        if lv == "G": s = 8 if 8 not in used else None
        else:
            s = next((x for x in (BASE[lv], BASE[lv] + 1) if x not in used), None)
            if s is None: s = min((x for x in range(8) if x not in used), key=lambda x: abs(x - BASE[lv] - 1), default=None)
        if s is not None: used.add(s)
        out.append(s)
    return out
NAMES = {"B": "Beginner", "I": "Intermediate", "A": "Advanced", "M": "Masterclass"}
def read_old(wk, grid):
    """-> (challenges, fonts by block, notes) or None when the tab isn't a scoreboard"""
    H, W = len(grid), max(len(r) for r in grid)
    cell = lambda r, c: grid[r - 1][c - 1] if 0 < r <= H and 0 < c <= len(grid[r - 1]) else None
    val = lambda r, c: getattr(cell(r, c), "value", None)
    sval = lambda r, c: str(val(r, c)).strip() if isinstance(val(r, c), str) else ""
    notes, cards = [], []          # card: dict(path, lv, label, song, diff, ents, fl)
    def rows(c, get, first):
        ents, fl = [], []
        for r in range(first, H + 1):
            n = val(r, c)
            if n in (None, "") or not str(n).strip(): continue
            pct, streak, score = get(r)
            if pct is None or not (0 < pct <= 100): continue             # listed without a score: didn't play
            # notes after a name, e.g. "(1dl)", "(Int)", "(aka Krazyone)", aren't part of it
            name = re.sub(r"\s*\((?:\d[du]l|m|mm|ab|bb|int|aka [^)]*)\)", "", str(n).strip(), flags=re.I)
            name = re.sub(r"\s+([*~]+)$", r"\1", name)
            ents.append([name, pct, streak, score])
            f = cell(r, c).font
            fl.append([name, color(f), bool(f.b), f.sz, False])
        return ents, fl
    if sval(8, 2) == "Name" or any(sval(8, c) == "Name" for c in range(1, W + 1)):
        cols = [c for c in range(1, W + 1) if sval(8, c) == "Name"]
        # a few cards have lost their "Name" header: the level label on row 7 marks those
        cols = sorted(set(cols) | {c for c in range(2, W + 1) if level(sval(7, c)) and c not in cols and c + 1 not in cols
                                   and any(isinstance(val(r, c), str) for r in range(9, min(H, 20) + 1))})
        sec = sorted((c, t) for c in range(1, W + 1) if (t := sval(5, c)))
        def path_of(c):
            p = None
            for sc, t in sec:
                if sc > c + 1: break
                tl = t.lower()
                p = 0 if "lead" in tl else 1 if "rhythm" in tl else 2 if "bass" in tl else -1   # -1: tribute / Da Capo
            return p
        for i, c in enumerate(cols):
            end = cols[i + 1] - 2 if i + 1 < len(cols) else c + 4
            span = range(c - 1, end + 1)
            label = next((sval(7, k) for k in span if sval(7, k) and sval(7, k) not in ("Level>",) and not re.fullmatch(r"[\d,.?+]+", sval(7, k)) and level(sval(7, k))), "")
            anyl = next((sval(7, k) for k in span if sval(7, k) and sval(7, k) != "Level>"), "")
            diff = next((fnum(val(7, k)) for k in span if k >= c and fnum(val(7, k)) is not None and not isinstance(val(7, k), str) or (isinstance(val(7, k), str) and re.fullmatch(r"\d+,5", val(7, k).strip()))), None)
            song = next((sval(6, k) for k in span if sval(6, k) and sval(6, k) != "Song>"), "")
            hd = [sval(8, k) for k in range(c + 1, end + 2)]
            has_score = len(hd) > 2 and c + 3 <= end + 1 and hd[2] in ("Score", "Points", "") and (i + 1 == len(cols) or cols[i + 1] > c + 3)
            def get(r, c=c, has_score=has_score):
                sc = fnum(val(r, c + 3)) if has_score else None
                return fnum(val(r, c + 1)), fnum(val(r, c + 2)), sc if sc and sc > 1000 else None
            ents, fl = rows(c, get, 9)
            cards.append(dict(c=c, path=path_of(c), label=label, anyl=anyl, song=song, diff=diff, ents=ents, fl=fl, hd=hd))
        # the section titles don't always sit over the right card (and weeks 150-187 have no Bass title), so a path
        # also starts where the levels start over: a Beginner card right after an Advanced, Masterclass or God card
        seq = [k for k in cards if k["path"] in (0, 1, 2) and level(k["label"])]
        bonus = lambda k: bool(re.search(r"bonus|alt|2", k["label"].lower()))
        drops = [i for i in range(1, len(seq)) if level(seq[i]["label"]) == "B" and level(seq[i - 1]["label"]) in "AMG"]
        # a bonus card at the end of a path belongs to that path: the next one starts at the plain Beginner card after it
        drops = [i + 1 if bonus(seq[i]) and i + 1 < len(seq) and level(seq[i + 1]["label"]) == "B" and not bonus(seq[i + 1]) else i for i in drops]
        if len(drops) == 2:
            for i, k in enumerate(seq):
                p = 0 if i < drops[0] else 1 if i < drops[1] else 2
                k["path"] = p
    elif sval(7, 3) == "Name" or any(sval(7, c) == "Name" for c in range(1, W + 1)):
        cols = [c for c in range(1, W + 1) if sval(7, c) == "Name"]
        starts = [c for c in range(1, W + 1) if sval(6, c) == "Class"]
        secs = []
        for c in cols:
            s = max([x for x in starts if x < c], default=1)
            if s not in secs: secs.append(s)
        for c in cols:
            s = max([x for x in starts if x < c], default=1)
            label = next((sval(6, k) for k in range(c - 1, s, -1) if sval(6, k)), "")
            song = next((sval(5, k) for k in range(c - 1, s, -1) if sval(5, k)), "")
            def get(r, c=c): return points(val(r, c - 1))
            ents, fl = rows(c, get, 8)
            cards.append(dict(c=c, sec=s, label=label, anyl=label, song=song, diff=None, ents=ents, fl=fl, hd=[]))
        live = [s for s in secs if any(k["sec"] == s and k["ents"] for k in cards)]
        for k in cards:
            t = k["song"].lower()
            m = re.search(r"\((?:guitar\s+)?(lead|rhythm|bass)\)\s*$", t)
            if m: k["path"] = ("lead", "rhythm", "bass").index(m.group(1))
            elif k["sec"] in live: k["path"] = live.index(k["sec"]) if len(live) != 2 else (0, 2)[live.index(k["sec"])]
            else: k["path"] = -1
            k["song"] = re.sub(r"\s*\((?:guitar\s+)?(lead|rhythm|bass)\)\s*$", "", k["song"], flags=re.I)
    else:
        return None
    chal, frows = [], {}
    for p in (0, 1, 2):
        mine = []
        for k in cards:
            if k["path"] != p: continue
            song = "" if k["song"].lower() in NA else k["song"]
            if not k["ents"] and (not song or wk < 14): continue             # weeks 2-13 share one song across a section
            lv = level(k["label"])
            if not lv or "da capo" in k["label"].lower() or song.lower().startswith("combined"):
                if k["ents"]: notes.append(f"skipped card '{k['anyl']}' col {k['c']} ({len(k['ents'])} scores)")
                continue
            k["song"] = song; mine.append((lv, k))
        sl = slots([(lv, k["label"]) for lv, k in mine])
        seen = set()
        for s, (lv, k) in zip(sl, mine):
            if lv == "G": k["label"] = ("God of Guitar", "God of Rhythm", "God of Bass")[p]
            else: k["label"] = NAMES[lv] + (" Bonus" if lv in seen else ""); seen.add(lv)
            if s is None:
                if k["ents"]: notes.append(f"no slot for '{k['label']}' col {k['c']} ({len(k['ents'])} scores)")
                continue
            chal.append([p, s, k["label"], k["song"], k["diff"], "", k["ents"]]); frows[p * 9 + s] = k["fl"]
    for k in cards:
        if k["path"] not in (0, 1, 2) and k["ents"]: notes.append(f"outside the three paths: '{k['anyl']}' col {k['c']} ({len(k['ents'])} scores)")
    chal.sort(key=lambda x: (x[0], x[1]))
    return chal, frows, notes
