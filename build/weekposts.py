# Each week's forum post, as generated on the NewWeekPost sheet (Song Selection List), saved at every site update so it
# can still be updated with new ratings after NewWeekPost has moved on to the next week (drandTools' "Week post with
# updated ratings" reads weekposts.json). Keeps the newest 12 weeks; a week's post is replaced if it's regenerated.
#   python3 weekposts.py <index.html>      writes weekposts.json next to the page, and cache/weekposts.json
import csv, io, json, os, re, sys, urllib.request, datetime
SSL_ID = os.environ.get("SSL_ID", "1HzgY90kLwyGqzJ-R64v8lmpeQMMhhxwGwUlenepIgms")
url = f"https://docs.google.com/spreadsheets/d/{SSL_ID}/gviz/tq?tqx=out:csv&headers=0&sheet=NewWeekPost"
page = sys.argv[1] if len(sys.argv) > 1 else "../../index.html"
cached = "cache/weekposts.json"
posts = json.load(open(cached)) if os.path.exists(cached) else {}
try:
    if os.environ.get("WEEKPOSTS_TEST_FILE"): text = open(os.environ["WEEKPOSTS_TEST_FILE"], encoding="utf-8").read()
    else: text = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
    if text.lstrip().startswith("<"): raise ValueError("not shared (got a sign-in page)")
    post = next((c for r in csv.reader(io.StringIO(text)) for c in r if "Welcome to the CF" in c and "This week's songs are:" in c), None)
    m = post and re.search(r"-= Week (\d+) =-", post)
    if not m: raise ValueError("no week post on the NewWeekPost sheet")
    w = m.group(1); now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes")
    if w not in posts: posts[w] = {"post": post, "saved": now}; print(f"weekposts: saved week {w}'s post")
    elif posts[w]["post"] != post: posts[w] = {"post": post, "saved": now}; print(f"weekposts: week {w}'s post changed, saved again")
    else: print(f"weekposts: week {w}'s post already saved")
except Exception as e:
    print("weekposts: couldn't read NewWeekPost, kept the saved posts:", e)
posts = {w: posts[w] for w in sorted(posts, key=int)[-12:]}
json.dump(posts, open(cached, "w"))
out = os.path.join(os.path.dirname(os.path.abspath(page)), "weekposts.json")
new = json.dumps({"made": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes"), "weeks": posts})
old = open(out).read() if os.path.exists(out) else ""
# only rewrite the file when a post changed, so an update with nothing new commits nothing
if not old or json.loads(old).get("weeks") != posts: open(out, "w").write(new)
