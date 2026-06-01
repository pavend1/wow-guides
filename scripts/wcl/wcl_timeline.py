import json, asyncio, re
from playwright.async_api import async_playwright
CODE='R47AwfNhdXpgD38c'; UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0 Safari/537.36'
KEYS=['Void Metamorphosis','Metamorphosis','Soul Immolation','Reap','Void Ray','Consume','Devour','Collapsing Star','Cull','Eradicate']
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=UA, viewport={'width':1920,'height':1080})
        url=f'https://www.warcraftlogs.com/reports/{CODE}?fight=last&type=timeline&source=3'
        await page.goto(url, wait_until='domcontentloaded', timeout=120000)
        for _ in range(50):
            if 'Just a moment' not in await page.title(): break
            await page.wait_for_timeout(2000)
        await page.wait_for_timeout(15000)
        text=await page.inner_text('body')
        await browser.close()
    open(r'e:/wow_guides/wcl_timeline_source3.txt','w',encoding='utf-8').write(text)
    found={k: text.count(k) for k in KEYS}
    print(json.dumps({'cf':'security' in text.lower(), 'err':'Unable to fetch' in text, 'found':found, 'lines':len(text.splitlines())}))
asyncio.run(main())
