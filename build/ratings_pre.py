# Website ratings for drandTools' "Update ratings from website": every recent challenge's rating as shown on the site
# (players' ratings and hosts' ratings, see songRating() in the page), worked out in headless Chrome from the page just
# built and saved as ratings.json next to index.html.
#   python3 ratings_pre.py <index.html>
# The ratings are read from the site's database (the same public read the site itself does) and given to the page,
# so Chrome needs no network. If anything fails, the previous ratings.json is kept.
import json, os, re, shutil, subprocess, sys, tempfile, urllib.request

page = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../../index.html")
out = os.path.join(os.path.dirname(page), "ratings.json")
html = open(page, encoding="utf-8").read()
grab = lambda pat: (re.search(pat, html) or [None, None])[1]
url, key = grab(r'SUPA_URL="([^"]+)"'), grab(r'SUPA_KEY="([^"]+)"')
chrome = os.environ.get("CHROME") or next((shutil.which(c) for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(c)), None)
if not url or not key or not chrome:
    print("ratings: no database settings or no Chrome, skipped"); sys.exit(0)
try:
    votes, start = [], 0
    if os.environ.get("RATINGS_TEST_VOTES"):   # local testing without the database: a JSON file of rating rows
        votes = json.load(open(os.environ["RATINGS_TEST_VOTES"])); raise StopIteration
    while True:   # the database returns at most 1000 rows at a time
        req = urllib.request.Request(f"{url}/rest/v1/votes?select=*", headers={"apikey": key, "Authorization": f"Bearer {key}", "Range": f"{start}-{start+999}"})
        part = json.load(urllib.request.urlopen(req, timeout=60)); votes += part
        if len(part) < 1000: break
        start += 1000
except StopIteration:
    pass
except Exception as e:
    print("ratings: couldn't read the ratings, kept the previous file:", e); sys.exit(0)
tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=os.path.dirname(page), encoding="utf-8")
tmp.write(html.replace("<script>", "<script>window.__VOTES=" + json.dumps(votes).replace("<", "\\u003c") + ";</script><script>", 1)); tmp.close()   # before the page's first script
try:
    dom = subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                          "--virtual-time-budget=120000", "--dump-dom", "file://" + tmp.name + "?rateout"],
                         capture_output=True, text=True, timeout=300).stdout
finally:
    os.unlink(tmp.name)
m = re.search(r'<script type="application/json" id="rateout">(.*?)</script>', dom, re.S)
if not m:
    print("ratings: no results from the page, kept the previous file"); sys.exit(0)
data = json.loads(m.group(1))
json.dump(data, open(out, "w"), separators=(",", ":"))
print(f"ratings: {len(votes)} ratings read, {sum(len(v) for v in data['weeks'].values())} challenges in {len(data['weeks'])} weeks")
