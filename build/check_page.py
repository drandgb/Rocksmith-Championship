# Check a built page before it goes live: open it in headless Chrome, open every tab, and fail if any tab is empty
# or the page's code hits an error.
#   python3 build/check_page.py [index.html]
# Exit code 0: fine. 1: problems found (listed). 0 with a note: Chrome or playwright isn't available, nothing checked.
# Nothing is loaded from the internet (fonts, database): only the page's own code is checked.
import os, shutil, sys

page = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "index.html")
chrome = os.environ.get("CHROME") or next((shutil.which(c) for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(c)), None)
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("check: playwright isn't installed, nothing checked"); sys.exit(0)

TABS = ["thisweek", "level", "rankings", "season", "hosting", "players", "winners", "scores", "songs", "faq"]
problems = []
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=chrome, args=["--no-sandbox"]) if chrome else pw.chromium.launch()
    for width in (1300, 390):  # a computer and a phone
        pg = br.new_page(viewport={"width": width, "height": 900})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.route("**/*", lambda r: r.continue_() if r.request.url.startswith("file:") else r.abort())
        pg.goto("file://" + page, wait_until="load")
        pg.wait_for_timeout(3000)
        for t in TABS:
            try:
                pg.evaluate("v=>showView(v)", t)
            except Exception as e:
                problems.append(f"{width}px: couldn't open the {t} tab: {e}"); continue
            pg.wait_for_timeout(400)
            size = pg.evaluate("v=>{const el=document.getElementById('view-'+v); return el&&!el.hidden?el.innerText.trim().length:-1}", t)
            if size < 50:
                problems.append(f"{width}px: the {t} tab is empty")
        problems += [f"{width}px: page error: {e}" for e in errors]
        pg.close()
    br.close()

if problems:
    print("check: problems found in " + os.path.basename(page) + ":")
    for p in problems[:30]:
        print("  - " + p)
    sys.exit(1)
print(f"check: {os.path.basename(page)} is fine ({len(TABS)} tabs, computer and phone widths)")
