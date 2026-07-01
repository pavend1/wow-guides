# WoW Guides (RU)

Гайды для **русского клиента**: названия способностей, подземелий и предметов сверяются с [Wowhead RU](https://www.wowhead.com/ru) (tooltip API, `locale=7`).

Патч: **12.0.5**, Midnight Season 1.

## Гайды

| Файл | Класс / режим |
|------|----------------|
| [guides/mplus/prot-paladin-mplus-ru.md](guides/mplus/prot-paladin-mplus-ru.md) | Прот-паладин, Mythic+ |
| [guides/mplus/guardian-druid-mplus-ru.md](guides/mplus/guardian-druid-mplus-ru.md) | Страж (медведь), Mythic+ |
| [guides/mplus/brewmaster-monk-mplus-ru.md](guides/mplus/brewmaster-monk-mplus-ru.md) | Пивовар, Mythic+ |
| [guides/mplus/shadow-priest-mplus-ru.md](guides/mplus/shadow-priest-mplus-ru.md) | Теневой жрец (ШП), Mythic+ |
| [guides/mplus/discipline-priest-mplus-ru.md](guides/mplus/discipline-priest-mplus-ru.md) | Послушание (дис жрец), Mythic+ |
| [guides/mplus/unholy-dk-mplus-ru.md](guides/mplus/unholy-dk-mplus-ru.md) | Анхоли ДК (нечестивый), Mythic+ |
| [guides/mplus/subtlety-rogue-mplus-ru.md](guides/mplus/subtlety-rogue-mplus-ru.md) | Разбойник (Скрытность), Mythic+ |
| [guides/mplus/outlaw-rogue-mplus-ru.md](guides/mplus/outlaw-rogue-mplus-ru.md) | Разбойник (Головорез), Mythic+ |
| [guides/mplus/demonology-warlock-mplus-ru.md](guides/mplus/demonology-warlock-mplus-ru.md) | Демонолог (варлок), Mythic+ |
| [guides/rotation/devourer-dh-rotation-ru.md](guides/rotation/devourer-dh-rotation-ru.md) | Охотник на демонов — Пожиратель, ротация |
| [guides/rotation/augmentation-evoker-rotation-ru.md](guides/rotation/augmentation-evoker-rotation-ru.md) | Пробудитель — Насыщатель, ротация |
| [guides/mplus/frost-mage-mplus-ru.md](guides/mplus/frost-mage-mplus-ru.md) | Фрост-маг, Mythic+ |

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

| Где открываете | Тултипы |
|----------------|---------|
| Файлы `guides/*.md` на **github.com** (просмотр Markdown) | **Нет** — GitHub не запускает JavaScript |
| **GitHub Pages** (`site/*.html`) | **Да** — см. ниже |
| Локально: `python scripts/serve_guides.py --build --open` | **Да** |
| IntelliJ: **Guides: сервер (HTML + тултипы)** | **Да** |

### GitHub Pages (рекомендуется для браузера)

1. Запушьте изменения в `main`.
2. На GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Дождитесь зелёного workflow **Deploy guides (GitHub Pages)**.
4. Откройте сайт: `https://pavend1.github.io/wow-guides/` (не `.md` в репозитории).

**Приватный репозиторий:** GitHub Pages на бесплатном тарифе для private repo недоступен — сделайте репозиторий **public** и включите **Settings → Pages → GitHub Actions**, затем дождитесь зелёного workflow.

Тултипы: официальный **power.js** (как на Icy Veins). Если CDN Wowhead недоступен — запасной вариант через `nether.wowhead.com` + CSS Wowhead.

Подробности: [site/README.md](site/README.md).
