import json, re, asyncio
from playwright.async_api import async_playwright

CODE = "R47AwfNhdXpgD38c"
PLAYER = "\u0410\u043d\u043f\u0430\u0432\u0430\u043b"
BASE = f"https://www.warcraftlogs.com/reports/{CODE}"

async def grab(page, path):
    url = BASE + path
    await page.goto(url, wait_until="domcontentloaded", timeout=90000)
    await page.wait_for_timeout(8000)
    return await page.title(), await page.content(), await page.inner_text("body")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        results = {}
        for key, path in [
            ("damage_done", "?fight=last&type=damage-done"),
            ("casts", "?fight=last&type=casts"),
            ("timeline", "?fight=last&type=timeline"),
            ("summary", "?fight=last&type=summary"),
        ]:
            try:
                title, html, text = await grab(page, path)
                results[key] = {"title": title, "html_len": len(html), "text_len": len(text)}
                open(rf"e:/wow_guides/wcl_{key}.html", "w", encoding="utf-8", errors="replace").write(html)
                open(rf"e:/wow_guides/wcl_{key}.txt", "w", encoding="utf-8", errors="replace").write(text)
                print(key, title)
            except Exception as e:
                results[key] = {"error": str(e)}
                print(key, "ERR", e)
        await browser.close()
    with open(r"e:/wow_guides/wcl_pages_meta.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

asyncio.run(main())
