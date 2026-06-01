# Просмотр гайдов с тултипами Wowhead

Обычный Markdown в Cursor / GitHub **не** запускает скрипты Wowhead — всплывающих подсказок там не будет.

Здесь собирается **HTML-версия** с официальным виджетом [Wowhead Tooltips](https://www.wowhead.com/tooltips) (`power.js`). При наведении на ссылку вида `https://www.wowhead.com/ru/spell=…` появляется тот же тултип, что на сайте Icy Veins.

## Сборка

```bash
python scripts/build_guide_site.py
```

Файлы появятся в `site/` (`index.html` + по странице на гайд).

## IntelliJ IDEA

В проекте есть shared run configuration (появится после открытия/синхронизации проекта):

**Run → Guides: сервер (HTML + тултипы)**

- пересобирает `site/` из `.md` (`--build`);
- поднимает сервер на http://127.0.0.1:8080/;
- открывает браузер (`--open`).

Остановка: **Ctrl+F2** или красный квадрат в Run.

Отдельно: **Guides: собрать HTML** — только сборка без сервера.

Если конфигурации не видны: **Run → Edit Configurations… → + → Python** → скрипт `scripts/serve_guides.py`, parameters `--build --open --port 8080`, working directory `site`.

## Как открыть (без IDE)

1. **Локальный сервер** (рекомендуется):

```bash
cd site
python -m http.server 8080
```

Откройте http://localhost:8080/

2. Двойной клик по `index.html` иногда работает, но браузер может блокировать загрузку `power.js` с `file://`.

## Ограничения

- Тултипы требуют **интернет** и доступ к `wow.zamimg.com` / Wowhead.
- В РФ иногда нужен VPN или расширение вроде [WowTool.tips](https://wowtool.tips/), если CDN Wowhead не открывается.
- Ссылки в гайдах уже ведут на **`/ru/`** — тултипы будут на русском.
- После правки `.md` пересоберите HTML (`build_guide_site.py`).

## Альтернативы

| Где читаете | Тултипы Wowhead |
|-------------|-----------------|
| `guides/*.md` в редакторе | Нет |
| `site/*.html` в браузере | Да |
| Свой сайт / GitHub Pages с `power.js` | Да |
| Публикация только в Telegram | Нет (только ссылки) |
