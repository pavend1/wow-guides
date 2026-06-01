import json, asyncio, re
from playwright.async_api import async_playwright

CODE = "R47AwfNhdXpgD38c"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

async def load(page, url, wait_sel=None):
    await page.goto(url, wait_until="domcontentloaded", timeout=120000)
    for _ in range(40):
        if "Just a moment" not in await page.title():
            break
        await page.wait_for_timeout(2000)
    if wait_sel:
        try:
            await page.wait_for_selector(wait_sel, timeout=60000)
        except Exception:
            pass
    await page.wait_for_timeout(8000)

async def table_rows(page):
    return await page.evaluate('''() => {
      const out = [];
      for (const tr of document.querySelectorAll('table tbody tr')) {
        const cells = [...tr.querySelectorAll('td')].map(td => td.innerText.trim()).filter(Boolean);
        if (cells.length >= 2) out.push(cells);
      }
      return out;
    }''')

async def main():
    captured = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=UA)
        async def on_response(resp):
            u = resp.url
            if 'warcraftlogs.com' in u and resp.status == 200:
                ct = resp.headers.get('content-type','')
                if 'json' in ct or '/client' in u or 'table' in u:
                    try:
                        body = await resp.text()
                        if len(body) > 100:
                            captured.append({'url': u, 'len': len(body), 'body': body[:200000]})
                    except Exception:
                        pass
        page.on('response', on_response)

        urls = [
            f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type=damage-done&source=3",
            f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type=casts&source=3",
            f"https://www.warcraftlogs.com/reports/{CODE}?fight=last&type=timeline&source=3",
        ]
        results = {}
        for url in urls:
            await load(page, url, 'table tbody tr')
            results[url] = {
                'title': await page.title(),
                'rows': await table_rows(page),
            }
        await browser.close()

    with open(r'e:/wow_guides/wcl_table_extract.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(r'e:/wow_guides/wcl_network_capture2.json', 'w', encoding='utf-8') as f:
        json.dump([{k:v for k,v in c.items() if k!='body'} for c in captured], f, ensure_ascii=False, indent=2)
    for i,c in enumerate(captured):
        open(rf'e:/wow_guides/wcl_net_{i}.json','w',encoding='utf-8').write(c['body'])
    for url, data in results.items():
        print(url.split('type=')[1][:20], 'rows', len(data['rows']), 'title', data['title'][:80])

asyncio.run(main())
