from pathlib import Path
html = Path(r'e:/wow_guides/wcl_full_page.html').read_text(encoding='utf-8', errors='replace')
chunk = html[795000:805000]
Path(r'e:/wow_guides/wcl_html_chunk_stats.html').write_text(chunk, encoding='utf-8')
# also around consume id
for pos in [620910, 647369, 658635]:
    Path(rf'e:/wow_guides/wcl_html_chunk_{pos}.html').write_text(html[pos-500:pos+1500], encoding='utf-8')
print('written')
