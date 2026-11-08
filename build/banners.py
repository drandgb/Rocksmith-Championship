# Forum signature banners for players with an approved profile claim.
#   python3 build/banners.py [index.html] [cards dir]
# Reads the approved claims from the site's database (the same public read the site itself does), then screenshots
# each player's banner from the built page in headless Chrome (bannerHtml() in the page, opened with ?banner=) into
# cards/<slug>.png (700x150).
#   - every banner is redrawn when a new week's results arrive (or when BANNER_VERSION changes, or an admin presses
#     Redraw all banners on the site: a row in banner_redraw, banner_redraw.sql)
#   - otherwise only newly approved players get one, so this is cheap to run every few minutes
#   - when a claim is removed, the admin chooses whether the banner stays (and keeps updating) or is deleted
# Each banner also gets a share page, cards/<slug>.html: a link that shows the banner as its preview in Discord,
# Reddit and other apps, and opens the player's lookup on the site. The site's own link preview picture,
# cards/og/site.png (1200x630), is drawn with the banners each week (ogCardHtml() in the page).
# If the claims can't be read, nothing is changed.
import html as htmlmod, json, os, re, shutil, sys, urllib.parse, urllib.request

BANNER_VERSION = 56  # bump to redraw every banner after a design change

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
# an admin asked for every banner to be redrawn (Admin → Player banners → Redraw all banners)
redraw_at = stamp.get("req")
try:
    if not os.environ.get("BANNER_TEST_PLAYERS"):
        q = urllib.request.Request(f"{url}/rest/v1/banner_redraw?select=at&order=at.desc&limit=1",
                                   headers={"apikey": key, "Authorization": f"Bearer {key}"})
        r = json.load(urllib.request.urlopen(q, timeout=30))
        if r: redraw_at = r[0]["at"]
except Exception:
    pass  # not set up yet
redraw_all = stamp.get("week") != week or stamp.get("v") != BANNER_VERSION or redraw_at != stamp.get("req")
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
        m = re.fullmatch(r"(.+)\.(?:png|html)", f)
        if m and m.group(1) not in names:
            os.remove(os.path.join(out, f)); removed += 1

# share pages (rewritten only when they change: the week in the picture's link makes apps fetch the new banner)
SITE = "https://drandgb.github.io/Rocksmith-Championship/"
def share_page(s, n):
    e, img, go = htmlmod.escape(n), f"{SITE}cards/{s}.png?w={week}", "../#players/" + urllib.parse.quote(n, safe="")
    title = f"{e} · Rocksmith 2014 Championship"
    return f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>{title}</title>
<meta property="og:title" content="{title}">
<meta property="og:description" content="{e}'s weekly Rocksmith 2014 challenge stats: weeks played, wins, levels and medals.">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Rocksmith 2014 Championship">
<meta property="og:url" content="{SITE}cards/{s}.html">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="700">
<meta property="og:image:height" content="150">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d0f14">
<meta http-equiv="refresh" content="0; url={htmlmod.escape(go)}">
<script>location.replace({json.dumps(go)})</script>
<a href="{htmlmod.escape(go)}">{e} on the Rocksmith 2014 Championship site</a>
"""
for s, n in names.items():
    f, txt = os.path.join(out, s + ".html"), share_page(s, n)
    if not os.path.exists(f) or open(f, encoding="utf-8").read() != txt:
        open(f, "w", encoding="utf-8").write(txt)
site_png = os.path.join(out, "og", "site.png")
need_site = redraw_all or not os.path.exists(site_png)

todo = [(s, n) for s, n in names.items()
        if redraw_all or not os.path.exists(os.path.join(out, s + ".png"))]
if not todo and not need_site:
    print(f"banners: {len(names)} up to date" + (f", removed {removed}" if removed else ""))
    if stamp.get("names") != names or removed or redraw_at != stamp.get("req"): json.dump({**stamp, "players": sorted(names), "names": names, "req": redraw_at}, open(stamp_path, "w"))
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
    if need_site:  # the site's link preview picture
        os.makedirs(os.path.dirname(site_png), exist_ok=True)
        pg.set_viewport_size({"width": 1200, "height": 630})
        if pg.evaluate("()=>{if(typeof ogCardHtml!=='function')return false; const d=document.getElementById('bnshot'); d.innerHTML=ogCardHtml(); return !!d.firstElementChild}"):
            pg.evaluate("document.fonts.ready")
            # the title is one line: make it smaller if the site's font draws it wider than the picture
            pg.evaluate("()=>{const t=document.querySelector('#bnshot .og-t'); let s=64; while(t&&t.scrollWidth>1130&&s>40){s-=2; t.style.fontSize=s+'px'}}")
            pg.locator("#bnshot > div").screenshot(path=site_png)
            print("banners: drew the site's link preview picture")
    br.close()

json.dump({"week": week, "v": BANNER_VERSION, "players": sorted(names), "names": names, "req": redraw_at}, open(stamp_path, "w"))
print(f"banners: made {made} images for {len(todo)} players" + (" (redrew all)" if redraw_all else "") + (f", removed {removed}" if removed else ""))
