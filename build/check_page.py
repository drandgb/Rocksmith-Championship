# Check a built page before it goes live: open it in headless Chrome, open every tab, and fail if any tab is empty,
# the page's code hits an error (also one a section catches and logs), two functions share a name (the later one
# silently replaces the earlier), a template placeholder was left unfilled, or the footer is far too long (data ended up in it). With --compare OLD.html, also fail if a section that had content on the old page is
# now gone, hidden or mostly empty.
#   python3 build/check_page.py [index.html] [--compare old.html]
# Exit code 0: fine. 1: problems found (listed). 0 with a note: Chrome or playwright isn't available, nothing checked.
# Nothing is loaded from the internet (fonts, database): only the page's own code is checked.
import os, re, shutil, sys

args = [a for a in sys.argv[1:] if a != "--compare"]
cmp_i = sys.argv.index("--compare") if "--compare" in sys.argv else -1
base = os.path.abspath(sys.argv[cmp_i + 1]) if cmp_i >= 0 and cmp_i + 1 < len(sys.argv) else None
if base: args = [a for a in args if os.path.abspath(a) != base]
page = os.path.abspath(args[0] if args else "index.html")
chrome = os.environ.get("CHROME") or next((shutil.which(c) for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(c)), None)
problems = []

# 1. two top-level functions (or vars) with the same name: no error, the later one just replaces the earlier
src = open(page, encoding="utf-8").read()
seen = {}
for sc in re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", src, re.S):
    for m in re.finditer(r"^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(|^var\s+([A-Za-z_$][\w$]*)\s*=", sc, re.M):
        n = m.group(1) or m.group(2); seen[n] = seen.get(n, 0) + 1
problems += [f"two definitions named {n}: the second replaces the first" for n, c in sorted(seen.items()) if c > 1]
# 2. a template placeholder (like __SCORES__) left in the page, unfilled
left = sorted(set(re.findall(r"__[A-Z][A-Z0-9_]*__", src)))
problems += [f"placeholder {n} was left in the page unfilled" for n in left]

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    for p in problems: print("  - " + p)
    print("check: playwright isn't installed, the page itself wasn't opened"); sys.exit(1 if problems else 0)

TABS = ["thisweek", "level", "rankings", "season", "hosting", "players", "winners", "scores", "songs", "faq"]
NOISE = re.compile(r"net::ERR|Failed to load resource|ERR_FAILED|ERR_ABORTED")
SECTIONS = """v=>[...document.querySelectorAll('#view-'+v+' section')].map((s,i)=>{const h=s.querySelector('h2');
  return {k:s.id||(h?h.textContent.trim().slice(0,40):'')||('#'+i), vis:!s.hidden&&s.offsetParent!==null, n:s.innerText.trim().length}})"""

def visit(br, path, width, errors_too=True):
    pg = br.new_page(viewport={"width": width, "height": 900})
    errs, secs = [], {}
    pg.on("pageerror", lambda e: errs.append(str(e).split("\n")[0]))
    pg.on("console", lambda m: m.type == "error" and not NOISE.search(m.text) and errs.append(m.text.split("\n")[0][:200]))
    pg.route("**/*", lambda r: r.continue_() if r.request.url.startswith("file:") else r.abort())
    pg.goto("file://" + path, wait_until="load")
    pg.wait_for_timeout(3000)
    # 3. the footer is a few short lines: much longer means data ended up in it (a placeholder filled with the wrong thing)
    ft = pg.evaluate("()=>{const f=document.querySelector('footer'); return f?f.innerText.trim().length:0}")
    if ft > 1500: errs.append(f"the footer is {ft} characters long (it should be a few short lines): data ended up in it")
    tabs = {}
    for t in TABS:
        try:
            pg.evaluate("v=>showView(v)", t)
        except Exception as e:
            tabs[t] = -2; continue
        pg.wait_for_timeout(400)
        tabs[t] = pg.evaluate("v=>{const el=document.getElementById('view-'+v); return el&&!el.hidden?el.innerText.trim().length:-1}", t)
        for s in pg.evaluate(SECTIONS, t): secs[(t, s["k"])] = s
    pg.close()
    return tabs, secs, errs

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=chrome, args=["--no-sandbox"]) if chrome else pw.chromium.launch()
    new_secs = None
    for width in (1300, 390):  # a computer and a phone
        tabs, secs, errs = visit(br, page, width)
        if width == 1300: new_secs = secs
        problems += [f"{width}px: couldn't open the {t} tab" for t, n in tabs.items() if n == -2]
        problems += [f"{width}px: the {t} tab is empty" for t, n in tabs.items() if -2 < n < 50]
        problems += [f"{width}px: error: {e}" for e in dict.fromkeys(errs)]
    # 4. sections that had content before and lost it
    if base and os.path.exists(base):
        _, old_secs, _ = visit(br, base, 1300)
        for key, o in old_secs.items():
            if not o["vis"] or o["n"] < 40: continue
            nw = new_secs.get(key)
            if not nw: problems.append(f"the {key[0]} tab's '{key[1]}' section is gone")
            elif not nw["vis"]: problems.append(f"the {key[0]} tab's '{key[1]}' section is now hidden (it had content)")
            elif nw["n"] < o["n"] * 0.3: problems.append(f"the {key[0]} tab's '{key[1]}' section lost most of its content ({o['n']} → {nw['n']} characters)")
    br.close()

if problems:
    print("check: problems found in " + os.path.basename(page) + ":")
    for p in list(dict.fromkeys(problems))[:40]:
        print("  - " + p)
    sys.exit(1)
print(f"check: {os.path.basename(page)} is fine ({len(TABS)} tabs, computer and phone widths{', every section compared with ' + os.path.basename(base) if base else ''})")
