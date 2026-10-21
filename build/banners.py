# Forum signature banners for players with an approved profile claim.
#   python3 build/banners.py [index.html] [cards dir]
# Reads the approved claims from the site's database (the same public read the site itself does), then screenshots
# each player's banner from the built page in headless Chrome (bannerHtml() in the page, opened with ?banner=) into
# cards/<slug>.png (700x150).
#   - every banner is redrawn when a new week's results arrive (or when BANNER_VERSION changes)
#   - otherwise only newly approved players get one, so this is cheap to run every few minutes
#   - when a claim is removed, the admin chooses whether the banner stays (and keeps updating) or is deleted
# If the claims can't be read, nothing is changed.
import json, os, re, shutil, sys, urllib.request

BANNER_VERSION = 22  # bump to redraw every banner after a design change

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "index.html"))
out = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(page), "cards"))
html = open(page, encoding="utf-8").read()

def grab(pat):
    m = re.search(pat, html)
    return m.group(1) if m else None

url, key = grab(r'SUPA_URL="([^"]+)"'), grab(r'SUPA_KEY="([^"]+)"')
if not url or not key:
    print("banners: no database settings in the page, skipped"); sys.exit(0)
week = grab(r"Player stats run through week (\d+)") or "?"  # the week the page was built for (in the footer)

try:
    if os.environ.get("BANNER_TEST_PLAYERS"):  # local testing without the database: comma-separated names
        rows = [{"player": n} for n in os.environ["BANNER_TEST_PLAYERS"].split(",")]
    else:
      req = urllib.request.Request(f"{url}/rest/v1/claims?select=player&status=eq.approved",
                                   headers={"apikey": key, "Authorization": f"Bearer {key}"})
      rows = json.load(urllib.request.urlopen(req, timeout=30))
except Exception as e:
    print("banners: couldn't read the claims, nothing changed:", e); sys.exit(0)

def slug(n):
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", n.lower())) or "player"

players = sorted({r["player"] for r in rows if r.get("player")})
os.makedirs(out, exist_ok=True)
stamp_path = os.path.join(out, "stamp.json")
try:
    stamp = json.load(open(stamp_path))
except Exception:
    stamp = {}
redraw_all = stamp.get("week") != week or stamp.get("v") != BANNER_VERSION
want = {slug(n): n for n in players}
# players whose claim was removed but who keep their banner (an admin's choice when removing the claim)
try:
    if os.environ.get("BANNER_TEST_PLAYERS"):
        keep_rows = []
    else:
        req = urllib.request.Request(f"{url}/rest/v1/kept_banners?select=player", headers={"apikey": key, "Authorization": f"Bearer {key}"})
        keep_rows = json.load(urllib.request.urlopen(req, timeout=30))
    kept = {slug(r["player"]): r["player"] for r in keep_rows if r.get("player")}
    can_delete = True
except Exception:
    # not set up yet (claim_remove.sql not run): delete nothing, keep every banner that's already there
    kept = {s: n for s, n in (stamp.get("names") or {}).items() if os.path.exists(os.path.join(out, s + ".png"))}
    can_delete = False
names = {**kept, **want}

removed = 0
if can_delete:
    for f in os.listdir(out):
        m = re.fullmatch(r"(.+)\.png", f)
        if m and m.group(1) not in names:
            os.remove(os.path.join(out, f)); removed += 1

todo = [(s, n) for s, n in names.items()
        if redraw_all or not os.path.exists(os.path.join(out, s + ".png"))]
if not todo:
    print(f"banners: {len(names)} up to date" + (f", removed {removed}" if removed else ""))
    if stamp.get("names") != names or removed: json.dump({**stamp, "players": sorted(names), "names": names}, open(stamp_path, "w"))
    sys.exit(0)

chrome = os.environ.get("CHROME") or next((shutil.which(c) for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(c)), None)
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("banners: playwright isn't installed, skipped"); sys.exit(0)

made = 0
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=chrome, args=["--no-sandbox", "--allow-file-access-from-files"]) if chrome else pw.chromium.launch()
    pg = br.new_page(viewport={"width": 900, "height": 400}, device_scale_factor=1)
    pg.goto("file://" + page + "?banner=", wait_until="load")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(500)
    for s, n in todo:
        dest = os.path.join(out, s + ".png")
        ok = pg.evaluate("n=>{const d=document.getElementById('bnshot'); d.innerHTML=bannerHtml(n); bnFit(d); return !!d.firstElementChild}", n)
        if not ok:
            print(f"banners: {n} isn't in the player list"); continue
        pg.evaluate("document.fonts.load('800 22px Oxanium').catch(()=>0).then(()=>document.fonts.ready).then(()=>bnFit(document.getElementById('bnshot')))")
        pg.locator("#bnshot > div").screenshot(path=dest, omit_background=True)
        made += 1
    br.close()

json.dump({"week": week, "v": BANNER_VERSION, "players": sorted(names), "names": names}, open(stamp_path, "w"))
print(f"banners: made {made} images for {len(todo)} players" + (" (new week, redrew all)" if redraw_all else "") + (f", removed {removed}" if removed else ""))
