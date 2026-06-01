import re, json, asyncio
from playwright.async_api import async_playwright

CODE = "R47AwfNhdXpgD38c"
PLAYER = "\u0410\u043d\u043f\u0430\u0432\u0430\u043b"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=UA)
        page = await context.new_page()
        await page.goto(f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type=damage-done&source=3", wait_until="domcontentloaded", timeout=120000)
        for _ in range(40):
            if "Just a moment" not in await page.title():
                break
            await page.wait_for_timeout(2000)
        await page.wait_for_timeout(12000)
        title = await page.title()
        text = await page.inner_text("body")
        html = await page.content()
        open(r"e:/wow_guides/wcl_player_damage_abilities.txt", "w", encoding="utf-8").write(text)
        open(r"e:/wow_guides/wcl_player_damage_abilities.html", "w", encoding="utf-8", errors="replace").write(html)
        print("title", title, "len", len(text))

        # casts tab - click by link text
        await page.goto(f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type=casts&source=3", wait_until="domcontentloaded", timeout=120000)
        await page.wait_for_timeout(12000)
        casts_text = await page.inner_text("body")
        open(r"e:/wow_guides/wcl_player_casts_source3.txt", "w", encoding="utf-8").write(casts_text)
        print("casts cloudflare", "Just a moment" in casts_text or "security verification" in casts_text.lower())

        # cooldowns / timeline
        await page.goto(f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type=timeline&source=3", wait_until="domcontentloaded", timeout=120000)
        await page.wait_for_timeout(12000)
        tl = await page.inner_text("body")
        open(r"e:/wow_guides/wcl_player_timeline_source3.txt", "w", encoding="utf-8").write(tl)
        print("timeline cloudflare", "security verification" in tl.lower())

        await browser.close()

asyncio.run(main())
