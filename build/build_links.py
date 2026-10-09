# Download links for the Scoreboard: the Ignition4 (CustomsForge) links that the song titles on each
# WeekNNN tab are hyperlinked to. Adds "links": {week: {path*9+slot: cdlc id}} to scores.json.
# Each link is checked once (results kept in cache/links_check.json) and links that turn out to be dead
# are left out. Set LINK_CHECK=0 to skip the checks (links that were never checked are then kept).
import json, os, re, time, zipfile, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

z = zipfile.ZipFile("board.xlsx")
wbx = z.read("xl/workbook.xml").decode()
def rels_of(xml):
    m = {a: b for a, b in re.findall(r'Id="(rId\d+)"[^>]*?Target="([^"]+)"', xml)}
    m.update({a: b for b, a in re.findall(r'Target="([^"]+)"[^>]*?Id="(rId\d+)"', xml)})
    return m
wrels = rels_of(z.read("xl/_rels/workbook.xml.rels").decode())
def colnum(s):
    n = 0
    for ch in s: n = n * 26 + ord(ch) - 64
    return n

links = {}
for name, rid in re.findall(r'<sheet [^>]*?name="Week(\d+)"[^>]*?r:id="(rId\d+)"', wbx):
    path = "xl/" + wrels[rid].lstrip("/").replace("xl/", "", 1)
    rpath = path.replace("worksheets/", "worksheets/_rels/") + ".rels"
    if rpath not in z.namelist(): continue
    tg = rels_of(z.read(rpath).decode())
    for r, col in re.findall(r'<hyperlink r:id="(rId\d+)" ref="([A-Z]+)6"', z.read(path).decode()):
        m = re.match(r"https?://ignition4?\.customsforge\.com/cdlc/(\d+)", tg.get(r, ""))
        c = colnum(col)
        if not m or (c - 2) % 5 or not 0 <= (c - 2) // 5 < 27: continue   # only song titles (row 6 of each card)
        links.setdefault(name, {})[str((c - 2) // 5)] = int(m.group(1))   # card block = path*9 + slot

# ---- check that each linked CDLC page still exists ----
CK = "cache/links_check.json"
check = json.load(open(CK)) if os.path.exists(CK) else {}
now = int(time.time())
def due(i):
    c = check.get(str(i))
    if not c: return True
    return c[0] == "bad" and now - c[1] > 30 * 86400 or c[0] == "unknown" and now - c[1] > 7 * 86400   # re-check dead links monthly
def probe(i):
    url = f"https://ignition4.customsforge.com/cdlc/{i}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Rocksmith Championship stats site link check)"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read(200000).decode("utf-8", "replace"); final = resp.geturl()
        title = re.sub(r"\s+", " ", (re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I) or [None, ""])[1]).strip()
        if f"/cdlc/{i}" not in final or re.search(r"not found|404|does not exist|no longer available", title, re.I):
            return i, "bad", f"200 → {final} · {title}"
        return i, "ok", title
    except urllib.error.HTTPError as e:
        return i, "bad" if e.code in (404, 410) else "unknown", f"HTTP {e.code}"
    except Exception as e:
        return i, "unknown", type(e).__name__
if os.environ.get("LINK_CHECK", "1") != "0":
    ids = sorted({i for w in links.values() for i in w.values() if due(i)}, reverse=True)[:int(os.environ.get("LINK_CHECK_MAX", "3000"))]
    if ids:
        res = list(ThreadPoolExecutor(6).map(probe, ids + [999999999]))
        print("link check, nonexistent id 999999999 →", res[-1][1:])
        for i, st, info in res[:-1]: check[str(i)] = [st, now]
        cnt = {s: sum(1 for r in res[:-1] if r[1] == s) for s in ("ok", "bad", "unknown")}
        print(f"link check: {len(ids)} checked · {cnt}")
        for r in res[:3] + [r for r in res[:-1] if r[1] != "ok"][:10]: print("  ", r)
    json.dump(check, open(CK, "w"), separators=(",", ":"))

out = {w: {b: i for b, i in v.items() if check.get(str(i), ["?"])[0] != "bad"} for w, v in links.items()}
out = {w: v for w, v in out.items() if v}
sb = json.load(open("scores.json")); sb["links"] = out
json.dump(sb, open("scores.json", "w"), separators=(",", ":"))
print(f"download links: {sum(len(v) for v in out.values())} kept across {len(out)} weeks"
      f" ({sum(len(v) for v in links.values()) - sum(len(v) for v in out.values())} dead links left out)")
