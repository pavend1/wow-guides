import json, re, asyncio
from playwright.async_api import async_playwright

URL = "https://www.warcraftlogs.com/reports/R47AwfNhdXpgD38c?fight=last&type=damage-done"
PLAYER = "\u0410\u043d\u043f\u0430\u0432\u0430\u043b"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, wait_until="networkidle", timeout=120000)
        await page.wait_for_timeout(3000)
        title = await page.title()
        # extract summary table rows via DOM
        data = await page.evaluate('''() => {
          const out = {rows: [], headers: []};
          const tables = [...document.querySelectorAll('table')];
          for (const t of tables) {
            const headers = [...t.querySelectorAll('thead th')].map(th => th.innerText.trim());
            const rows = [...t.querySelectorAll('tbody tr')].map(tr => [...tr.querySelectorAll('td')].map(td => td.innerText.trim()));
            if (rows.length >= 3) out.tables = out.tables || [];
            if (rows.length >= 3) (out.tables||[]).push({headers, rows: rows.slice(0,30)});
          }
          // damage table often in specific container
          const dmg = document.querySelector('#table-container, .report-table, [class*="Damage"]');
          return {title: document.title, tables: out.tables || [], textSample: document.body.innerText.slice(0,5000)};
        }''')
        # click player row if link exists
        try:
            loc = page.get_by_text(PLAYER, exact=True)
            if await loc.count():
                await loc.first.click()
                await page.wait_for_timeout(2500)
        except Exception as e:
            print('click err', e)
        # damage breakdown page for player
        url2 = "https://www.warcraftlogs.com/reports/R47AwfNhdXpgD38c?fight=last&type=damage-done&source=" + PLAYER
        # instead navigate via query - need source id; parse from links
        links = await page.evaluate('''(player) => {
          return [...document.querySelectorAll('a')].filter(a => a.textContent.includes(player)).map(a => ({text:a.textContent.trim(), href:a.getAttribute('href')}));
        }''', PLAYER)
        html = await page.content()
        await browser.close()
    open(r'e:/wow_guides/wcl_playwright_page.html','w',encoding='utf-8',errors='replace').write(html)
    with open(r'e:/wow_guides/wcl_dom_extract.json','w',encoding='utf-8') as f:
        json.dump({"title": title, "links": links, "data": data}, f, ensure_ascii=False, indent=2)
    print('title', title)
    print('links', links[:5])
    print('tables', len(data.get('tables') or []))
    for i,t in enumerate(data.get('tables') or []):
        print('table', i, 'headers', t.get('headers'), 'rows', len(t.get('rows',[])))

asyncio.run(main())
