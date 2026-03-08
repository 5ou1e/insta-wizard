<p align="center">
  <img src="logo.png" width="50%" alt="InstaWizard">
</p>

<p align="center">Python-клиент для работы с приватным мобильным и веб API Instagram — с синхронным и асинхронным интерфейсом.</p>

<p align="center">
  <a href="https://pypi.org/project/insta-wizard/"><img src="https://img.shields.io/pypi/v/insta-wizard" alt="PyPI"></a>
  <a href="https://pypi.org/project/insta-wizard/"><img src="https://img.shields.io/pypi/pyversions/insta-wizard" alt="Python"></a>
  <a href="https://github.com/5ou1e/insta-wizard/blob/main/LICENSE"><img src="https://img.shields.io/github/license/5ou1e/insta-wizard" alt="License"></a>
  <a href="https://github.com/5ou1e/insta-wizard/actions/workflows/tests.yml"><img src="https://github.com/5ou1e/insta-wizard/actions/workflows/tests.yml/badge.svg" alt="Tests"></a></p>

<p align="center"><small>🌐 <strong>Языки:</strong> <a href="README.md">English</a> · Русский</small></p>

---

## Возможности

### Общее

- ⚡ **Async & sync** — нативные async-клиенты и синхронные обёртки из коробки
- 💻 **Мобильный и веб-клиенты**
  - `MobileClient` / `SyncMobileClient` — приватный мобильный API (имитирует официальное Android-приложение)
  - `WebClient` / `SyncWebClient` — веб-API (имитирует поведение браузера)
- 🌐 **Поддержка HTTP-прокси** — статический или с автоматической ротацией через провайдер
- 📱 **Отпечатки устройств и браузеров** — встроенные пресеты и случайная генерация
- 💾 **Сохранение сессии** — `dump_state()` / `load_state()`, без повторной авторизации при каждом запуске
- 📋 **Интеграция со стандартным модулем `logging`** из коробки

Весь функционал ниже доступен в async и sync клиентах.

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

**Mobile (async):**

```python
import asyncio
from insta_wizard import MobileClient

async def main() -> None:
    async with MobileClient() as client:
        await client.login("USERNAME", "PASSWORD")

        me = await client.account.get_current_user()
        print("Вы вошли как:", me.username)

        user = await client.users.get_info_by_username("instagram")
        await client.friendships.follow(user.pk)

asyncio.run(main())
```

**Web (async):**

```python
import asyncio
from insta_wizard import WebClient

async def main() -> None:
    async with WebClient() as client:
        await client.login("USERNAME", "PASSWORD")

        await client.likes.like("MEDIA_ID")
        await client.likes.unlike("MEDIA_ID")

asyncio.run(main())
```

**Sync — без asyncio:**

```python
from insta_wizard import SyncMobileClient

with SyncMobileClient() as client:
    client.login("USERNAME", "PASSWORD")

    me = client.account.get_current_user()
    print("Вы вошли как:", me.username)

    user = client.users.get_info_by_username("instagram")
    client.friendships.follow(user.pk)
```

---

## Прокси

Клиент поддерживает работу через прокси. На данный момент поддерживаются только HTTP/HTTPS прокси — с авторизацией и без.

```python
from insta_wizard import MobileClient, ProxyInfo

# Поддерживаемые форматы: "1.2.3.4:8080", "user:pass@1.2.3.4:8080", "1.2.3.4:8080:user:pass"
proxy = ProxyInfo.from_string("user:pass@1.2.3.4:8080")

async with MobileClient(proxy=proxy) as client:
    ...
    await client.set_proxy(ProxyInfo.from_string("..."))  # сменить прокси во время работы
    await client.set_proxy(None)                          # или отключить
```

При сетевых ошибках клиент может автоматически повторять запрос и при необходимости сменить прокси — настраивается через `TransportSettings`:

**Автоматическая ротация** — реализуйте `ProxyProvider` и передайте его через `TransportSettings`:

```python
import random

from insta_wizard import TransportSettings, ProxyInfo
from insta_wizard.common.interfaces import ProxyProvider

class MyProxyPool(ProxyProvider):
    _proxies = [
        "194.67.201.14:8080:user1:pass1",
        "91.108.4.220:3128:user2:pass2",
        "185.199.229.156:7492:user3:pass3",
    ]

    async def provide_new(self) -> ProxyInfo | None:
        return ProxyInfo.from_string(random.choice(self._proxies))

settings = TransportSettings(
    network_error_retry_limit=3,   # 3 попытки на каждый прокси перед сменой
    network_error_retry_delay=1.0, # пауза 1 с между попытками
    change_proxies=True,           # менять прокси после исчерпания всех попыток
    proxy_change_limit=5,          # не более 5 смен, затем выбрасывается NetworkError
    proxy_provider=MyProxyPool(),
)

async with MobileClient(transport_settings=settings) as client:
    ...
```
После исчерпания всех попыток клиент вызывает `proxy_provider.provide_new()` и повторяет запрос с новым прокси.

---

## Пресеты устройств и браузеров

Вы можете задать настройки устройства для клиента (user-agent, фингерпринт и т.д.). Если не указать явно — будет автоматически выбран стандартный пресет.

**Mobile (Android):**

```python
from insta_wizard import AndroidDeviceInfo, MobileClient
from insta_wizard.mobile.models.android_device_info import AndroidPreset

device = AndroidDeviceInfo.from_preset(AndroidPreset.SAMSUNG_A16)
device = AndroidDeviceInfo.from_preset(AndroidPreset.PIXEL_8, locale="en_US", timezone="America/New_York")
device = AndroidDeviceInfo.random()  # случайный пресет из реально существующих Android-устройств

async with MobileClient(device=device) as client:
    ...
```

Доступные пресеты: `SAMSUNG_A16`, `SAMSUNG_S23`, `SAMSUNG_A54`, `PIXEL_8`, `REDMI_NOTE_13_PRO`

**Web (браузер):**

```python
from insta_wizard import BrowserDeviceInfo, WebClient
from insta_wizard.web.models.device_info import BrowserPreset

device = BrowserDeviceInfo.from_preset(BrowserPreset.CHROME_143_WIN11)
device = BrowserDeviceInfo.random()  # случайный пресет из реально существующих конфигураций браузеров

async with WebClient(device=device) as client:
    ...
```

Доступные пресеты: `CHROME_143_WIN11`, `CHROME_143_MACOS`

---

## Сохранение сессии

Сохраняйте сессию между запусками — без необходимости входить заново:

```python
import asyncio, json
from insta_wizard import MobileClient

async def main() -> None:
    async with MobileClient() as client:
        await client.login("USERNAME", "PASSWORD")

        with open("session.json", "w", encoding="utf-8") as f:
            json.dump(client.dump_state(), f)

asyncio.run(main())
```

Восстановление при следующем запуске:

```python
import asyncio, json
from insta_wizard import MobileClient

async def main() -> None:
    async with MobileClient() as client:
        with open("session.json", encoding="utf-8") as f:
            client.load_state(json.load(f))

        me = await client.account.get_current_user()  # уже авторизован

asyncio.run(main())
```

Состояние — это обычный Python-словарь. Настройки прокси и транспорта в него не входят — передавайте их в конструктор как обычно.

---

## Логирование

По умолчанию клиенты используют стандартный модуль `logging`. Для включения вывода:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

Для использования **собственного логгера** или отключения логирования:

```python
from insta_wizard import MobileClient, NoOpInstagramClientLogger

async with MobileClient(logger=NoOpInstagramClientLogger()) as client:
    ...
```

Пример кастомного логгера — в [`examples/logging_setup.py`](examples/logging_setup.py).

---

## Команды

Команды — это типизированные обёртки над отдельными API-запросами, возвращающие ответ как есть. В ряде случаев может быть полезно вызывать их напрямую через `client.execute()`:

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

---

## Отказ от ответственности

Данная библиотека является инструментом для разработчиков, предназначенным для создания персональных интеграций и изучения API Instagram. Она **не предназначена** для рассылки спама, масштабной автоматизации или любой деятельности, нарушающей [Условия использования Instagram](https://help.instagram.com/581066165581870). Мы не аффилированы с Meta или Instagram. Используйте только с аккаунтами и данными, доступ к которым у Вас есть.

---

## Лицензия

MIT — см. [LICENSE](LICENSE)
