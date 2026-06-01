# Просмотр гайдов с тултипами Wowhead

## Важно: не путайте Markdown и HTML на GitHub

На **github.com** при открытии `guides/*.md` тултипов **не будет** — GitHub показывает только текст, без скриптов.

Нужна **HTML-версия**:

- **GitHub Pages:** https://pavend1.github.io/wow-guides/
- **Локально:** `python scripts/serve_guides.py --build --open`

## Как работают тултипы

1. **Основной режим:** официальный виджет [Wowhead power.js](https://www.wowhead.com/tooltips) — те же всплывающие подсказки, что на Icy Veins / Wowhead.
2. **Запасной режим:** если `wow.zamimg.com` не открывается (часто в РФ), через 2 с включается fallback: API `nether.wowhead.com` + стили Wowhead.

Ссылки в гайдах: `https://www.wowhead.com/ru/spell=53600` — тултип на русском.

## Сборка

```bash
python scripts/build_guide_site.py
```

## IntelliJ IDEA

**Run → Guides: сервер (HTML + тултипы)**

## GitHub Pages

Workflow `.github/workflows/pages.yml` — push в `main` → деплой `site/`.

## Ограничения

- Нужен интернет; для power.js — доступ к `wow.zamimg.com` (VPN / [WowTool.tips](https://wowtool.tips/) в РФ).
- После правки `.md` пересоберите HTML или сделайте push в `main`.
