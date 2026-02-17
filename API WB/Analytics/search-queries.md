# Поисковые запросы по вашим товарам

## Общие правила раздела

- Данные обновляются 1 раз в час.
- Лимит: `3 запроса / 1 мин`, интервал `20 сек`, всплеск `3`.
- Пара `includeSubstitutedSKUs` и `includeSearchTexts` не может одновременно быть `false`.

## Общие объекты периода

| Объект | Обязательные поля | Ограничения |
|---|---|---|
| `Period` | `start`, `end` | `start <= end`, даты не старше 365 суток от текущей даты |
| `pastPeriod` | `start`, `end` | длина периода `<= currentPeriod`, `end` должен быть раньше `currentPeriod.start` |
| `PeriodOrdersRequest` | `start`, `end` | максимум 7 суток |

## Общие перечисления

- `positionCluster`: `all`, `firstHundred`, `secondHundred`, `below`
- сортировка `mode`: `asc`, `desc`

---

## 1) POST `/api/v2/search-report/report`

**Назначение:** основная страница отчёта (общие метрики, позиции, видимость, таблица групп).

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/search-report/report" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "currentPeriod": {"start": "2026-02-10", "end": "2026-02-16"},
    "pastPeriod": {"start": "2026-02-03", "end": "2026-02-09"},
    "nmIds": [162579635],
    "subjectIds": [64],
    "brandNames": ["Nike"],
    "tagIds": [32],
    "positionCluster": "all",
    "orderBy": {"field": "avgPosition", "mode": "asc"},
    "includeSubstitutedSKUs": true,
    "includeSearchTexts": true,
    "limit": 100,
    "offset": 0
  }'
```

### Параметры (`MainRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `currentPeriod` | object | да | Текущий период |
| `pastPeriod` | object | нет | Прошлый период для сравнения |
| `nmIds` | array<int32> | нет | Фильтр по артикулам |
| `subjectIds` | array<int32> | нет | Фильтр по предметам |
| `brandNames` | array<string> | нет | Фильтр по брендам |
| `tagIds` | array<int64> | нет | Фильтр по ярлыкам |
| `positionCluster` | enum | да | Кластер позиций |
| `orderBy` | object | да | Сортировка (`field`, `mode`) |
| `includeSubstitutedSKUs` | boolean | нет | Включать данные с подменным артикулом |
| `includeSearchTexts` | boolean | нет | Включать данные без подменного артикула |
| `limit` | uint32 | да | Кол-во групп, `<=1000` |
| `offset` | uint32 | да | Смещение |

`orderBy.field` для main/details: `avgPosition`, `openCard`, `addToCart`, `openToCart`, `orders`, `cartToOrder`, `visibility`, `minPrice`, `maxPrice`.

### Ответ `200`

Формат: `{"data": MainResponse}`

`MainResponse`:
- `commonInfo`:
  - `supplierRating` (`current`, `dynamics`)
  - `advertisedProducts` (`current`, `dynamics`)
  - `totalProducts`
- `positionInfo`:
  - `average`, `median` (`current`, `dynamics`)
  - `chartItems[]` (`dt`, `average`, `median`)
  - `clusters` (`firstHundred`, `secondHundred`, `below`)
- `visibilityInfo`:
  - `visibility`, `openCard` (`current`, `dynamics`)
  - графики `byDay[]`, `byWeek[]`, `byMonth[]` (`dt`, `visibility`, `open`)
- `groups[]` — группы (`subjectName`, `subjectId`, `brandName`, `tagName`, `tagId`, `metrics`, `items[]`)
- `currency`

### Ошибки

- `400` (`ErrorObject400`)
- `401`
- `403` (`ErrorObject403`)
- `429`

---

## 2) POST `/api/v2/search-report/table/groups`

**Назначение:** пагинация по группам для основной страницы.

### Важно

Пагинация по группам работает только если есть фильтр по `brandNames` и/или `subjectIds` и/или `tagIds`.

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/search-report/table/groups" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "currentPeriod": {"start": "2026-02-10", "end": "2026-02-16"},
    "subjectIds": [64, 334],
    "brandNames": ["nikkle", "abikas"],
    "tagIds": [32, 53],
    "orderBy": {"field": "avgPosition", "mode": "asc"},
    "positionCluster": "all",
    "includeSubstitutedSKUs": true,
    "includeSearchTexts": true,
    "limit": 100,
    "offset": 0
  }'
```

### Параметры (`TableGroupRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `currentPeriod` | object | да | Текущий период |
| `pastPeriod` | object | нет | Прошлый период |
| `nmIds` | array<int32> | нет | Артикулы |
| `subjectIds` | array<int32> | нет | Предметы |
| `brandNames` | array<string> | нет | Бренды |
| `tagIds` | array<int64> | нет | Ярлыки |
| `orderBy` | object | да | Сортировка (`OrderByGrTe`) |
| `positionCluster` | enum | да | Кластер позиций |
| `includeSubstitutedSKUs` | boolean | нет | Данные с подменным артикулом |
| `includeSearchTexts` | boolean | нет | Данные без подменного артикула |
| `limit` | uint32 | да | Кол-во групп, `<=1000` |
| `offset` | uint32 | да | Смещение |

`OrderByGrTe.field`: `avgPosition`, `openCard`, `addToCart`, `openToCart`, `orders`, `cartToOrder`, `visibility`.

### Ответ `200`

Формат: `{"data": TableGroupResponse}`

`TableGroupResponse`:
- `groups[]` — элементы типа `TableGroupItem`
  - группа: `subjectName`, `subjectId`, `brandName`, `tagName`, `tagId`
  - `metrics`: `avgPosition`, `openCard`, `addToCart`, `openToCart`, `orders`, `cartToOrder`, `visibility` (каждая метрика: `current`, `dynamics`)
  - `items[]`: товары группы (`TableProductItem`)
- `currency`

### Ошибки

- `400`, `401`, `403`, `429`

---

## 3) POST `/api/v2/search-report/table/details`

**Назначение:** пагинация по товарам внутри группы.

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/search-report/table/details" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "currentPeriod": {"start": "2026-02-10", "end": "2026-02-16"},
    "subjectId": 123,
    "brandName": "Apple",
    "tagId": 45,
    "nmIds": [162579635, 166699779],
    "orderBy": {"field": "orders", "mode": "desc"},
    "positionCluster": "all",
    "includeSubstitutedSKUs": true,
    "includeSearchTexts": true,
    "limit": 150,
    "offset": 0
  }'
```

### Параметры (`TableDetailsRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `currentPeriod` | object | да | Текущий период |
| `pastPeriod` | object | нет | Прошлый период |
| `subjectId` | int32 | нет | ID предмета (фильтр группы) |
| `brandName` | string | нет | Бренд (фильтр группы) |
| `tagId` | int64 | нет | ID ярлыка (фильтр группы) |
| `nmIds` | array<uint64> | нет | Фильтр по товарам, максимум `50` |
| `orderBy` | object | да | Сортировка (`OrderByMainAndDetails`) |
| `positionCluster` | enum | да | Кластер позиций |
| `includeSubstitutedSKUs` | boolean | нет | Данные с подменным артикулом |
| `includeSearchTexts` | boolean | нет | Данные без подменного артикула |
| `limit` | uint32 | да | Кол-во товаров, `<=1000` |
| `offset` | uint32 | да | Смещение |

### Ответ `200`

Формат: `{"data": TableDetailsResponse}`

`TableDetailsResponse`:
- `products[]` (`TableProductItem`):
  - идентификация: `nmId`, `name`, `vendorCode`, `subjectName`, `brandName`, `mainPhoto`
  - признаки: `isAdvertised`, `isSubstitutedSKU`, `isCardRated`
  - рейтинг/цены: `rating`, `feedbackRating`, `price.minPrice`, `price.maxPrice`
  - метрики: `avgPosition`, `openCard`, `addToCart`, `openToCart`, `orders`, `cartToOrder`, `visibility` (каждая: `current`, `dynamics`)
- `currency`

### Ошибки

- `400`, `401`, `403`, `429`

---

## 4) POST `/api/v2/search-report/product/search-texts`

**Назначение:** топ поисковых запросов по товару.

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/search-report/product/search-texts" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "currentPeriod": {"start": "2026-02-10", "end": "2026-02-16"},
    "pastPeriod": {"start": "2026-02-03", "end": "2026-02-09"},
    "nmIds": [162579635],
    "topOrderBy": "openCard",
    "includeSubstitutedSKUs": true,
    "includeSearchTexts": true,
    "orderBy": {"field": "avgPosition", "mode": "asc"},
    "limit": 30
  }'
```

### Параметры (`ProductSearchTextsRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `currentPeriod` | object | да | Текущий период |
| `pastPeriod` | object | нет | Прошлый период |
| `nmIds` | array<uint64> | да | Артикулы, максимум `50` |
| `topOrderBy` | enum | да | Критерий топа: `openCard`, `addToCart`, `openToCart`, `orders`, `cartToOrder` |
| `includeSubstitutedSKUs` | boolean | нет | Данные с подменным артикулом |
| `includeSearchTexts` | boolean | нет | Данные без подменного артикула |
| `orderBy` | object | да | Сортировка (`OrderByGrTe`) |
| `limit` | integer | да | Лимит текста запроса: стандартный тариф `1..30`, продвинутый `1..100` |

### Ответ `200`

Формат: `{"data": ProductSearchTextsResponse}`

`ProductSearchTextsResponse`:
- `items[]` (`TableSearchTextItem`):
  - идентификация: `text`, `nmId`, `subjectName`, `brandName`, `vendorCode`, `name`
  - рейтинг/цены: `isCardRated`, `rating`, `feedbackRating`, `price.minPrice`, `price.maxPrice`
  - частота: `frequency` (`current`, `dynamics`), `weekFrequency`
  - позиции: `medianPosition`, `avgPosition` (`current`, `dynamics`)
  - воронка поиска:
    - `openCard`, `addToCart`, `openToCart`, `orders`, `cartToOrder` (для каждой есть `current`, `dynamics`, `percentile`)
  - `visibility` (`current`, `dynamics`)
- `currency`

### Ошибки

- `400`, `401`, `403`, `429`

---

## 5) POST `/api/v2/search-report/product/orders`

**Назначение:** таблица заказов и позиций по текстам запросов для выбранного товара.

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/search-report/product/orders" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "period": {"start": "2026-02-10", "end": "2026-02-16"},
    "nmId": 211131895,
    "searchTexts": ["костюм", "пиджак"]
  }'
```

### Параметры (`ProductOrdersRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `period` | object | да | Период, максимум 7 суток |
| `nmId` | uint64 | да | Артикул WB |
| `searchTexts` | array<string> | да | Тексты запросов; в схеме `1..30` |

Примечание по документации: в описании указано «для тарифа Продвинутый максимум 100», но в схеме OpenAPI стоит `maxItems: 30`.

### Ответ `200`

Формат: `{"data": ProductOrdersResponse}`

`ProductOrdersResponse`:
- `total[]` — итоговые метрики (по датам):
  - `dt`, `avgPosition`, `orders`
- `items[]`:
  - `text`
  - `frequency`
  - `dateItems[]` (`dt`, `avgPosition`, `orders`)

### Ошибки

- `400`, `401`, `403`, `429`

---

## Структура ошибок

### `400` (`ErrorObject400`)

- `title`
- `detail`
- `requestId`
- `origin`

### `403` (`ErrorObject403`)

- `title`
- `detail`
- `requestId`
- `origin`

### `401` и `429`

Стандартные объекты ошибок WB (`application/problem+json`).
