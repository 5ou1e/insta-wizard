# insta-wizard
<small>[English](README.md)</small>

[![PyPI](https://img.shields.io/pypi/v/insta-wizard)](https://pypi.org/project/insta-wizard/)
[![Python](https://img.shields.io/pypi/pyversions/insta-wizard)](https://pypi.org/project/insta-wizard/)
[![License](https://img.shields.io/github/license/5ou1e/insta-wizard)](LICENSE)

Асинхронная Python-библиотека для работы с Instagram.

Управление профилем, подписки и отписки, работа с Direct, лайки и комментарии, получение информации о пользователях — и многое другое через удобный асинхронный интерфейс.

Предоставляет два клиента:
- **`MobileInstagramClient`** — имитирует поведение официального Android-приложения, работает с **приватным мобильным API (v374)**
- **`WebInstagramClient`** — работает с **веб API**, имитируя поведение браузера

Поддержка прокси, пресеты устройств и профилей, гибкое управление состоянием сессий и куков.

> **Планируется:** регистрация аккаунтов, расширение покрытия API.

> **Статус:** активная разработка (API может меняться между версиями).


---

## Установка

```bash
pip install insta-wizard
```

---

## Быстрый старт

```python
import asyncio
from insta_wizard import MobileInstagramClient

async def main():
    async with MobileInstagramClient() as client:
        await client.account.login("username", "password")
        user = await client.users.get_info("1200123809")  # числовой ID пользователя в виде строки
        print(user)

asyncio.run(main())
```

---

## Обзор клиентов

| Клиент | Описание                                                                                                                             |
|---|--------------------------------------------------------------------------------------------------------------------------------------|
| `MobileInstagramClient` | Клиент для работы с приватным API Instagram, имитирует поведение официального Android-приложения |
| `WebInstagramClient` | Клиент для работы с веб API Instagram, имитирующий поведение браузера                                                                |

**Mobile-клиент** покрывает большую часть функционала Instagram. Web-клиент предоставляет схожий функционал, но работает с другими API-эндпоинтами Instagram.

## Основные возможности

**Mobile-клиент**:
- Логин, управление профилем (редактировать bio, имя, фото профиля)
- Поиск пользователей, получение информации по ID или username
- Подписка / отписка, управление списками фолловеров и фолловинга
- Лента, истории, suggested reels
- Direct: входящие, ожидающие запросы, отправка текстовых сообщений и реакций, управление тредами (создать групповой, одобрить, отклонить, скрыть, замьютить)
- Комментарии: получить, добавить, лайкнуть, анлайкнуть
- Уведомления и inbox активности
- Live и Clips discovery
- Определение и прохождение чекпоинтов (VettedDelta и ScrapingWarning)

**Web-клиент**:
- Логин
- Подписка / отписка
- Лайк / анлайк медиа
- Добавление / лайк / анлайк комментариев
- Определение и прохождение чекпоинтов (VettedDelta и ScrapingWarning)

---

## Два стиля API

### 1. Методы секций (основной интерфейс)

Секции — атрибуты клиента. Это основной и рекомендуемый способ работы с библиотекой — они покрывают большинство практических сценариев:

```python
# Аккаунт
await client.account.login("username", "password")
me = await client.account.get_current_user()

# Пользователи
user = await client.users.get_info_by_username("someuser")
user = await client.users.get_info(user_id)
results = await client.users.search("query")

# Подписки
await client.friendships.follow(user_id)
await client.friendships.unfollow(user_id)
await client.friendships.remove_follower(user_id)
followers = await client.friendships.get_user_followers(user_id)
following = await client.friendships.get_user_following(user_id)

# Лента
timeline = await client.feed.get_timeline()
stories  = await client.feed.get_stories_tray()
reels    = await client.feed.get_suggested_reels()

# Директ
inbox   = await client.direct.get_inbox()
pending = await client.direct.get_pending()

# Медиа и комментарии
comments = await client.media.get_comments(media_id)
await client.media.add_comment(media_id, "отличный пост!")
await client.media.like_comment(comment_id)
await client.media.unlike_comment(comment_id)

# Чекпоинты (во время активной сессии)
from insta_wizard.mobile.exceptions import ChallengeRequiredError
from insta_wizard.common.models.checkpoint import VettedDeltaCheckpoint, ScrapingWarningCheckpoint

try:
    me = await client.account.get_current_user()
except ChallengeRequiredError as e:
    checkpoint = await client.challenge.get_challenge_info(e.challenge_data)
    match checkpoint:
        case VettedDeltaCheckpoint():
            await client.challenge.pass_vetted_delta(choice="0")  # "Это был я"
        case ScrapingWarningCheckpoint():
            await client.challenge.pass_scraping_warning()
```

**Mobile client:**

| Секция | Что покрывает                                                                      |
|---|------------------------------------------------------------------------------------|
| `account` | логин/логаут, получить текущего пользователя, редактирование профиля, bio, аватара |
| `users` | инфо о пользователе по id / username, web profile, поиск                           |
| `friendships` | подписка, отписка, удалить подписчика, списки фолловеров / фолловинга, статус      |
| `feed` | лента, stories tray, suggested reels                                               |
| `direct` | входящие, ожидающие, presence, отправка сообщений и реакций, управление тредами    |
| `media` | лайк, анлайк, сохранение, редактирование, удаление, комментарии (получить / добавить / лайкнуть / анлайкнуть) |
| `challenge` | определение и прохождение чекпоинтов               |

**Web client:**

| Секция | Что покрывает                                |
|---|----------------------------------------------|
| `account` | инфо об аккаунте, редактирование профиля     |
| `friendships` | подписка, отписка                            |
| `comments` | добавить / лайкнуть / анлайкнуть комментарий |
| `likes` | лайк / анлайк медиа                          |
| `challenge` | определение и прохождение чекпоинтов |

Секции покрывают большинство практических сценариев. Если нужен полный контроль над параметрами или доступ к командам, ещё не выставленным через секции — используйте прямой вызов команд.

### 2. Команды

Команды — базовые строительные блоки библиотеки. Каждая команда является типизированной обёрткой над одним запросом к Instagram API — в 99% случаев одна команда = один API-запрос.

Методы секций — это удобный слой поверх команд. Любую команду можно вызвать напрямую через `client.execute()` — когда нужен полный контроль над параметрами или доступ к командам, ещё не выставленным через секции:

```python
from insta_wizard.mobile.commands.user.usernameinfo import UserUsernameInfo

user = await client.execute(UserUsernameInfo(username="someuser"))
```

### Просмотр доступных команд

```python
from insta_wizard.mobile import print_help

print_help()  # выводит таблицу: имя команды, модуль, сигнатура
```

Для web:

```python
from insta_wizard.web import print_help

print_help()
```

---

## Общие возможности

### Прокси

```python
from insta_wizard import MobileInstagramClient, ProxyInfo

proxy = ProxyInfo.from_string("user:pass@1.2.3.4:8080")

async with MobileInstagramClient(proxy=proxy) as client:
    ...
```

Поддерживаемые форматы `from_string`:

```
1.2.3.4:8080
http://1.2.3.4:8080
user:pass@1.2.3.4:8080
http://user:pass@1.2.3.4:8080
1.2.3.4:8080:user:pass
http://1.2.3.4:8080:user:pass
```

Прокси можно менять в рантайме:

```python
await client.set_proxy(ProxyInfo.from_string("..."))
await client.set_proxy(None)  # убрать прокси
```

### Авто-ротация прокси при сетевых ошибках

Реализуйте `ProxyProvider` и передайте через `TransportSettings`:

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

Когда все попытки исчерпаны, клиент вызывает `proxy_provider.provide_new()` и повторяет запрос с новым прокси.

### Сохранение и восстановление сессии

Переиспользование сессии между запусками — без повторного логина:

```python
import json
from insta_wizard import MobileInstagramClient

# Сохранение после логина
async with MobileInstagramClient() as client:
    await client.account.login("username", "password")

    state = client.dump_state()
    with open("session.json", "w") as f:
        json.dump(state, f)

# Восстановление при следующем запуске
async with MobileInstagramClient() as client:
    with open("session.json") as f:
        client.load_state(json.load(f))

    me = await client.account.get_current_user()  # уже авторизован
```

Состояние — обычный Python-словарь, можно работать с ним напрямую:

```python
state = client.dump_state()  # возвращает dict
client.load_state(state)     # принимает dict
```

> `dump_state` / `load_state` не включают прокси и настройки транспорта — их передавайте в конструктор как обычно.

### TransportSettings

```python
from insta_wizard import TransportSettings

settings = TransportSettings(
    max_network_wait_time=30.0,               # таймаут запроса в секундах
    max_retries_on_network_errors=3,
    delay_before_retries_on_network_errors=1.0,
)

async with MobileInstagramClient(transport_settings=settings) as client:
    ...
```

---

## Mobile-клиент

### Пресеты устройств

```python
from insta_wizard import AndroidDeviceInfo, MobileInstagramClient
from insta_wizard.mobile.models.android_device_info import AndroidPreset

# из пресета
device = AndroidDeviceInfo.from_preset(AndroidPreset.SAMSUNG_A16)

# с переопределениями
device = AndroidDeviceInfo.from_preset(AndroidPreset.PIXEL_8, locale="ru_RU", timezone="Europe/Moscow")

# случайный пресет
device = AndroidDeviceInfo.random()

async with MobileInstagramClient(device=device) as client:
    ...
```

Доступные пресеты: `SAMSUNG_A16`, `SAMSUNG_S23`, `SAMSUNG_A54`, `PIXEL_8`, `REDMI_NOTE_13_PRO`.

### Локальные данные

`MobileClientLocalData` хранит cookies, токены авторизации и device IDs, которые создаются при логине:

```python
from insta_wizard import MobileInstagramClient, MobileClientLocalData

local_data = MobileClientLocalData.create()  # пустые, новые
client = MobileInstagramClient(local_data=local_data)

# прочитать обратно позже
local_data = client.get_local_data()
```


## Web-клиент

Работает с веб API Instagram, имитируя поведение браузера. Предоставляет схожий с mobile-клиентом функционал, но использует другие API-эндпоинты.

### Пресеты устройств

```python
from insta_wizard import BrowserDeviceInfo, WebInstagramClient
from insta_wizard.web.models.device_info import BrowserPreset

device = BrowserDeviceInfo.from_preset(BrowserPreset.CHROME_143_WIN11)
device = BrowserDeviceInfo.from_preset(BrowserPreset.CHROME_143_MACOS, locale="ru_RU")
device = BrowserDeviceInfo.random()

async with WebInstagramClient(device=device) as client:
    ...
```

Доступные пресеты: `CHROME_143_WIN11`, `CHROME_143_MACOS`.

### Логин

```python
import asyncio
from insta_wizard import WebInstagramClient

async def main():
    async with WebInstagramClient() as client:
        await client.account.login("...", "...")
        cookies = client.get_cookies()

asyncio.run(main())
```

### Подписка на пользователя

```python
async with WebInstagramClient() as client:
    await client.account.login("...", "...")
    await client.friendships.follow("1200123809")  # числовой ID пользователя в виде строки
```

### Cookies

```python
# передать существующие cookies (например, от прошлой сессии)
client.set_cookies({"sessionid": "...", "csrftoken": "...", "mid": "..."})

# прочитать текущие cookies
cookies = client.get_cookies()  # dict
```

---

## Исключения

Основные исключения, которые стоит обрабатывать:

**Базовое (`insta_wizard`):**

| Исключение | Описание |
|---|---|
| `InstaWizardError` | Базовый класс для всех ошибок библиотеки |

**Mobile (`insta_wizard.mobile.exceptions`):**

| Исключение | Когда возникает |
|---|---|
| `ChallengeRequiredError` | Чекпоинт во время активной сессии |
| `LoginChallengeRequiredError` | Проверка при логине (базовый класс) |
| `LoginTwoStepVerificationRequiredError` | Требуется код двухэтапной проверки при логине |
| `LoginUnknownChallengeRequiredError` | Неизвестная проверка при логине |
| `LoginError` | Ошибка авторизации |
| `LoginBadPasswordError` | Неверный пароль |
| `TooManyRequestsError` | Превышен лимит запросов (HTTP 429) |
| `FeedbackRequiredError` | Действие заблокировано Instagram |
| `UnauthorizedError` | Сессия недействительна или истекла |
| `NetworkError` | Проблема с сетевым соединением |
| `NotFoundError` | Запрошенный ресурс не найден |

**Web (`insta_wizard.web.exceptions`):**

| Исключение | Когда возникает |
|---|---|
| `CheckpointRequiredError` | Чекпоинт во время активной сессии |
| `LoginCheckpointRequiredError` | Чекпоинт при логине |
| `LoginError` | Ошибка авторизации |
| `LoginBadPasswordError` | Неверный пароль |
| `TooManyRequestsError` | Превышен лимит запросов (HTTP 429) |
| `NetworkError` | Проблема с сетевым соединением |
| `StateParametersMissingError` | Не инициализировано состояние (вызовите `initialize_state()`) |

**Транспорт (`insta_wizard.common.transport.exceptions`):**

| Исключение | Когда возникает |
|---|---|
| `TransportTimeoutError` | Таймаут запроса |
| `TransportNetworkError` | Низкоуровневая сетевая ошибка |

---


## Roadmap

Планируется реализовать и улучшить:

- [ ] Прохождение чекпоинтов авторизации
- [ ] Регистрация аккаунтов
- [ ] Доработка функционала (новые методы API Instagram)
- [ ] Поддержка синхронного взаимодействия (API) клиентов
---

## Дисклеймер

Проект является инструментом для разработчиков, предназначенным для создания персональных интеграций и изучения Instagram API. Он **не предназначен** для автоматизации, массового ботоводства, рассылки спама или любой другой деятельности, нарушающей [Условия использования Instagram](https://help.instagram.com/581066165581870). Проект не аффилирован с Meta и Instagram. Используйте только с аккаунтами и данными, на которые у вас есть права. Соблюдайте применимые законы и правила платформы.

## Лицензия

MIT — см. [LICENSE](LICENSE)
