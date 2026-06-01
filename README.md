# WoW Guides (RU)

Гайды для **русского клиента**: названия способностей, подземелий и предметов сверяются с [Wowhead RU](https://www.wowhead.com/ru) (tooltip API, `locale=7`).

Патч: **12.0.5**, Midnight Season 1.

## Гайды

| Файл | Класс / режим |
|------|----------------|
| [guides/mplus/prot-paladin-mplus-ru.md](guides/mplus/prot-paladin-mplus-ru.md) | Прот-паладин, Mythic+ |
| [guides/mplus/guardian-druid-mplus-ru.md](guides/mplus/guardian-druid-mplus-ru.md) | Страж (медведь), Mythic+ |
| [guides/mplus/brewmaster-monk-mplus-ru.md](guides/mplus/brewmaster-monk-mplus-ru.md) | Пивовар, Mythic+ |
| [guides/rotation/devourer-dh-rotation-ru.md](guides/rotation/devourer-dh-rotation-ru.md) | Охотник на демонов — Пожиратель, ротация |

## Структура репозитория

```
guides/          — тексты гайдов (.md)
data/wowhead/    — JSON с русскими названиями (зоны, предметы, сверка API)
scripts/wowhead/ — загрузка и проверка имён с Wowhead
scripts/wcl/     — скрипты разбора логов Warcraft Logs (исследование)
archive/scratch/ — временные выгрузки, HTML/txt из парсинга (не гайды)
tg/              — отправка в Telegram
```

## Скрипты Wowhead

Из корня проекта:

```bash
python scripts/wowhead/fetch_items_ru.py
python scripts/wowhead/verify_guides.py
python scripts/wowhead/fetch_wowhead_ru.py
```

Отчёт о расхождениях ссылок в гайдах: `data/wowhead/verify_report.json`.

## Пул M+ S1 (имена зон)

Терраса Магистров · Пещеры Маисара · Узел Нексуса Зенас · **Шпили Ветрокрылых** (в ключе может быть «Шпиль…») · Академия Алгет'ар · Яма Сарона · Престол Триумвирата · Небесный Путь

См. также `data/wowhead/mplus_dungeons_ru.json` (достижения «Триумфатор ключей»).

## Тултипы Wowhead при наведении

В **`.md` в редакторе** всплывающих подсказок нет — это ограничение превью Markdown.

Чтобы получить тултипы как на Icy Veins / Wowhead, соберите HTML и откройте в браузере:

```bash
python scripts/build_guide_site.py
python scripts/serve_guides.py --build --open
```

**IntelliJ IDEA:** Run → **Guides: сервер (HTML + тултипы)**.

Подробности: [site/README.md](site/README.md).
