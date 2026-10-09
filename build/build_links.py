# Download links for the Scoreboard: the Ignition4 (CustomsForge) links that the song titles on each
# WeekNNN tab are hyperlinked to. Adds "links": {week: {path*9+slot: cdlc id}} to scores.json.
# The links are taken as they are: the Ignition4 site is never contacted by the build.
import json, re, zipfile

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

out = links
sb = json.load(open("scores.json")); sb["links"] = out
json.dump(sb, open("scores.json", "w"), separators=(",", ":"))
print(f"download links: {sum(len(v) for v in out.values())} across {len(out)} weeks")
