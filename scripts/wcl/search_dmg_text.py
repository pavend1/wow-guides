from pathlib import Path
text=Path(r'e:/wow_guides/wcl_dmg_source3.txt').read_text(encoding='utf-8')
for name in ['Void Ray','Collapsing Star','Soul Immolation','Eradicate','Void Metamorphosis','Immolation','Hunger','Vortex','Devour','Consume','Reap','Cull','Catastrophe','Total']:
    idx=text.find(name)
    print(name, idx)
    if idx>=0:
        print(text[idx:idx+250].replace('\n',' | '))
