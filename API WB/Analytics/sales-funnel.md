# Воронка продаж

## Общие особенности

- Метрики отчётов обновляются 1 раз в час.
- Большая часть событий (переходы, корзина, заказы) появляется в течение часа, часть данных может дозаписываться несколько дней.
- Выкупы/отмены/возвраты относятся к дате заказа, а не к фактической дате выкупа/возврата.
- Лимит: `3 запроса / 1 мин`, интервал `20 сек`, всплеск `3`.

---

## 1) POST `/api/analytics/v3/sales-funnel/products`

**Назначение:** статистика карточек товаров за период + сравнение с прошлым периодом.

### Пример запроса (curl)

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/analytics/v3/sales-funnel/products" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "selectedPeriod": {"start": "2025-12-01", "end": "2025-12-31"},
    "pastPeriod": {"start": "2025-11-01", "end": "2025-11-30"},
    "nmIds": [162579635],
    "brandNames": ["Nike"],
    "subjectIds": [64],
    "tagIds": [32],
    "skipDeletedNm": false,
    "orderBy": {"field": "openCard", "mode": "desc"},
    "limit": 100,
    "offset": 0
  }'
```

### Параметры тела запроса (`ProductsRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `selectedPeriod` | object | да | Запрашиваемый период (`start`, `end`) |
| `pastPeriod` | object | нет | Период для сравнения |
| `nmIds` | array<uint64> | нет | Фильтр по артикулам WB, `0..1000` элементов |
| `brandNames` | array<string> | нет | Фильтр по брендам |
| `subjectIds` | array<uint64> | нет | Фильтр по ID предметов |
| `tagIds` | array<uint64> | нет | Фильтр по ID ярлыков |
| `skipDeletedNm` | boolean | нет | Скрыть удалённые карточки |
| `orderBy` | object | нет | Сортировка (см. поля ниже) |
| `limit` | uint32 | нет | Лимит карточек в ответе, `<=1000`, default `50` |
| `offset` | uint32 | нет | Смещение, default `0` |

### `orderBy` (если передаёте)

| Поле | Тип | Обяз. | Допустимые значения |
|---|---|---|---|
| `field` | string | да | `openCard`, `addToCart`, `orderCount`, `orderSum`, `buyoutCount`, `buyoutSum`, `cancelCount`, `cancelSum`, `avgPrice`, `stockMpQty`, `stockWbQty`, `shareOrderPercent`, `addToWishlist`, `timeToReady`, `localizationPercent`, `wbClub.orderCount`, `wbClub.orderSum`, `wbClub.buyoutSum`, `wbClub.cancelSum`, `wbClub.buyoutCount`, `wbClub.avgPrice`, `wbClub.buyoutPercent`, `wbClub.avgOrderCountPerDay`, `wbClub.cancelCount` |
| `mode` | string | да | `asc`, `desc` |

### Правила и ограничения

- Можно получить отчёт максимум за последние **365 дней**.
- Фильтры `brandNames`, `subjectIds`, `tagIds`, `nmIds` могут быть пустыми массивами `[]` — тогда берутся все карточки.
- Если указано несколько фильтров, применяется пересечение (карточка должна подходить одновременно всем фильтрам).
- Если `pastPeriod.start` уходит дальше чем на 365 дней назад, сервер корректирует его до `текущая дата - 365 дней`.

### Ответ `200`

Формат: `{"data": ProductsResponse}`

`ProductsResponse`:
- `products[]`:
  - `product`:
    - `nmId`, `title`, `vendorCode`, `brandName`, `subjectId`, `subjectName`
    - `tags[]` (`id`, `name`)
    - `productRating`, `feedbackRating`
    - `stocks` (`wb`, `mp`, `balanceSum`)
  - `statistic`:
    - `selected` (метрики текущего периода)
    - `past` (метрики прошлого периода, если передан)
    - `comparison` (динамика)
- `currency` (например, `RUB`)

Ключевые метрики периода (`selected`/`past`):
- `openCount`, `cartCount`, `orderCount`, `orderSum`, `buyoutCount`, `buyoutSum`, `cancelCount`, `cancelSum`
- `avgPrice`, `avgOrdersCountPerDay`, `shareOrderPercent`, `addToWishlist`
- `timeToReady` (`days`, `hours`, `mins`)
- `localizationPercent`
- `wbClub` (заказы/выкупы/суммы/средние)
- `conversions` (`addToCartPercent`, `cartToOrderPercent`, `buyoutPercent`)

`comparison` содержит те же показатели в формате динамики (`...Dynamic`, в процентах/дельтах по документации).

### Ошибки

- `400` — неверное тело/параметры
- `401` — неавторизован
- `403` — нет доступа
- `429` — превышен лимит

---

## 2) POST `/api/analytics/v3/sales-funnel/products/history`

**Назначение:** статистика карточек по дням/неделям (история), максимум за последнюю неделю.

### Пример запроса (curl)

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/analytics/v3/sales-funnel/products/history" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "selectedPeriod": {"start": "2026-02-10", "end": "2026-02-16"},
    "nmIds": [162579635, 166699779],
    "skipDeletedNm": true,
    "aggregationLevel": "day"
  }'
```

### Параметры тела (`ProductHistoryRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `selectedPeriod` | object | да | Период (`start`, `end`) |
| `nmIds` | array<uint64> | да | Список артикулов WB, `1..20` элементов |
| `skipDeletedNm` | boolean | нет | Скрыть удалённые карточки |
| `aggregationLevel` | string | нет | `day` или `week`, default `day` |

### Ограничения

- Период запроса — максимум **последняя неделя**.

### Ответ `200`

Формат: `ProductHistoryResponse` (массив)

Элемент массива:
- `product`: `nmId`, `title`, `vendorCode`, `brandName`, `subjectId`, `subjectName`
- `history[]` (по датам/неделям):
  - `date`
  - `openCount`, `cartCount`, `orderCount`, `orderSum`
  - `buyoutCount`, `buyoutSum`, `buyoutPercent`
  - `addToCartConversion`, `cartToOrderConversion`
  - `addToWishlistCount`
- `currency`

### Ошибки

- `400`, `401`, `403`, `429`

---

## 3) POST `/api/analytics/v3/sales-funnel/grouped/history`

**Назначение:** статистика по дням/неделям для групп карточек (по предметам, брендам, ярлыкам).

### Пример запроса (curl)

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/analytics/v3/sales-funnel/grouped/history" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "selectedPeriod": {"start": "2026-02-10", "end": "2026-02-16"},
    "subjectIds": [64, 334],
    "brandNames": ["Nike", "Adidas"],
    "tagIds": [32, 53],
    "skipDeletedNm": false,
    "aggregationLevel": "week"
  }'
```

### Параметры тела (`GroupedHistoryRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `selectedPeriod` | object | да | Период (`start`, `end`) |
| `brandNames` | array<string> | нет | Фильтр по брендам |
| `subjectIds` | array<uint64> | нет | Фильтр по предметам |
| `tagIds` | array<uint64> | нет | Фильтр по ярлыкам |
| `skipDeletedNm` | boolean | нет | Скрыть удалённые карточки |
| `aggregationLevel` | string | нет | `day` или `week`, default `day` |

### Ограничения

- Период — максимум **последняя неделя**.
- `brandNames`, `subjectIds`, `tagIds` могут быть пустыми `[]`.
- Ограничение комбинаций фильтров: произведение количества значений предметов, брендов и ярлыков должно быть `<= 16`.

### Ответ `200`

Формат: `{"data": GroupedHistoryResponse}`

`GroupedHistoryResponse` (массив):
- `product`: `nmId`, `title`, `vendorCode`, `brandName`, `subjectId`, `subjectName`
- `history[]` с метриками (`date`, `openCount`, `cartCount`, `orderCount`, `orderSum`, `buyoutCount`, `buyoutSum`, `buyoutPercent`, `addToCartConversion`, `cartToOrderConversion`, `addToWishlistCount`)
- `currency`

### Ошибки

- `400`, `401`, `403`, `429`

---

## Общие форматы периодов для воронки

| Объект | Поля | Ограничения |
|---|---|---|
| `DatePeriod` | `start`, `end` | строки дат `YYYY-MM-DD` |
| `selectedPeriod` | `start`, `end` | обязателен |
| `pastPeriod` | `start`, `end` | опционален, для сравнения |
