import json, re, asyncio
from playwright.async_api import async_playwright

URL = "https://www.warcraftlogs.com/reports/R47AwfNhdXpgD38c?fight=last&type=damage-done"
PLAYER_NAMES = ["\u0410\u043d\u043f\u0430\u0432\u0430\u043b", "Anpaval"]
captured = []

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0 Safari/537.36")
        page = await context.new_page()

        async def on_response(resp):
            u = resp.url
            if "warcraftlogs.com" not in u:
                return
            if not any(x in u for x in ["/api/v2/client", "graphql", "table", "summary", "events"]):
                return
            try:
                ctype = resp.headers.get("content-type", "")
                if "json" not in ctype and "/client" not in u:
                    return
                body = await resp.text()
                if len(body) < 20:
                    return
                captured.append({"url": u, "status": resp.status, "body": body})
            except Exception:
                pass

        page.on("response", on_response)
        await page.goto(URL, wait_until="networkidle", timeout=120000)
        await page.wait_for_timeout(5000)
        html = await page.content()
        title = await page.title()
        print("title", title)
        print("html_len", len(html))
        for name in PLAYER_NAMES:
            print("player_in_html", name, name in html)
        text = await page.inner_text("body")
        for name in PLAYER_NAMES:
            print("player_in_body", name, name in text)
        # try open casts tab
        try:
            casts_link = page.get_by_role("link", name=re.compile("Casts", re.I))
            if await casts_link.count() > 0:
                await casts_link.first.click()
                await page.wait_for_timeout(4000)
        except Exception as e:
            print("casts nav err", e)
        await browser.close()

    print("captured", len(captured))
    out = {"title": title, "captured": captured}
    with open(r"e:/wow_guides/wcl_playwright_capture.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    # also save trimmed bodies separately for analysis
    summaries = []
    for i, c in enumerate(captured):
        b = c["body"]
        summaries.append({"i": i, "url": c["url"], "status": c["status"], "len": len(b), "snippet": b[:300]})
        if len(b) < 5_000_000:
            with open(rf"e:/wow_guides/wcl_resp_{i}.json", "w", encoding="utf-8") as f:
                f.write(b)
    with open(r"e:/wow_guides/wcl_capture_index.json", "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    for s in summaries:
        print(s["i"], s["status"], s["len"], s["url"][:100])

asyncio.run(main())
