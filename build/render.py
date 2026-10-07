# Fill the page template with the built data and write ../index.html
import json, datetime, os
d = datetime.date.fromisoformat(os.environ["BUILD_DATE"]) if os.environ.get("BUILD_DATE") else datetime.date.today()
sb = json.load(open("scores.json"))
t = open("template.html").read()
for key, f in [("__WEEKS__", "weeks.json"), ("__PLAYERS__", "players.json"), ("__PARTS__", "parts.json"),
               ("__SCORES__", "scores.json"), ("__WINS__", "wins.json"), ("__SONGS_OLD__", "songs_old.json"), ("__RANKINGS__", "rankings.json")]:
    assert key in t, key
    t = t.replace(key, open(f).read())
t = (t.replace("__BUILT__", f"{d:%B} {d.day}, {d.year}")
      .replace("__BUILT_ISO__", datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
      .replace("__DATAWEEK__", open("data_week.txt").read().strip())
      .replace("__SBMAX__", str(max(map(int, sb["weeks"])))))
out = os.environ.get("OUT", "../../index.html")
open(out, "w").write(t)
print("wrote", out, f"({len(t)//1024} KB)")
