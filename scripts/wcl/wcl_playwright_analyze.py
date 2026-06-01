import json, re, asyncio
from playwright.async_api import async_playwright

CODE = "R47AwfNhdXpgD38c"
PLAYER = "\u0410\u043d\u043f\u0430\u0432\u0430\u043b"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

async def main():
    gql = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=UA, locale="en-US")
        page = await context.new_page()

        async def on_response(resp):
            if resp.request.method == "POST" and "/api/v2/client" in resp.url:
                try:
                    gql.append({"status": resp.status, "body": await resp.text()})
                except Exception:
                    pass
        page.on("response", on_response)

        await page.goto(f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type=damage-done", wait_until="domcontentloaded", timeout=120000)
        for _ in range(30):
            t = await page.title()
            if "Just a moment" not in t:
                break
            await page.wait_for_timeout(2000)
        await page.wait_for_timeout(10000)
        title = await page.title()
        text = await page.inner_text("body")
        html = await page.content()
        open(r"e:/wow_guides/wcl_full_page.html", "w", encoding="utf-8", errors="replace").write(html)
        open(r"e:/wow_guides/wcl_full_page.txt", "w", encoding="utf-8", errors="replace").write(text)

        # parse player line from damage table text blocks
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        player_lines = [ln for ln in lines if PLAYER in ln]
        # fight duration from header area
        fight_line = next((ln for ln in lines if "Pit of" in ln or "Last Run" in ln or "Duration" in ln), None)

        source_id = None
        m = re.search(rf'source=(\d+)[^>]*>{re.escape(PLAYER)}', html)
        if not m:
            m = re.search(rf'/reports/{CODE}\?[^"\']*source=(\d+)[^"\']*[^>]*>\s*{re.escape(PLAYER)}', html)
        if not m:
            # href with player
            for hit in re.finditer(rf'href="([^"]*source=(\d+)[^"]*)"[^>]*>\s*{re.escape(PLAYER)}', html):
                source_id = hit.group(2)
                break
        else:
            source_id = m.group(1)

        pages = {"damage_done": text}
        if source_id:
            for typ, q in [("casts", "casts"), ("damage_taken", "damage-taken"), ("timeline", "timeline")]:
                url = f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type={q}&source={source_id}"
                await page.goto(url, wait_until="domcontentloaded", timeout=120000)
                await page.wait_for_timeout(8000)
                pages[typ] = await page.inner_text("body")

        await browser.close()

    with open(r"e:/wow_guides/wcl_gql_responses.json", "w", encoding="utf-8") as f:
        json.dump(gql, f, ensure_ascii=False)
    meta = {
        "title": title,
        "source_id": source_id,
        "player_lines": player_lines[:20],
        "gql_count": len(gql),
        "html_len": len(html),
    }
    with open(r"e:/wow_guides/wcl_analysis_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    for k,v in pages.items():
        open(rf"e:/wow_guides/wcl_player_{k}.txt", "w", encoding="utf-8", errors="replace").write(v)
    print(json.dumps(meta, ensure_ascii=False, indent=2))

asyncio.run(main())
