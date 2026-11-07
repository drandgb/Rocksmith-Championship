# Stop anything private from being committed to this public repository: secret keys and passwords, and email
# addresses (players' emails stay private). Looks at every file that would be committed (tracked files, plus new ones
# not ignored by .gitignore). Prints the file, line and kind of each find, never the secret itself (logs are public).
#   python3 build/check_secrets.py
# Exit code 0: nothing found. 1: something found (listed).
import base64, json, re, subprocess, sys

# addresses that are fine to have: placeholders and GitHub's no-reply addresses
OK_EMAIL = re.compile(r"@(example\.(com|org|net)|users\.noreply\.github\.com)$", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
KEYS = [
    ("a Supabase secret key", re.compile(r"\bsb_secret_[A-Za-z0-9_-]{10,}")),
    ("a GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{30,}")),
    ("an OpenAI key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}")),
    ("a Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}")),
    ("an AWS key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("a Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("a private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("a database address with its password", re.compile(r"\bpostgres(?:ql)?://[^:/\s\"'@]+:[^@\s\"']+@")),
    # a Gmail app password (four groups of four letters), only next to a word like "password" so ordinary text doesn't trip it
    ("a Gmail app password", re.compile(r"(?i)(?:pass|pwd|smtp)\w*\W{1,6}[\"']?[a-z]{4} ?[a-z]{4} ?[a-z]{4} ?[a-z]{4}[\"']?(?![a-z])")),
]
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.(eyJ[A-Za-z0-9_-]{10,})\.[A-Za-z0-9_-]{10,}")

def jwt_role(part):
    try: return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4))).get("role", "")
    except Exception: return ""

files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "-z"], capture_output=True, check=True).stdout.decode().split("\0")
found = []
for f in filter(None, files):
    try: data = open(f, "rb").read()
    except (FileNotFoundError, IsADirectoryError): continue
    if b"\0" in data[:8000]: continue          # images and other binary files
    for n, line in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
        for kind, rx in KEYS:
            if rx.search(line): found.append(f"{f}:{n}: {kind}")
        for m in JWT.finditer(line):
            if jwt_role(m.group(1)) == "service_role": found.append(f"{f}:{n}: a Supabase service_role key")
        for m in EMAIL.finditer(line):
            e = m.group(0)
            if OK_EMAIL.search(e) or re.search(r"\.(png|jpe?g|gif|svg|webp|js|css)$", e, re.I): continue   # "name@2x.png" isn't an address
            found.append(f"{f}:{n}: an email address ({e[0]}…@{e.split('@')[1]})")

if found:
    print("secrets check: found something that shouldn't be in this public repository:")
    for x in dict.fromkeys(found): print("  - " + x)
    sys.exit(1)
print(f"secrets check: nothing private found ({len([f for f in files if f])} files)")
