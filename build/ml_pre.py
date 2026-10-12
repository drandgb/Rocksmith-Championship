# Medal leaders for the Winners, Players and Hosts pages, worked out once per build instead of in every visitor's
# browser: open the freshly built page in headless Chrome with ?mlpre (the page counts every medal and writes the
# results into itself), read them back and save ml_pre.json for render.py to build into the page.
# Skipped quietly if no Chrome is available: the page then counts the medals itself when the pages are opened.
import json, os, re, shutil, subprocess, sys

page = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../../index.html")
chrome = os.environ.get("CHROME") or next((shutil.which(c) for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(c)), None)
if not chrome:
    print("medal leaders: no Chrome found, skipped (the page will count them itself)"); sys.exit(0)
try:
    dom = subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                          "--virtual-time-budget=300000", "--dump-dom", "file://" + page + "?mlpre"],
                         capture_output=True, text=True, timeout=600).stdout
except Exception as e:
    print("medal leaders: Chrome failed, skipped:", e); sys.exit(0)
m = re.search(r'<script type="application/json" id="mlpre-out">(.*?)</script>', dom, re.S)
if not m:
    print("medal leaders: no results in the page, skipped"); sys.exit(0)
data = json.loads(m.group(1))
json.dump(data, open("ml_pre.json", "w"), separators=(",", ":"))
print("medal leaders:", {k: len(v) for k, v in data.items()}, f"{os.path.getsize('ml_pre.json')//1024} KB")
