# Если my.telegram.org выдаёт ERROR

## Быстрый обход (для бота)

В `.env` добавьте:

```env
TELEGRAM_USE_DESKTOP_API=1
```

Это использует пару ключей **Telegram Desktop** (официальный клиент). Для **бота**, который постит в ваш канал, обычно достаточно.

Затем:

```powershell
python scripts\send_telegram.py "Тест"
```

Свои ключи с my.telegram.org всё равно лучше получить, когда получится.

---

## Как пробить ERROR на my.telegram.org

Пробуйте **по одному пункту**, после каждого — новая попытка.

1. **Режим инкогнито** (Chrome / Edge / Firefox).
2. **Выключить** VPN, AdBlock, uBlock, Brave Shields.
3. Если без VPN не открывается — **другой VPN** или **мобильный интернет** (не Wi‑Fi).
4. Форма:
   - App title: `wow guides bot`
   - Short name: `wowguidesbot` (латиница, без пробелов)
   - URL: **пусто** или `https://example.com`
   - Platform: **Desktop** (не Other)
   - Description: `Bot posts WoW guides to my channel`
5. Жмите **Create application** несколько раз подряд (иногда срабатывает с 3–5 попытки).
6. **Телефон**: браузер на телефоне, LTE, без Wi‑Fi.
7. IP должен совпадать со **страной номера** Telegram (частая причина для RU/CIS).

---

## Уже есть приложение?

Откройте https://my.telegram.org/apps — возможно, api_id уже создан раньше, и создавать новое не нужно.

---

## Альтернатива

Попросите знакомого из другой страны создать приложение и прислать **вам** api_id + api_hash (не токен бота).
