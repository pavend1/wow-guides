"""Compare guide link text with Wowhead RU tooltip names."""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

LOCALE = 7
ROOT = Path(__file__).resolve().parents[2]
GUIDES = [
    ROOT / "guides" / "mplus" / "prot-paladin-mplus-ru.md",
    ROOT / "guides" / "mplus" / "guardian-druid-mplus-ru.md",
    ROOT / "guides" / "mplus" / "brewmaster-monk-mplus-ru.md",
    ROOT / "guides" / "mplus" / "subtlety-rogue-mplus-ru.md",
    ROOT / "guides" / "rotation" / "devourer-dh-rotation-ru.md",
]

LINK_RE = re.compile(
    r"\[([^\]]+)\]\(https://www\.wowhead\.com/ru/(spell|item|zone|item-set)=(\d+)",
    re.UNICODE,
)


def fetch_name(kind: str, iid: int) -> str:
    url = f"https://nether.wowhead.com/tooltip/{kind}/{iid}?locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8"))
    return (data.get("name") or "").strip()


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def main() -> None:
    mismatches = []
    checked = set()
    for path in GUIDES:
        if not path.exists():
            print(f"SKIP missing {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for label, kind, iid_s in LINK_RE.findall(text):
            key = (kind, int(iid_s))
            if key in checked:
                continue
            checked.add(key)
            try:
                api_name = fetch_name(kind, int(iid_s))
            except Exception as e:
                mismatches.append(
                    {
                        "file": str(path.relative_to(ROOT)),
                        "kind": kind,
                        "id": int(iid_s),
                        "label": label,
                        "api": f"ERR: {e}",
                        "match": False,
                    }
                )
                continue
            # label in link may be partial; flag if clearly different
            if norm(label) != norm(api_name) and norm(api_name) not in norm(label) and norm(label) not in norm(api_name):
                mismatches.append(
                    {
                        "file": str(path.relative_to(ROOT)),
                        "kind": kind,
                        "id": int(iid_s),
                        "label": label,
                        "api": api_name,
                        "match": False,
                    }
                )

    out = ROOT / "data" / "wowhead" / "verify_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(mismatches, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Checked {len(checked)} links, mismatches: {len(mismatches)}")
    for m in mismatches[:40]:
        print(f"  {m['kind']}:{m['id']} guide={m['label']!r} api={m['api']!r} ({m['file']})")


if __name__ == "__main__":
    main()
