# Player levels: Rodman's "PlayerLevel" tab in the championship sheet. For each path (Lead, Rhythm, Bass) it lists every player
# with their XP level now (needs 3+ score entries in the recent window), over the last 6 months, and for each year
# (5+ entries that year). Writes level.json: {weeks, last, years, paths: [[{n, xp, m6, y: {year: level}}, ...] x3]}.
import json, openpyxl
wb = openpyxl.load_workbook("board.xlsx", read_only=True, data_only=True)
name = next((n for n in wb.sheetnames if n.replace(" ", "").lower() == "playerlevel"), None)
if not name:
    raise SystemExit("PlayerLevel tab not found")
rows = [list(r) for r in wb[name].iter_rows(min_row=1, max_row=1200, max_col=48, values_only=True)]
txt = lambda v: str(v).strip() if v is not None else ""
def num(v):
    try:
        x = float(v)
        return round(x, 2) if x > 0 else None
    except (TypeError, ValueError):
        return None
info = {}
for r in rows[:4]:
    for j in range(len(r) - 1):
        if txt(r[j]) == "Weeks scored": info["weeks"] = num(r[j + 1])
        if txt(r[j]) == "Last week scored": info["last"] = num(r[j + 1])
# the header row has "Name" in each block; the year columns follow "last 6 Moths"
hi = next(i for i, r in enumerate(rows) if sum(1 for c in r if txt(c) == "Name") >= 3)
head = rows[hi]
starts = [j for j, c in enumerate(head) if txt(c) == "Name"][:3]
paths, years = [], []
for s in starts:
    ycols = [(j, int(float(head[j]))) for j in range(s + 3, min(s + 16, len(head))) if txt(head[j]).replace(".0", "").isdigit()]
    if not years: years = [y for _, y in ycols]
    lst = []
    for r in rows[hi + 1:]:
        n = txt(r[s]) if s < len(r) else ""
        if not n or n == "#REF!": continue
        y = {str(yr): num(r[j]) for j, yr in ycols if num(r[j])}
        p = {"n": n, "xp": num(r[s + 1]), "m6": num(r[s + 2]), "y": y}
        if p["xp"] or p["m6"] or y: lst.append(p)
    paths.append(lst)
json.dump({"weeks": info.get("weeks"), "last": info.get("last"), "years": years, "paths": paths}, open("level.json", "w"))
print("level:", [len(p) for p in paths], "players per path, years", years[:1], "to", years[-1:])
