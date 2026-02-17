# История остатков

## Общие правила раздела

- Данные обновляются 1 раз в час.
- Лимит: `3 запроса / 1 мин`, интервал `20 сек`, всплеск `3`.
- Период `currentPeriod` для этого раздела: не ранее чем за **3 месяца** от текущей даты.

## Общие фильтры и перечисления

### `stockType`

- `""` — все склады
- `wb` — склады WB
- `mp` — склады продавца

### `availabilityFilters[]`

- `deficient` — дефицит
- `actual` — актуальный
- `balanced` — баланс
- `nonActual` — неактуальный
- `nonLiquid` — неликвид
- `invalidData` — не рассчитано

### `TableOrderBy`

- `mode`: `asc` / `desc`
- `field`:
  - `ordersCount`, `ordersSum`, `avgOrders`
  - `buyoutCount`, `buyoutSum`, `buyoutPercent`
  - `stockCount`, `stockSum`
  - `saleRate`, `avgStockTurnover`
  - `toClientCount`, `fromClientCount`
  - `minPrice`, `maxPrice`
  - `officeMissingTime`
  - `lostOrdersCount`, `lostOrdersSum`
  - `lostBuyoutsCount`, `lostBuyoutsSum`

### Особые значения метрик

Для `saleRate`, `avgStockTurnover`, `officeMissingTime` возможны особые `hours`:
- `-1` — бесконечная длительность
- `-2` — нулевая длительность
- `-3` — длительность не рассчитана
- для `officeMissingTime` также `-4` — отсутствие весь период

Для `lostOrders*`/`lostBuyouts*`:
- `< 0` и не `-2` — значение не рассчитано
- `-2` — нулевое значение

---

## 1) POST `/api/v2/stocks-report/products/groups`

**Назначение:** данные по группам товаров (`subjectID + brandName + tagID`).

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/groups" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nmIDs": [111222333],
    "subjectIDs": [123],
    "brandNames": ["Brand"],
    "tagIDs": [3],
    "currentPeriod": {"start": "2026-01-01", "end": "2026-02-01"},
    "stockType": "mp",
    "skipDeletedNm": true,
    "availabilityFilters": ["deficient", "balanced"],
    "orderBy": {"field": "avgOrders", "mode": "asc"},
    "limit": 100,
    "offset": 0
  }'
```

### Параметры (`TableGroupRequestSt`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `nmIDs` | array<int64> | нет | Артикулы WB |
| `subjectIDs` | array<int32> | нет | ID предметов |
| `brandNames` | array<string> | нет | Бренды |
| `tagIDs` | array<int64> | нет | ID ярлыков |
| `currentPeriod` | object | да | Период (`start`, `end`) |
| `stockType` | enum | да | Тип складов |
| `skipDeletedNm` | boolean | да | Скрыть удалённые товары |
| `availabilityFilters` | array<enum> | да | Фильтр по доступности |
| `orderBy` | object | да | Сортировка |
| `limit` | uint32 | нет | Лимит групп, `<=1000`, default `100` |
| `offset` | uint32 | да | Смещение |

### Ответ `200`

Формат: `{"data": TableGroupResponseSt}`

`TableGroupResponseSt`:
- `groups[]` (`TableGroupItemSt`):
  - идентификация группы: `subjectID`, `subjectName`, `brandName`, `tagID`, `tagName`
  - `metrics` (`TableCommonMetrics`)
  - `items[]` — товары группы (`TableProductItemSt`)
- `currency`

`TableCommonMetrics` включает:
- заказы/выкупы: `ordersCount`, `ordersSum`, `buyoutCount`, `buyoutSum`, `buyoutPercent`
- средние и остатки: `avgOrders`, `avgOrdersByMonth[]`, `stockCount`, `stockSum`
- оборачиваемость: `saleRate`, `avgStockTurnover`
- логистика: `toClientCount`, `fromClientCount`, `officeMissingTime`
- упущенные: `lostOrdersCount`, `lostOrdersSum`, `lostBuyoutsCount`, `lostBuyoutsSum`

### Ошибки

- `400`, `401`, `403`, `429`

---

## 2) POST `/api/v2/stocks-report/products/products`

**Назначение:** данные по товарам.

Можно запрашивать:
- по конкретным фильтрам;
- весь отчёт, если не переданы `nmIDs`, `subjectID`, `brandName`, `tagID`.

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/products" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "currentPeriod": {"start": "2026-01-01", "end": "2026-02-01"},
    "stockType": "wb",
    "skipDeletedNm": false,
    "orderBy": {"field": "ordersCount", "mode": "desc"},
    "availabilityFilters": ["actual"],
    "limit": 100,
    "offset": 0
  }'
```

### Параметры (`TableProductRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `nmIDs` | array<int64> | нет | Артикулы WB |
| `subjectID` | int32 | нет | ID предмета |
| `brandName` | string | нет | Бренд |
| `tagID` | int64 | нет | ID ярлыка |
| `currentPeriod` | object | да | Период |
| `stockType` | enum | да | Тип складов |
| `skipDeletedNm` | boolean | да | Скрыть удалённые товары |
| `orderBy` | object | да | Сортировка |
| `availabilityFilters` | array<enum> | да | Доступность |
| `limit` | uint32 | нет | Лимит товаров, `<=1000`, default `100` |
| `offset` | uint32 | да | Смещение |

### Ответ `200`

Формат: `{"data": TableProductResponse}` (в схеме верхний объект помечен как `nullable: true`).

`TableProductResponse`:
- `items[]` (`TableProductItemSt`):
  - карточка: `nmID`, `isDeleted`, `subjectName`, `name`, `vendorCode`, `brandName`, `mainPhoto`, `hasSizes`
  - `metrics`:
    - `TableCommonMetrics`
    - `currentPrice.minPrice`, `currentPrice.maxPrice`
    - `availability`
- `currency`

### Ошибки

- `400`, `401`, `403`, `429`

---

## 3) POST `/api/v2/stocks-report/products/sizes`

**Назначение:** данные по размерам товара.

### Логика ответа (важно)

1. Товар с размерами + `includeOffice=true`:
   - `sizes[]` с детализацией по складам в каждом размере.
2. Товар с размерами + `includeOffice=false`:
   - `sizes[]` без детализации по складам.
3. Товар без размеров + `includeOffice=true`:
   - детализация только по складам.
4. Товар без размеров + `includeOffice=false`:
   - тело ответа пустое.

Товар считается неразмерным, если единственный размер имеет `techSize="0"` (в товарном отчёте у него `hasSizes=false`).

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/sizes" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nmID": 123456789,
    "currentPeriod": {"start": "2026-01-01", "end": "2026-02-01"},
    "stockType": "mp",
    "orderBy": {"field": "stockCount", "mode": "desc"},
    "includeOffice": true
  }'
```

### Параметры (`TableSizeRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `nmID` | int64 | да | Артикул WB |
| `currentPeriod` | object | да | Период |
| `stockType` | enum | да | Тип складов |
| `orderBy` | object | да | Сортировка |
| `includeOffice` | boolean | да | Включить детализацию по складам |

### Ответ `200`

Формат: `{"data": TableSizeResponse}`

`TableSizeResponse`:
- `offices[]` (`TableOfficeItem`) — данные по складам
- `sizes[]`:
  - `name`, `chrtID`
  - `offices[]` (если включена детализация)
  - `metrics` = `TableCommonMetrics` + `currentPrice`
- `currency`

Агрегированные данные по складам продавца приходят как:
- `regionName: "Маркетплейс"`
- `officeName: ""`

### Ошибки

- `400`, `401`, `403`, `429`

---

## 4) POST `/api/v2/stocks-report/offices`

**Назначение:** данные по складам и регионам отгрузки.

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/stocks-report/offices" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "currentPeriod": {"start": "2026-01-01", "end": "2026-02-01"},
    "stockType": "",
    "skipDeletedNm": false,
    "nmIDs": [111222333],
    "subjectIDs": [123],
    "brandNames": ["Brand"],
    "tagIDs": [3]
  }'
```

### Параметры (`TableShippingOfficeRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `nmIDs` | array<int64> | нет | Артикулы WB |
| `subjectIDs` | array<int32> | нет | ID предметов |
| `brandNames` | array<string> | нет | Бренды |
| `tagIDs` | array<int64> | нет | Ярлыки |
| `currentPeriod` | object | да | Период |
| `stockType` | enum | да | Тип складов |
| `skipDeletedNm` | boolean | да | Скрыть удалённые товары |

### Ответ `200`

Формат: `{"data": TableShippingOfficeResponse}`

`TableShippingOfficeResponse`:
- `regions[]`:
  - `regionName`
  - `metrics` (`stockCount`, `stockSum`, `saleRate`, `toClientCount`, `fromClientCount`)
  - `offices[]`:
    - `officeID`, `officeName`
    - `metrics` (те же 5 метрик)
- `currency`

Для данных по складам продавца без детализации:
- `regionName: "Маркетплейс"`
- `offices: []`

### Ошибки

- `400`, `401`, `403`, `429`
