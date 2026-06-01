import json, asyncio, re
from playwright.async_api import async_playwright

CODE = "R47AwfNhdXpgD38c"
PLAYER = "\u0410\u043d\u043f\u0430\u0432\u0430\u043b"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

async def wait_cf(page):
    for _ in range(40):
        if "Just a moment" not in await page.title():
            return
        await page.wait_for_timeout(2000)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=UA, viewport={"width": 1920, "height": 1080})
        base = f"https://www.warcraftlogs.com/reports/{CODE}?fight=last"
        await page.goto(base + "&type=damage-done", wait_until="domcontentloaded", timeout=120000)
        await wait_cf(page)
        await page.wait_for_timeout(12000)
        # click player in summary table
        cell = page.get_by_role("link", name=PLAYER)
        if await cell.count() == 0:
            cell = page.get_by_text(PLAYER, exact=True)
        await cell.first.click()
        await page.wait_for_timeout(8000)
        dmg_text = await page.inner_text("body")
        # switch to casts via query param on same session
        await page.goto(base + "&type=casts&source=3", wait_until="domcontentloaded", timeout=120000)
        await wait_cf(page)
        await page.wait_for_timeout(15000)
        casts_text = await page.inner_text("body")
        await browser.close()
    open(r"e:/wow_guides/wcl_after_click_dmg.txt", "w", encoding="utf-8").write(dmg_text)
    open(r"e:/wow_guides/wcl_casts_source3_session.txt", "w", encoding="utf-8").write(casts_text)
    meta = {
        "dmg_has_error": "Unable to fetch data" in dmg_text,
        "casts_has_error": "Unable to fetch data" in casts_text,
        "casts_cf": "Just a moment" in casts_text or "security verification" in casts_text.lower(),
        "dmg_has_consume": "Consume" in dmg_text,
        "casts_has_consume": "Consume" in casts_text,
        "casts_lines": len(casts_text.splitlines()),
    }
    Path = __import__('pathlib').Path
    Path(r"e:/wow_guides/wcl_session_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(meta, ensure_ascii=False))

asyncio.run(main())
