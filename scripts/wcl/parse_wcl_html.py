import re, json
from html import unescape
text = open(r"e:/wow_guides/wcl_report.html", encoding="utf-8", errors="replace").read()
print("title:", re.search(r"<title>(.*?)</title>", text, re.I|re.S).group(1)[:200] if re.search(r"<title>", text, re.I) else "none")
# find script json blobs
patterns = [
    r"window\.report\s*=\s*(\{.*?\});",
    r"var reportData\s*=\s*(\{.*?\});",
    r'"report"\s*:\s*(\{.*?\})\s*,\s*"',
]
for p in patterns:
    m = re.search(p, text, re.S)
    print("pattern", p[:40], "->", bool(m))
# search player
for s in ["Anpaval", "\u0410\u043d\u043f\u0430\u0432\u0430\u043b", "R47AwfNhdXpgD38c", "fight", "damage-done"]:
    idx = text.find(s)
    print("find", repr(s), idx)
# all application/json scripts
for m in re.finditer(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', text, re.S|re.I):
    blob = m.group(1).strip()
    print("json script len", len(blob), blob[:80])
# large script tags with fight
for m in re.finditer(r"<script[^>]*>(.*?)</script>", text, re.S|re.I):
    b = m.group(1)
    if len(b) > 5000 and ("fight" in b.lower() or "report" in b.lower()):
        print("big script", len(b), b[:120].replace("\n"," "))
        open(r"e:/wow_guides/wcl_big_script.js","w",encoding="utf-8").write(b[:200000])
        break
