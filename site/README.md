# Просмотр гайдов с тултипами Wowhead

## Важно: не путайте Markdown и HTML на GitHub

На **github.com** при открытии `guides/*.md` тултипов **не будет** — GitHub показывает только текст, без скриптов.

Нужна **HTML-версия**:

- **GitHub Pages:** https://pavend1.github.io/wow-guides/ (после включения Actions в Settings → Pages)
- **Локально:** `python scripts/serve_guides.py --build --open`

## Как работают тултипы

Скрипт `tooltips-fallback.js` при наведении на ссылку вида  
`https://www.wowhead.com/ru/spell=53600` запрашивает  
`https://nether.wowhead.com/tooltip/spell/53600?locale=7`  
и показывает HTML-тултип (как в игре, на русском).

Старый виджет `wow.zamimg.com/widgets/power.js` **не используется** — он часто не грузится из РФ и на GitHub Pages.

## Сборка

```bash
python scripts/build_guide_site.py
```

Файлы в `site/`: `index.html` + страница на каждый гайд.

## IntelliJ IDEA

**Run → Guides: сервер (HTML + тултипы)** — сборка, http://127.0.0.1:8080/, браузер.

## GitHub Pages

Workflow: `.github/workflows/pages.yml` (сборка + деплой `site/`).

1. **Settings → Pages → Source: GitHub Actions**
2. Push в `main` → Actions → **Deploy guides (GitHub Pages)**

## Ограничения

- Нужен интернет и доступ к `nether.wowhead.com`.
- После правки `.md` пересоберите HTML (`build_guide_site.py` или push в `main` с workflow).
