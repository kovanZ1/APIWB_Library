# Поисковые кластеры

Базовый домен: `https://advert-api.wildberries.ru`

## Общие структуры

### Пара `(advert_id, nm_id)`

Используется почти во всех методах раздела:
- `advert_id` — ID кампании
- `nm_id` — артикул WB

### Общая ошибка `response400`

| Поле | Тип | Описание |
|---|---|---|
| `detail` | string | Детали ошибки |
| `origin` | string | Внутренний сервис |
| `request_id` | string | ID запроса |
| `status` | integer | HTTP-код |
| `title` | string | Заголовок |

---

## 1) POST `/adv/v0/normquery/get-bids`

**Назначение:** получить текущие ставки поисковых кластеров по кампаниям и артикулам.

### Лимит

- `1 сек`: 5 запросов, интервал `200 мс`, всплеск 10.

### Пример

```bash
curl -X POST "https://advert-api.wildberries.ru/adv/v0/normquery/get-bids" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"advert_id":1825035,"nm_id":983512347}]}'
```

### Тело запроса

| Поле | Тип | Обяз. | Ограничения |
|---|---|---|---|
| `items` | array<object> | да | максимум 100 |
| `items[].advert_id` | integer | да | ID кампании |
| `items[].nm_id` | integer | да | Артикул WB |

### Ответ `200`

| Поле | Тип | Описание |
|---|---|---|
| `bids` | array | Список ставок |

Элемент `bids[]`:

| Поле | Тип | Описание |
|---|---|---|
| `advert_id` | integer | ID кампании |
| `nm_id` | integer | Артикул WB |
| `norm_query` | string | Поисковый кластер |
| `bid` | integer | Текущая ставка за 1000 показов, ₽ |

### Ошибки

- `400`, `401`, `403` (`AccessDenied`), `429`

---

## 2) POST `/adv/v0/normquery/bids`

**Назначение:** установить ставки для поисковых кластеров.

### Применимость

Только для кампаний с:
- ручной ставкой
- `payment_type=cpm`

### Лимит

- `1 сек`: 2 запроса, интервал `500 мс`, всплеск 4.

### Пример

```bash
curl -X POST "https://advert-api.wildberries.ru/adv/v0/normquery/bids" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bids": [
      {"advert_id": 1825035, "nm_id": 983512347, "norm_query": "Фраза 1", "bid": 1000}
    ]
  }'
```

### Тело запроса (`V0SetNormQueryBidsRequest`)

| Поле | Тип | Обяз. | Ограничения |
|---|---|---|---|
| `bids` | array<object> | да | максимум 100 |
| `bids[].advert_id` | integer | да | ID кампании |
| `bids[].nm_id` | integer | да | Артикул WB |
| `bids[].norm_query` | string | да | Поисковый кластер |
| `bids[].bid` | integer | да | Ставка за 1000 показов, ₽ |

### Ответы

- `200` — успех (без тела).
- `400`, `401`, `403`, `429`.

---

## 3) DELETE `/adv/v0/normquery/bids`

**Назначение:** удалить ставки с поисковых кластеров.

### Применимость

Только для кампаний с:
- ручной ставкой
- `payment_type=cpm`

### Лимит

- `1 сек`: 5 запросов, интервал `200 мс`, всплеск 10.

### Пример

```bash
curl -X DELETE "https://advert-api.wildberries.ru/adv/v0/normquery/bids" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bids": [
      {"advert_id": 1825035, "nm_id": 983512347, "norm_query": "Фраза 1", "bid": 1000}
    ]
  }'
```

### Тело запроса

То же, что для `POST /adv/v0/normquery/bids`.

### Ответы

- `200` — успех (без тела).
- `400`, `401`, `403`, `429`.

---

## 4) POST `/adv/v0/normquery/get-minus`

**Назначение:** получить список минус-фраз по кампаниям и артикулам.

### Лимит

- `1 сек`: 5 запросов, интервал `200 мс`, всплеск 10.

### Пример

```bash
curl -X POST "https://advert-api.wildberries.ru/adv/v0/normquery/get-minus" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"advert_id":1825035,"nm_id":983512347}]}'
```

### Тело запроса (`V0GetNormQueryMinusRequest`)

| Поле | Тип | Обяз. | Ограничения |
|---|---|---|---|
| `items` | array<object> | да | максимум 100 |
| `items[].advert_id` | integer | да | ID кампании |
| `items[].nm_id` | integer | да | Артикул WB |

### Ответ `200`

| Поле | Тип | Описание |
|---|---|---|
| `items` | array | Список результатов |

Элемент `items[]`:

| Поле | Тип | Описание |
|---|---|---|
| `advert_id` | integer | ID кампании |
| `nm_id` | integer | Артикул WB |
| `norm_queries` | array<string> | Список минус-фраз |

### Ошибки

- `400`, `401`, `403`, `429`

---

## 5) POST `/adv/v0/normquery/set-minus`

**Назначение:** установить/обновить минус-фразы.

### Применимость

Только для кампаний с:
- ручной ставкой
- `payment_type=cpm`

### Важно

- Если отправить пустой массив `norm_queries`, будут удалены все минус-фразы.

### Лимит

- `1 сек`: 5 запросов, интервал `200 мс`, всплеск 10.

### Пример

```bash
curl -X POST "https://advert-api.wildberries.ru/adv/v0/normquery/set-minus" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "advert_id": 1825035,
    "nm_id": 983512347,
    "norm_queries": ["Фраза 1", "Фраза 2"]
  }'
```

### Тело запроса (`V0SetMinusNormQueryRequest`)

| Поле | Тип | Обяз. | Ограничения |
|---|---|---|---|
| `advert_id` | integer | да | ID кампании |
| `nm_id` | integer | да | Артикул WB |
| `norm_queries` | array<string> | да | До 1000 фраз |

### Ответы

- `200` — успех (без тела).
- `400`, `401`, `403`, `429`.

---

## 6) POST `/adv/v0/normquery/list`

**Назначение:** получить активные и неактивные (исключённые) кластеры с порогом от 100 показов.

### Лимит

- `1 сек`: 5 запросов, интервал `200 мс`, всплеск 10.

### Пример

```bash
curl -X POST "https://advert-api.wildberries.ru/adv/v0/normquery/list" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"advertId":123456789,"nmId":987654321}]}'
```

### Тело запроса (`V0GetNormQueryListRequest`)

| Поле | Тип | Обяз. | Ограничения |
|---|---|---|---|
| `items` | array<object> | да | максимум 100 |
| `items[].advertId` | int64 | да | ID кампании |
| `items[].nmId` | int64 | да | Артикул WB |

### Ответ `200`

| Поле | Тип | Описание |
|---|---|---|
| `items` | array\|null | Результаты по товарам |

Элемент `items[]`:

| Поле | Тип | Описание |
|---|---|---|
| `advertId` | int64 | ID кампании |
| `nmId` | int64 | Артикул WB |
| `normQueries.active` | array<string>\|null | Активные кластеры |
| `normQueries.excluded` | array<string>\|null | Неактивные кластеры |

### Ошибки

- `400`, `401`, `429`.
