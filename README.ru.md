# InstaWizard
<small>🌐 **Языки:** [English](README.md) · Русский</small>

[![PyPI](https://img.shields.io/pypi/v/insta-wizard)](https://pypi.org/project/insta-wizard/)
[![Python](https://img.shields.io/pypi/pyversions/insta-wizard)](https://pypi.org/project/insta-wizard/)
[![License](https://img.shields.io/github/license/5ou1e/insta-wizard)](https://github.com/5ou1e/insta-wizard/blob/main/LICENSE)

Асинхронная Python-библиотека для работы с приватным API Instagram.

Управляйте профилями, подписывайтесь на пользователей, отправляйте сообщения в Direct, работайте с медиа и комментариями — через чистый, типизированный, полностью асинхронный интерфейс.

Библиотека предоставляет два клиента:

- **`MobileInstagramClient`** — имитирует официальное Android-приложение (приватный мобильный API, v374)
- **`WebInstagramClient`** — имитирует поведение браузера (веб-API Instagram)

---

## Возможности

### Общее

- ⚡ **Полностью асинхронный** — asyncio + aiohttp
- 💾 **Сохранение сессии** — `dump_state()` / `load_state()`, без повторной авторизации при каждом запуске
- 🖥️ **Отпечатки устройств и браузеров** — встроенные пресеты и случайная генерация
- 🔐 **Обнаружение и обработка Checkpoint / Challenge**
- 🌐 **Поддержка HTTP-прокси** — статический или с автоматической ротацией через провайдер
- 📋 **Интеграция со стандартным модулем `logging`** из коробки

### Мобильный клиент

- Авторизация и управление сессией
- Редактирование профиля (описание, имя, фото профиля)
- Поиск пользователей; получение информации по ID или имени пользователя
- Подписка / отписка, удаление подписчика; списки подписчиков и подписок
- Direct: входящие, запросы, отправка сообщений и реакций, управление групповыми чатами
- Медиа: лайки, отмена лайков, сохранение; комментарии — получение, добавление, лайки, отмена лайков
- Публикация медиа: фото и видео в ленту, Stories, карусели (альбомы) и Reels
- Обнаружение и прохождение Checkpoint / Challenge
- Регистрация аккаунтов через SMS / Email

### Веб-клиент

- Авторизация и сохранение сессии
- Подписка / отписка
- Лайки / отмена лайков медиа
- Добавление / лайк / отмена лайка комментариев
- Обнаружение и прохождение Checkpoint / Challenge

---

## Установка

**Требуется Python 3.11+**

```bash
pip install insta-wizard
```

Из GitHub (последняя версия):

```bash
pip install git+https://github.com/5ou1e/insta-wizard.git
```

---

## Быстрый старт

**Mobile:**

```python
import asyncio
from insta_wizard import MobileInstagramClient

async def main() -> None:
    async with MobileInstagramClient() as client:
        await client.account.login("USERNAME", "PASSWORD")

        me = await client.account.get_current_user()
        print("Вы вошли как:", me.username)

        user = await client.users.get_info_by_username("instagram")
        await client.friendships.follow(str(user.pk))

asyncio.run(main())
```

**Web:**

```python
import asyncio
from insta_wizard import WebInstagramClient

async def main() -> None:
    async with WebInstagramClient() as client:
        await client.login("USERNAME", "PASSWORD")

        await client.likes.like("MEDIA_ID")
        await client.likes.unlike("MEDIA_ID")

asyncio.run(main())
```

---

## Сохранение сессии

Сохраняйте сессию между запусками — без необходимости входить заново:

```python
import asyncio, json
from insta_wizard import MobileInstagramClient

async def main() -> None:
    async with MobileInstagramClient() as client:
        await client.account.login("USERNAME", "PASSWORD")

        with open("session.json", "w", encoding="utf-8") as f:
            json.dump(client.dump_state(), f)

asyncio.run(main())
```

Восстановление при следующем запуске:

```python
import asyncio, json
from insta_wizard import MobileInstagramClient

async def main() -> None:
    async with MobileInstagramClient() as client:
        with open("session.json", encoding="utf-8") as f:
            client.load_state(json.load(f))

        me = await client.account.get_current_user()  # уже авторизован

asyncio.run(main())
```

Состояние — это обычный Python-словарь. Настройки прокси и транспорта в него не входят — передавайте их в конструктор как обычно.

---

## Прокси

```python
from insta_wizard import MobileInstagramClient, ProxyInfo

proxy = ProxyInfo.from_string("user:pass@1.2.3.4:8080")

async with MobileInstagramClient(proxy=proxy) as client:
    ...
```

`ProxyInfo.from_string` принимает несколько форматов:

```
1.2.3.4:8080
http://1.2.3.4:8080
user:pass@1.2.3.4:8080
http://user:pass@1.2.3.4:8080
1.2.3.4:8080:user:pass
```

Смена или отключение прокси во время работы:

```python
await client.set_proxy(ProxyInfo.from_string("..."))
await client.set_proxy(None)
```

**Автоматическая ротация** — реализуйте `ProxyProvider` и передайте его через `TransportSettings`:

```python
from insta_wizard import TransportSettings, ProxyInfo
from insta_wizard.common.interfaces import ProxyProvider

class MyProxyPool(ProxyProvider):
    async def provide_new(self) -> ProxyInfo | None:
        return ProxyInfo.from_string(fetch_next_from_pool())

settings = TransportSettings(
    max_retries_on_network_errors=3,
    delay_before_retries_on_network_errors=1.0,
    change_proxy_after_all_failed_attempts=True,
    proxy_provider=MyProxyPool(),
)

async with MobileInstagramClient(transport_settings=settings) as client:
    ...
```

---

## Пресеты устройств и браузеров

**Mobile (Android):**

```python
from insta_wizard import AndroidDeviceInfo, MobileInstagramClient
from insta_wizard.mobile.models.android_device_info import AndroidPreset

device = AndroidDeviceInfo.from_preset(AndroidPreset.SAMSUNG_A16)
device = AndroidDeviceInfo.from_preset(AndroidPreset.PIXEL_8, locale="en_US", timezone="America/New_York")
device = AndroidDeviceInfo.random()

async with MobileInstagramClient(device=device) as client:
    ...
```

Доступные пресеты: `SAMSUNG_A16`, `SAMSUNG_S23`, `SAMSUNG_A54`, `PIXEL_8`, `REDMI_NOTE_13_PRO`

**Web (браузер):**

```python
from insta_wizard import BrowserDeviceInfo, WebInstagramClient
from insta_wizard.web.models.device_info import BrowserPreset

device = BrowserDeviceInfo.from_preset(BrowserPreset.CHROME_143_WIN11)
device = BrowserDeviceInfo.random()

async with WebInstagramClient(device=device) as client:
    ...
```

Доступные пресеты: `CHROME_143_WIN11`, `CHROME_143_MACOS`

---

## Логирование

По умолчанию клиенты используют стандартный модуль `logging`. Для включения вывода:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

Для использования **собственного логгера** или отключения логирования:

```python
from insta_wizard import MobileInstagramClient, NoOpInstagramClientLogger

async with MobileInstagramClient(logger=NoOpInstagramClientLogger()) as client:
    ...
```

Пример кастомного логгера — в [`examples/logging_setup.py`](examples/logging_setup.py).

---

## Команды

Секции охватывают наиболее распространённые сценарии использования, однако каждый их метод построен поверх **команд** — типизированных обёрток над отдельными вызовами API Instagram, возвращающих сырой ответ как есть. Вы можете выполнить любую команду напрямую через `client.execute()` — это полезно, когда необходимо выполнить какой-то запрос, и получить ответ "как есть".

```python
from insta_wizard.mobile.commands.user.usernameinfo import UserUsernameInfo

raw = await client.execute(UserUsernameInfo(username="someuser"))
```

Для просмотра всех доступных команд:

```python
from insta_wizard.mobile import print_help  # или insta_wizard.web

print_help()  # выводит таблицу: название команды, модуль, сигнатура
```

---

## Примеры

Готовые к запуску скрипты находятся в папке [`examples/`](examples) — пресеты устройств (mobile и web), настройка и ротация прокси, сохранение сессии и типовые сценарии работы с клиентом.

---

## Roadmap

- [ ] Прохождение Login Checkpoint
- [ ] Расширение покрытия API
- [ ] Синхронная обёртка клиента

---

## Отказ от ответственности

Данная библиотека является инструментом для разработчиков, предназначенным для создания персональных интеграций и изучения API Instagram. Она **не предназначена** для рассылки спама, масштабной автоматизации или любой деятельности, нарушающей [Условия использования Instagram](https://help.instagram.com/581066165581870). Мы не аффилированы с Meta или Instagram. Используйте только с аккаунтами и данными, доступ к которым у Вас есть.

---

## Лицензия

MIT — см. [LICENSE](LICENSE)
