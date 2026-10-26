# Year-end Rodman's Rankings: the championship sheet keeps a tab per year ("-= 2024 =-", "-=2022=-", "Rodman´s -=2016=- Rankings"...)
# with the leaderboard as it stood at the end of that year: for each path, four class blocks of Rank / Name / Points.
# Writes yearend.json: [{year, weeks, rules, paths: [[{cls, rows: [[rank, name, points], ...]}, ...] x3]}], newest year first.
import json, re, openpyxl
wb = openpyxl.load_workbook("board.xlsx", read_only=True, data_only=True)
CLASSES = ["Beginner", "Intermediate", "Advanced", "Masterclass"]
out = []
for name in wb.sheetnames:
    m = re.search(r"-=\s*(\d{4})\s*=-", name)
    if not m: continue
    ws = wb[name]
    rows = [list(r) for r in ws.iter_rows(min_row=1, max_row=250, max_col=26, values_only=True)]
    txt = lambda v: str(v).strip() if v is not None else ""
    weeks = next((txt(r[j + 1]) for r in rows[:6] for j in range(len(r) - 1) if txt(r[j]) == "Weeks"), "")
    rules = next((txt(c) for r in rows[:3] for c in r if txt(c).startswith("Rules:")), "")
    paths = [None, None, None]; cur = None
    for i, r in enumerate(rows):
        lab = " ".join(txt(c) for c in r[:2])
        if "~" in lab:   # a section title like "~ ~ Lead Guitar ~ ~" (the second cell wins, it's the one that's kept up to date)
            t = (txt(r[1]) if "~" in txt(r[1]) else "") or txt(r[0])
            cur = 0 if "Lead" in t else 1 if "Rhythm" in t else 2 if "Bass" in t else None
            continue
        start = next((j for j in range(3) if j < len(r) and txt(r[j]) == "Beginner"), None)   # the tables start in column A or B
        if cur is None or start is None: continue
        blocks = []
        for b, cls in enumerate(CLASSES):
            c0 = start + b * 5
            if len(r) <= c0 or txt(r[c0]) != cls: continue
            lst = []
            for rr in rows[i + 2:]:
                rk, nm, pt = (rr[c0] if len(rr) > c0 else None), (rr[c0 + 1] if len(rr) > c0 + 1 else None), (rr[c0 + 2] if len(rr) > c0 + 2 else None)
                if not isinstance(rk, (int, float)) or not txt(nm): break
                lst.append([int(rk), txt(nm), int(pt) if isinstance(pt, (int, float)) else 0])
            blocks.append({"cls": cls[0], "rows": lst})
        if paths[cur] is None: paths[cur] = blocks
    if any(paths):
        out.append({"year": int(m.group(1)), "weeks": weeks, "rules": rules, "paths": [p or [] for p in paths]})
out.sort(key=lambda x: -x["year"])
json.dump(out, open("yearend.json", "w"))
print("yearend:", ", ".join(f'{x["year"]} ({sum(len(b["rows"]) for p in x["paths"] for b in p)} rows)' for x in out))
