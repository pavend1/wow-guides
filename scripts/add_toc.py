"""Insert ## Оглавление into guide markdown files (GitHub-style anchors)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = list((ROOT / "guides").rglob("*-ru.md"))

EMOJI_RE = re.compile(r"[\U00002600-\U000027BF\U0001F300-\U0001FAFF⚠️✅❌]")


def slugify(title: str) -> str:
    t = EMOJI_RE.sub("", title)
    t = t.strip().lower()
    t = re.sub(r"[«»\"'?!.,:;()\[\]—–/\\+*→]", " ", t)
    t = re.sub(r"\s+", "-", t.strip())
    t = re.sub(r"-+", "-", t)
    return t


def parse_headings(text: str) -> list[tuple[int, str, str]]:
    out: list[tuple[int, str, str]] = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.+)$", line)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        if level == 3 and title.startswith("Шаг "):
            continue
        out.append((level, title, slugify(title)))
    return out


def build_toc(headings: list[tuple[int, str, str]]) -> str:
    lines = ["## Оглавление", ""]
    first_h1 = True
    seen: dict[str, int] = {}
    for level, title, anchor in headings:
        if level == 1:
            if first_h1:
                first_h1 = False
                continue
            lines.append("")
            lines.append(f"**[{title}](#{anchor})**")
            continue
        count = seen.get(anchor, 0)
        seen[anchor] = count + 1
        link = anchor if count == 0 else f"{anchor}-{count}"
        if level == 2:
            lines.append(f"- [{title}](#{link})")
        else:
            lines.append(f"  - [{title}](#{link})")
    lines.append("")
    return "\n".join(lines)


def find_insert_line(lines: list[str]) -> int:
    """Line index to insert TOC (after title + metadata block)."""
    i = 0
    if i < len(lines) and lines[i].startswith("# "):
        i += 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    while i < len(lines) and lines[i].startswith(">"):
        i += 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    return i


def insert_toc(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "## Оглавление" in text:
        print("skip (exists)", path.relative_to(ROOT))
        return
    lines = text.splitlines()
    idx = find_insert_line(lines)
    toc = build_toc(parse_headings(text))
    block = [""] + toc.splitlines() + [""]
    new_lines = lines[:idx] + block + lines[idx:]
    path.write_text("\n".join(new_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    print("updated", path.relative_to(ROOT))


def main() -> None:
    for p in sorted(GUIDES):
        insert_toc(p)


if __name__ == "__main__":
    main()
