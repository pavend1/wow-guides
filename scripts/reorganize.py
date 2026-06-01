"""One-time layout: move root clutter into guides/, data/, scripts/, archive/."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIRS = {
    "guides/mplus": [],
    "guides/rotation": [],
    "data/wowhead": [],
    "scripts/wowhead": [],
    "scripts/wcl": [],
    "archive/scratch": [],
}

GUIDES_MPLUS = {"prot-paladin-mplus-ru.md", "guardian-druid-mplus-ru.md"}
GUIDES_ROTATION = {"devourer-dh-rotation-ru.md"}
WOWHEAD_SCRIPTS = {"fetch_wowhead_ru.py", "fetch_guardian_ru.py", "fetch_dungeons_ru.py"}
WOWHEAD_DATA = {
    "mplus_dungeons_ru.json",
    "guardian_ru_names.json",
    "dungeon_zones_ru.json",
    "wowhead_ru_names.json",
    "wowhead_batch.txt",
}

WCL_PREFIXES = (
    "wcl_",
    "parse_",
    "fetch_wcl",
    "probe_wcl",
    "dump_",
    "extract_",
    "search_",
    "find_",
    "build_analysis",
)


def dest_for(name: str) -> Path | None:
    if name in GUIDES_MPLUS:
        return ROOT / "guides" / "mplus" / name
    if name in GUIDES_ROTATION:
        return ROOT / "guides" / "rotation" / name
    if name in WOWHEAD_SCRIPTS:
        return ROOT / "scripts" / "wowhead" / name
    if name in WOWHEAD_DATA:
        return ROOT / "data" / "wowhead" / name
    if any(name.startswith(p) for p in WCL_PREFIXES):
        return ROOT / "scripts" / "wcl" / name
    p = Path(name)
    if p.suffix in {".txt", ".json", ".html", ".js"} and name != "README.md":
        return ROOT / "archive" / "scratch" / name
    return None


def main() -> None:
    for rel in DIRS:
        (ROOT / rel).mkdir(parents=True, exist_ok=True)

    moved = []
    for src in list(ROOT.iterdir()):
        if not src.is_file():
            continue
        dst = dest_for(src.name)
        if dst is None:
            continue
        if dst.exists():
            continue
        shutil.move(str(src), str(dst))
        moved.append(f"{src.name} -> {dst.relative_to(ROOT)}")

    print(f"Moved {len(moved)} files")
    for line in moved[:30]:
        print(" ", line)
    if len(moved) > 30:
        print(f"  ... and {len(moved) - 30} more")


if __name__ == "__main__":
    main()
