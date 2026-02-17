# Документы

Базовый домен: `https://documents-api.wildberries.ru`

## Сценарии использования

1. Получить категории: `GET /api/v1/documents/categories`
2. Получить список документов: `GET /api/v1/documents/list`
3. Скачать один документ: `GET /api/v1/documents/download`
4. Скачать несколько документов: `POST /api/v1/documents/download/all`

---

## 1) GET `/api/v1/documents/categories`

**Назначение:** получить категории документов для последующей фильтрации в списке документов.

### Лимит

- `10 сек`: 1 запрос
- интервал: 10 сек
- всплеск: 5

### Пример

```bash
curl -G "https://documents-api.wildberries.ru/api/v1/documents/categories" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "locale=ru"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `locale` | string | нет | Язык поля `title`: `ru`, `en`, `zh`. По умолчанию `en` |

### Ответ `200`

`GetCategories`:
- `data.categories[]` — категории документов.

Поля `categories[]`:

| Поле | Тип | Описание |
|---|---|---|
| `name` | string | ID категории (используется в query-параметре `category` метода списка) |
| `title` | string | Локализованное название категории |

### Ошибки

- `401` — не авторизован
- `429` — превышен лимит

---

## 2) GET `/api/v1/documents/list`

**Назначение:** получить список документов продавца.

### Лимит

- `10 сек`: 1 запрос
- интервал: 10 сек
- всплеск: 5

### Пример

```bash
curl -G "https://documents-api.wildberries.ru/api/v1/documents/list" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "locale=ru" \
  --data-urlencode "beginTime=2024-07-09" \
  --data-urlencode "endTime=2024-07-15" \
  --data-urlencode "sort=date" \
  --data-urlencode "order=desc" \
  --data-urlencode "limit=10" \
  --data-urlencode "offset=0"
```

### Query-параметры

| Параметр | Тип | Обяз. | Ограничения и описание |
|---|---|---|---|
| `locale` | string | нет | Язык поля `category`: `ru`, `en`, `zh`. По умолчанию `en` |
| `beginTime` | date | нет | Начало периода. Передаётся только вместе с `endTime` |
| `endTime` | date | нет | Конец периода. Передаётся только вместе с `beginTime` |
| `sort` | enum | нет | `date` или `category`. Передаётся только вместе с `order`; для `category` требуется `locale=ru` |
| `order` | enum | нет | `desc` или `asc`. Передаётся только вместе с `sort` |
| `category` | string | нет | ID категории из `GET /api/v1/documents/categories` (`name`) |
| `serviceName` | string | нет | Уникальный ID документа |
| `limit` | integer | нет | Максимум 50, по умолчанию 50 |
| `offset` | integer | нет | Смещение (после какой строки выдавать данные), по умолчанию 0 |

### Ответ `200`

`GetList`:
- `data.documents[]` — список документов.

Поля `documents[]`:

| Поле | Тип | Описание |
|---|---|---|
| `serviceName` | string | Уникальный ID документа |
| `name` | string | Название документа |
| `category` | string | Название категории документа |
| `extensions` | array<string> | Доступные форматы документа |
| `creationTime` | string(date-time) | Дата/время создания документа |
| `viewed` | boolean | Был ли документ выгружен в ЛК |

### Ошибки

- `400` — `Responses400List` (например, `sort` и `order` указаны не вместе; `limit > 50`)
- `401`
- `429`

---

## 3) GET `/api/v1/documents/download`

**Назначение:** скачать один документ по `serviceName` и `extension`.

### Лимит

- `10 сек`: 1 запрос
- интервал: 10 сек
- всплеск: 5

### Пример

```bash
curl -G "https://documents-api.wildberries.ru/api/v1/documents/download" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "serviceName=redeem-notification-44841941" \
  --data-urlencode "extension=zip"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `serviceName` | string | да | Уникальный ID документа |
| `extension` | string | да | Формат документа (например, `zip`, `xlsx`) |

### Ответ `200`

`GetDoc`:

| Поле | Тип | Описание |
|---|---|---|
| `data.fileName` | string | Имя файла |
| `data.extension` | string | Формат файла |
| `data.document` | string | Файл в base64 |

### Ошибки

- `400` — `Responses400Download` (например, отсутствуют `serviceName`/`extension`)
- `401`
- `429`

---

## 4) POST `/api/v1/documents/download/all`

**Назначение:** скачать несколько документов одним запросом.

### Лимит

- `5 мин`: 1 запрос
- интервал: 5 мин
- всплеск: 5

### Пример

```bash
curl -X POST "https://documents-api.wildberries.ru/api/v1/documents/download/all" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "params": [
      {
        "serviceName": "redeem-notification-44841941",
        "extension": "zip"
      },
      {
        "serviceName": "act-income-mp-392460936",
        "extension": "xlsx"
      }
    ]
  }'
```

### Тело запроса

`requestDownload`:

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `params` | array | да | Список документов для скачивания, от 1 до 50 элементов |

Поля `params[]`:

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `serviceName` | string | да | Уникальный ID документа |
| `extension` | string | да | Формат документа |

### Ответ `200`

`GetDocs`:

| Поле | Тип | Описание |
|---|---|---|
| `data.fileName` | string | Имя файла архива |
| `data.extension` | string | Формат результата |
| `data.document` | string | Архив с документами в base64 |

### Ошибки

- `400` — `Responses400DownloadAll`:
  - в `params` нет ни одного корректного элемента (`serviceName` + `extension`)
  - в `params` больше 50 документов
- `401`
- `429`
