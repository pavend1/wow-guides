from pathlib import Path
lines = Path(r'e:/wow_guides/wcl_full_page.txt').read_text(encoding='utf-8', errors='replace').splitlines()
for i in range(3450, 3520):
    if i < len(lines):
        print(f'{i}: {lines[i][:120]}')
print('---')
for i in range(4720, 4860):
    if i < len(lines):
        print(f'{i}: {lines[i][:160]}')
