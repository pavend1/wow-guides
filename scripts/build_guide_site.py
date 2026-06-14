"""Build static HTML guides with Wowhead hover tooltips (power.js)."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# path, page title, class name, spec name, guide type label
GUIDES = [
    ("guides/mplus/prot-paladin-mplus-ru.md", "Прот-паладин — M+", "Паладин", "Защита", "M+"),
    ("guides/mplus/retribution-paladin-mplus-ru.md", "Ретри-паладин — M+", "Паладин", "Воздаяние", "M+"),
    ("guides/mplus/guardian-druid-mplus-ru.md", "Страж (медведь) — M+", "Друид", "Страж", "M+"),
    ("guides/mplus/brewmaster-monk-mplus-ru.md", "Пивовар — M+", "Монах", "Пивовар", "M+"),
    ("guides/mplus/shadow-priest-mplus-ru.md", "Теневой жрец (ШП) — M+", "Жрец", "Тень", "M+"),
    ("guides/mplus/unholy-dk-mplus-ru.md", "Анхоли ДК — M+", "Рыцарь смерти", "Нечестивость", "M+"),
    ("guides/mplus/subtlety-rogue-mplus-ru.md", "Скрытность — M+", "Разбойник", "Скрытность", "M+"),
    ("guides/mplus/demonology-warlock-mplus-ru.md", "Демонолог — M+", "Чернокнижник", "Демонология", "M+"),
    ("guides/rotation/devourer-dh-rotation-ru.md", "Пожиратель DH", "Охотник на демонов", "Пожиратель", "Ротация"),
    ("guides/rotation/augmentation-evoker-rotation-ru.md", "Насыщатель", "Пробудитель", "Насыщатель", "Ротация"),
]

CLASS_ORDER = [
    "Паладин",
    "Друид",
    "Монах",
    "Жрец",
    "Рыцарь смерти",
    "Разбойник",
    "Чернокнижник",
    "Охотник на демонов",
    "Пробудитель",
]
SITE = ROOT / "site"
TEMPLATE = SITE / "template.html"


def md_to_html(text: str) -> str:
    """Minimal Markdown → HTML (tables, headers, links, lists, code)."""
    lines = text.splitlines()
    out: list[str] = []
    in_code = False
    in_table = False
    in_ul = False
    in_blockquote = False
    i = 0

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def close_table():
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    def close_bq():
        nonlocal in_blockquote
        if in_blockquote:
            out.append("</blockquote>")
            in_blockquote = False

    def inline(s: str) -> str:
        s = html.escape(s, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(
            r"\[([^\]]+)\]\((https://www\.wowhead\.com/[^)]+)\)",
            r'<a href="\2">\1</a>',
            s,
        )
        s = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>'
            if not m.group(2).startswith("#")
            else f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
            s,
        )
        return s

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            close_ul()
            close_table()
            close_bq()
            if in_code:
                out.append("</pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            i += 1
            continue

        if in_code:
            out.append(html.escape(line) + "\n")
            i += 1
            continue

        if not stripped:
            close_ul()
            close_table()
            close_bq()
            i += 1
            continue

        if stripped.startswith(">"):
            close_ul()
            close_table()
            if not in_blockquote:
                out.append("<blockquote>")
                in_blockquote = True
            out.append(f"<p>{inline(stripped.lstrip('>').strip())}</p>")
            i += 1
            continue
        close_bq()

        if stripped.startswith("#"):
            close_ul()
            close_table()
            m = re.match(r"^(#{1,3})\s+(.+)$", stripped)
            if m:
                level = len(m.group(1))
                title = inline(m.group(2))
                slug = re.sub(r"<[^>]+>", "", title).lower()
                slug = re.sub(r"[^\w\s-]", " ", slug, flags=re.UNICODE)
                slug = re.sub(r"\s+", "-", slug.strip())
                out.append(f'<h{level} id="{slug}">{title}</h{level}>')
            i += 1
            continue

        if "|" in stripped and stripped.startswith("|"):
            close_ul()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.match(r"^[-:]+$", c) for c in cells):
                i += 1
                continue
            if not in_table:
                out.append("<table><tbody>")
                in_table = True
                tag = "th" if not any("</table>" in x for x in out[-3:]) and i > 0 and "|" in lines[i - 1] else "td"
                if out and "<table>" in out[-1]:
                    tag = "th"
                row = "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells)
                out.append(f"<tr>{row}</tr>")
                if tag == "th":
                    pass
            else:
                row = "".join(f"<td>{inline(c)}</td>" for c in cells)
                out.append(f"<tr>{row}</tr>")
            i += 1
            continue
        close_table()

        if stripped.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(stripped[2:])}</li>")
            i += 1
            continue
        close_ul()

        if stripped.startswith("---"):
            out.append("<hr>")
            i += 1
            continue

        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_ul()
    close_table()
    close_bq()
    if in_code:
        out.append("</pre>")
    return "\n".join(out)


def render_page(title: str, body_html: str) -> str:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    return tpl.replace("{{TITLE}}", html.escape(title)).replace("{{CONTENT}}", body_html)


def build_index(entries: list[tuple[str, str, str, str, str, str]]) -> str:
    by_class: dict[str, list[tuple[str, str, str]]] = {}
    for fname, _title, rel, class_name, spec_name, guide_type in entries:
        by_class.setdefault(class_name, []).append((fname, spec_name, guide_type))

    sections: list[str] = []
    for class_name in CLASS_ORDER:
        specs = by_class.get(class_name)
        if not specs:
            continue
        items = "\n".join(
            f'<li><a href="{fname}"><span class="index-spec">{html.escape(spec)}</span>'
            f'<span class="index-type">{html.escape(guide_type)}</span></a></li>'
            for fname, spec, guide_type in specs
        )
        sections.append(
            f'<section class="index-class">'
            f'<h2>{html.escape(class_name)}</h2>'
            f'<ul class="index-spec-list">{items}</ul>'
            f"</section>"
        )

    body = (
        "<h1>Гайды WoW (RU)</h1>"
        "<p>Наведите на ссылку Wowhead — всплывёт тултип с игры.</p>"
        + "".join(sections)
    )
    return render_page("Гайды WoW", body)


def main() -> None:
    SITE.mkdir(parents=True, exist_ok=True)
    built: list[tuple[str, str, str, str, str, str]] = []

    for rel, title, class_name, spec_name, guide_type in GUIDES:
        src = ROOT / rel
        md = src.read_text(encoding="utf-8")
        body = md_to_html(md)
        fname = Path(rel).stem + ".html"
        page = render_page(title, body)
        (SITE / fname).write_text(page, encoding="utf-8")
        built.append((fname, title, rel, class_name, spec_name, guide_type))
        print("built", fname)

    (SITE / "index.html").write_text(build_index(built), encoding="utf-8")
    print("built index.html")
    print("\nOpen: site/index.html (use a local server if tooltips fail on file://)")


if __name__ == "__main__":
    main()
