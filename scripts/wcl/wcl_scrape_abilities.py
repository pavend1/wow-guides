import json, asyncio, re
from playwright.async_api import async_playwright

CODE = "R47AwfNhdXpgD38c"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
ABILITIES = [
    ("473662", "Consume"),
    ("1225823", "Reap"),
    ("473728", "Void Ray (group)"),
    ("1214595", "Void Ray (Void Metamorphosis)"),
    ("1217610", "Devour"),
    ("1245455", "Cull"),
    ("1226033", "Eradicate (group)"),
    ("1225827", "Eradicate (Reap)"),
    ("1279200", "Eradicate (Cull)"),
    ("1", "Melee"),
]

async def wait_cf(page):
    for _ in range(45):
        t = await page.title()
        if "Just a moment" not in t:
            return t
        await page.wait_for_timeout(2000)
    return await page.title()

async def scrape_table_text(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # find rows with tab-separated numbers typical of WCL: amount, casts, hits
    rows = []
    for i,l in enumerate(lines):
        if re.search(r'\d+\.\d+m|\d+\.\d+k', l, re.I) and '%' in l:
            rows.append(l)
        if l in ('Total','Casts','Hits','Avg Cast','DPS') and i+1 < len(lines):
            rows.append(l + ' => ' + lines[i+1])
    return rows[:30]

async def main():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=UA, viewport={"width": 1920, "height": 1080})
        # warm up session on full damage page
        await page.goto(f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type=damage-done", wait_until="domcontentloaded", timeout=120000)
        await wait_cf(page)
        await page.wait_for_timeout(10000)
        for aid, name in ABILITIES:
            for typ in ("damage-done", "casts"):
                url = f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type={typ}&source=3&ability={aid}"
                await page.goto(url, wait_until="domcontentloaded", timeout=120000)
                title = await wait_cf(page)
                await page.wait_for_timeout(6000)
                text = await page.inner_text("body")
                key = f"{name}|{typ}"
                results[key] = {
                    "url": url,
                    "title": title,
                    "error": ("Unable to fetch data" in text) or ("Unable to generate" in text),
                    "cloudflare": "security verification" in text.lower(),
                    "sample_rows": await scrape_table_text(text),
                    "text_tail": text.splitlines()[-25:],
                }
                print(key, 'err' if results[key]['error'] else 'ok', 'rows', len(results[key]['sample_rows']))
        await browser.close()
    with open(r"e:/wow_guides/wcl_ability_scrape.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

asyncio.run(main())
