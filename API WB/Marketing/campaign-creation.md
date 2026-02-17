# Создание кампаний

Базовый домен: `https://advert-api.wildberries.ru`

---

## 1) POST `/api/advert/v1/bids/min`

**Назначение:** получить минимальные ставки (в копейках) для карточек товаров по местам размещения.

### Лимит

- `1 мин`: 20 запросов
- интервал: `3 сек`
- всплеск: 5

### Пример запроса

```bash
curl -X POST "https://advert-api.wildberries.ru/api/advert/v1/bids/min" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "advert_id": 98765432,
    "nm_ids": [12345678, 87654321],
    "payment_type": "cpm",
    "placement_types": ["combined", "search", "recommendation"]
  }'
```

### Тело запроса

| Поле | Тип | Обяз. | Ограничения и смысл |
|---|---|---|---|
| `advert_id` | int64 | да | ID кампании |
| `nm_ids` | array<int64> | да | Список артикулов WB, `1..100` |
| `payment_type` | enum | да | `cpm` / `cpc` |
| `placement_types` | array<enum> | да | `search`, `recommendation`, `combined` |

### Ответ `200`

| Поле | Тип | Описание |
|---|---|---|
| `bids` | array | Список карточек со ставками |

Элемент `bids[]`:

| Поле | Тип | Описание |
|---|---|---|
| `nm_id` | int64 | Артикул WB |
| `bids` | array | Минимальные ставки по размещениям |

Элемент внутреннего `bids[]`:

| Поле | Тип | Описание |
|---|---|---|
| `type` | enum | `combined`, `search`, `recommendation` |
| `value` | integer | Минимальная ставка, копейки |

### Ошибки

- `400` — `StandardizedBatchError`
- `401` — не авторизован
- `429` — превышен лимит

---

## 2) POST `/adv/v2/seacat/save-ad`

**Назначение:** создать кампанию с ручной или единой ставкой.

### Лимит

- `1 мин`: 5 запросов
- интервал: `12 сек`
- всплеск: 5

### Пример запроса

```bash
curl -X POST "https://advert-api.wildberries.ru/adv/v2/seacat/save-ad" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Телефоны",
    "nms": [146168367, 200425104],
    "bid_type": "manual",
    "payment_type": "cpm",
    "placement_types": ["search", "recommendations"]
  }'
```

### Тело запроса

| Поле | Тип | Обяз. | Ограничения и смысл |
|---|---|---|---|
| `name` | string | нет | Название кампании |
| `nms` | array<int> | нет | Товары для кампании, максимум 50 `nm` |
| `bid_type` | enum | нет | `manual` (по умолчанию) / `unified` |
| `payment_type` | enum | нет | `cpm` (default) / `cpc` |
| `placement_types` | array<enum> | нет | Для `manual`: `search`, `recommendations` |

Примечания:
- Для `cpc` при создании автоматически ставится минимальная ставка.
- Для `unified` поле `placement_types` не используется (по описанию метода).

### Ответ `200`

- Тип ответа: `integer`
- Значение: ID созданной кампании.

### Ошибки

- `400` — текстовая ошибка (пример: нет доступных категорий)
- `401` — не авторизован
- `429` — превышен лимит

---

## 3) GET `/adv/v1/supplier/subjects`

**Назначение:** получить список предметов, доступных для добавления в кампании.

### Лимит

- `12 сек`: 1 запрос
- интервал: `12 сек`
- всплеск: 5

### Пример запроса

```bash
curl -G "https://advert-api.wildberries.ru/adv/v1/supplier/subjects" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "payment_type=cpm"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `payment_type` | string | нет | Тип оплаты: `cpm` / `cpc`, default `cpm` |

### Ответ `200`

- Тип: `array` или `null`

Элемент массива:

| Поле | Тип | Описание |
|---|---|---|
| `id` | integer | ID предмета |
| `name` | string | Название предмета |
| `count` | integer | Количество артикулов WB с этим предметом |

### Ошибки

- `401` — не авторизован
- `404` — не найдено
- `429` — превышен лимит

---

## 4) POST `/adv/v2/supplier/nms`

**Назначение:** получить карточки товаров, доступные для кампаний, по ID предметов.

### Лимит

- `1 мин`: 5 запросов
- интервал: `12 сек`
- всплеск: 5

### Пример запроса

```bash
curl -X POST "https://advert-api.wildberries.ru/adv/v2/supplier/nms" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[123, 456, 765]'
```

### Тело запроса

- Тип: `array<integer>`
- Смысл: список `subjectId`, для которых нужно вернуть товары.

### Ответ `200`

Тип: `array`.

| Поле | Тип | Описание |
|---|---|---|
| `title` | string | Название товара |
| `nm` | integer | Артикул WB |
| `subjectId` | integer | ID предмета |

### Ошибки

- `400` — текстовая ошибка обработки тела
- `401` — не авторизован
- `429` — превышен лимит
