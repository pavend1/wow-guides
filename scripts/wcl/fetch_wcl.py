import cloudscraper, re, json, os
scraper = cloudscraper.create_scraper()
code = "R47AwfNhdXpgD38c"
url = f"https://www.warcraftlogs.com/reports/{code}?fight=last&type=damage-done"
r = scraper.get(url, timeout=90)
print("status", r.status_code, "len", len(r.text))
out_html = r"e:/wow_guides/wcl_report.html"
with open(out_html, "w", encoding="utf-8", errors="replace") as f:
    f.write(r.text)
for pat in ["__NEXT_DATA__", "reportData", "\u0410\u043d\u043f\u0430\u0432\u0430\u043b", "Anpaval", "Just a moment"]:
    print(pat, pat in r.text)
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
if m:
    data = json.loads(m.group(1))
    with open(r"e:/wow_guides/wcl_next_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("next_data bytes", len(m.group(1)))
