import json
from pathlib import Path

casts = json.loads(Path(r'e:/wow_guides/wcl_anpaval_tables.json').read_text(encoding='utf-8'))['casts']
# map damage by cast count from html misparsed rows
html_rows = json.loads(Path(r'e:/wow_guides/wcl_dmg_html_rows.json').read_text(encoding='utf-8'))
cast_map = {c['parts'][0]: c['name'] for c in casts if c['parts']}
damage = []
for r in html_rows:
    key = r['name'].replace(',','')
    ability = cast_map.get(key, f"unknown_{key}")
    damage.append({**r, 'ability_guess': ability})
damage.sort(key=lambda x: float(x['amount'].replace('m','').replace('k','')) if 'm' in x['amount'] else float(x['amount'].replace('k',''))/1000, reverse=True)

summary = {
  'report': 'R47AwfNhdXpgD38c',
  'player': '\u0410\u043d\u043f\u0430\u0432\u0430\u043b',
  'source_id': 3,
  'spec': 'Devourer DH',
  'fight': {
    'name': 'Pit of Saron Last Run',
    'key_level': 7,
    'label_duration': '41:11',
    'wcl_active_seconds': 2400,
    'wcl_active_time': '40:00',
  },
  'performance': {
    'dps': 37586.5,
    'damage_total': '90.21m',
    'damage_pct': '23.70%',
    'active_pct': '75.00%',
    'ilvl': 249,
    'parse_percentile': 6,
    'dps_rank_in_party': 3,
    'party_dps_order': [
      {'name':'Orgralin','dps':45445.5},
      {'name':'Culosudao','dps':43479.9},
      {'name':'\u0410\u043d\u043f\u0430\u0432\u0430\u043b','dps':37586.5},
      {'name':'Uholly','dps':23607.1},
      {'name':'Horandriel','dps':8480.4},
    ],
  },
  'casts': casts,
  'damage_by_castcount_map': damage,
  'cooldown_notes': {
    'fight_minutes': 40,
    'reap_casts': 25,
    'reap_theoretical_max_8s_cd': 300,
    'soul_immolation_casts': 27,
    'soul_immolation_theoretical_90s_cd': 27,
    'void_ray_casts': 142,
    'consume_casts': 384,
    'devour_casts': 259,
    'collapsing_star_casts': 50,
    'cull_casts': 35,
  },
}
Path(r'e:/wow_guides/wcl_anpaval_analysis.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print('saved')
