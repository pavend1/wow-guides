import re, json, cloudscraper
text = open(r"e:/wow_guides/wcl_report.html", encoding="utf-8", errors="replace").read()
print("len", len(text))
for kw in ["graphql", "reportData", "initialState", "fightID", "fightId", "tableData", "summaryData"]:
    print(kw, text.count(kw))
# find all quoted paths starting with /
paths = set(re.findall(r'"(/(?:api|v1|client)[^"]{3,120})"', text))
for p in sorted(paths)[:50]:
    print("path", p)
# CSRF / tokens
for m in re.finditer(r'name="csrf-token" content="([^"]+)"', text):
    print("csrf", m.group(1)[:20])
# embedded react query keys
for m in re.finditer(r'\\"query\\":\\"(.*?)\\"', text):
    print("escaped query", m.group(1)[:80])
