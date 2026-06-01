from pathlib import Path
import re, json
text = Path(r'e:/wow_guides/wcl_player_damage_abilities.txt').read_text(encoding='utf-8')
# find section after player name in title context
lines = [l.rstrip() for l in text.splitlines()]
# abilities often listed as Name then % then amount
rows = []
i = 0
while i < len(lines):
    l = lines[i].strip()
    if i+2 < len(lines):
        l1 = lines[i+1].strip()
        l2 = lines[i+2].strip()
        if re.match(r'^\d+\.\d+%$', l1) and (re.match(r'^\d+\.\d+m$', l2) or re.match(r'^\d+\.\d+k$', l2) or re.match(r'^\d+$', l2)):
            if len(l) > 2 and l not in ('Total','Name','Amount'):
                rows.append({"ability": l, "pct": l1, "amount": l2})
            i += 3
            continue
    i += 1
# filter devourer abilities
interesting = [r for r in rows if any(x in r['ability'].lower() for x in ['consume','reap','void','meta','ray','devour','cull','erad','soul','chaos','blade','immolation','fel','hunger','vortex','eye','sigil'])]
out = {"all_count": len(rows), "top20": rows[:20], "interesting": interesting, "last30": rows[-30:]}
Path(r'e:/wow_guides/wcl_parsed_abilities.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(out, ensure_ascii=True, indent=2)[:8000])
