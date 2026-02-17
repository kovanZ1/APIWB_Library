# Аналитика продавца CSV

## Общие правила

- Базовый URL: `https://seller-analytics-api.wildberries.ru`
- Авторизация: `Authorization`
- Лимит: `3 запроса / 1 мин`, интервал `20 сек`, всплеск `3`
- Для `STOCK_HISTORY_REPORT_CSV` подписка Джем не требуется.

---

## 1) POST `/api/v2/nm-report/downloads`

**Назначение:** создать задачу на генерацию CSV-отчёта.

### Пример запроса (общий)

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "06eae887-9d9f-491f-b16a-bb1766fcb8d2",
    "reportType": "DETAIL_HISTORY_REPORT",
    "userReportName": "Card report",
    "params": {
      "nmIDs": [1234567],
      "startDate": "2026-01-01",
      "endDate": "2026-01-31"
    }
  }'
```

### Базовые поля запроса

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | uuid | да | ID отчёта, генерируется на стороне клиента |
| `reportType` | string | да | Тип отчёта (см. ниже) |
| `userReportName` | string | нет | Имя отчёта (если не задано, генерируется автоматически) |
| `params` | object | да | Параметры, зависят от `reportType` |

### Поддерживаемые `reportType`

1. `DETAIL_HISTORY_REPORT` — воронка продаж по артикулам WB
2. `GROUPED_HISTORY_REPORT` — воронка продаж по группам (предмет/бренд/ярлык)
3. `SEARCH_QUERIES_PREMIUM_REPORT_GROUP` — поиск по группам
4. `SEARCH_QUERIES_PREMIUM_REPORT_PRODUCT` — поиск по товарам
5. `SEARCH_QUERIES_PREMIUM_REPORT_TEXT` — поиск по текстам запросов
6. `STOCK_HISTORY_REPORT_CSV` — история остатков

### Важно

`includeSubstitutedSKUs` и `includeSearchTexts` не могут одновременно быть `false`.

### `params` для каждого `reportType`

#### A. `DETAIL_HISTORY_REPORT` (`SalesFunnelProductReq`)

Обязательные:
- `startDate`, `endDate`

Опциональные:
- `nmIDs` (`0..1000`)
- `subjectIds`, `brandNames`, `tagIds`
- `timezone` (default `Europe/Moscow`)
- `aggregationLevel`: `day`, `week`, `month`
- `skipDeletedNm`

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `nmIDs` | array<int64> | нет | Артикулы WB, `0..1000` |
| `subjectIds` | array<int32> | нет | ID предметов |
| `brandNames` | array<string> | нет | Бренды |
| `tagIds` | array<int64> | нет | ID ярлыков |
| `startDate` | date | да | Начало периода |
| `endDate` | date | да | Конец периода |
| `timezone` | string | нет | Часовой пояс, default `Europe/Moscow` |
| `aggregationLevel` | enum | нет | `day`, `week`, `month` |
| `skipDeletedNm` | boolean | нет | Скрыть удалённые карточки |

#### B. `GROUPED_HISTORY_REPORT` (`SalesFunnelGroupReq`)

Обязательные:
- `startDate`, `endDate`

Опциональные:
- `subjectIds`, `brandNames`, `tagIds`
- `timezone`
- `aggregationLevel`: `day`, `week`, `month`
- `skipDeletedNm`

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `subjectIds` | array<int32> | нет | ID предметов |
| `brandNames` | array<string> | нет | Бренды |
| `tagIds` | array<int64> | нет | ID ярлыков |
| `startDate` | date | да | Начало периода |
| `endDate` | date | да | Конец периода |
| `timezone` | string | нет | Часовой пояс |
| `aggregationLevel` | enum | нет | `day`, `week`, `month` |
| `skipDeletedNm` | boolean | нет | Скрыть удалённые `nmID` |

#### C. `SEARCH_QUERIES_PREMIUM_REPORT_GROUP` (`SearchReportGroupReq`)

Обязательные:
- `currentPeriod`
- `subjectIds`
- `orderBy` (`field`, `mode`)
- `positionCluster`

Опциональные:
- `pastPeriod`
- `nmIds` (`0..1000`)
- `brandNames`, `tagIds`
- `includeSubstitutedSKUs`, `includeSearchTexts`

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `currentPeriod` | object | да | Текущий период (`start`, `end`) |
| `pastPeriod` | object | нет | Период сравнения |
| `nmIds` | array<int64> | нет | Артикулы WB, `0..1000` |
| `subjectIds` | array<int32> | да | ID предметов (может быть пустым для всех предметов) |
| `brandNames` | array<string> | нет | Бренды |
| `tagIds` | array<int64> | нет | ID ярлыков |
| `orderBy` | object | да | Сортировка (`field`, `mode`) |
| `positionCluster` | enum | да | `all`, `firstHundred`, `secondHundred`, `below` |
| `includeSubstitutedSKUs` | boolean | нет | Включать подменный артикул |
| `includeSearchTexts` | boolean | нет | Включать поисковые тексты |

#### D. `SEARCH_QUERIES_PREMIUM_REPORT_PRODUCT` (`SearchReportProductReq`)

Обязательные:
- `currentPeriod`
- `orderBy`
- `positionCluster`

Опциональные:
- `pastPeriod`
- `subjectId` (`0` = все предметы)
- `brandName`
- `tagId` (`0` = все ярлыки)
- `nmIds` (`0..1000`)
- `includeSubstitutedSKUs`, `includeSearchTexts`

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `currentPeriod` | object | да | Текущий период (`start`, `end`) |
| `pastPeriod` | object | нет | Период сравнения |
| `subjectId` | int32 | нет | ID предмета (`0` = все предметы) |
| `brandName` | string | нет | Бренд |
| `tagId` | int64 | нет | ID ярлыка (`0` = все ярлыки) |
| `nmIds` | array<int64> | нет | Артикулы WB, `0..1000` |
| `positionCluster` | enum | да | `all`, `firstHundred`, `secondHundred`, `below` |
| `orderBy` | object | да | Сортировка (`field`, `mode`) |
| `includeSubstitutedSKUs` | boolean | нет | Включать подменный артикул |
| `includeSearchTexts` | boolean | нет | Включать поисковые тексты |

#### E. `SEARCH_QUERIES_PREMIUM_REPORT_TEXT` (`SearchReportTextReq`)

Обязательные:
- `currentPeriod`
- `limit` (стандарт: `1..30`, продвинутый: `1..100`)
- `topOrderBy` (`openCard`, `addToCart`, `openToCart`, `orders`, `cartToOrder`)
- `orderBy`

Опциональные:
- `pastPeriod`
- `nmIds` (`0..1000`)
- `subjectIds`, `brandNames`, `tagIds`
- `includeSubstitutedSKUs`, `includeSearchTexts`

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `currentPeriod` | object | да | Текущий период (`start`, `end`) |
| `pastPeriod` | object | нет | Период сравнения |
| `nmIds` | array<int64> | нет | Артикулы WB, `0..1000` |
| `subjectIds` | array<int32> | нет | ID предметов |
| `brandNames` | array<string> | нет | Бренды |
| `tagIds` | array<int64> | нет | ID ярлыков |
| `topOrderBy` | enum | да | `openCard`, `addToCart`, `openToCart`, `orders`, `cartToOrder` |
| `orderBy` | object | да | Сортировка (`field`, `mode`) |
| `includeSubstitutedSKUs` | boolean | нет | Включать подменный артикул |
| `includeSearchTexts` | boolean | нет | Включать поисковые тексты |
| `limit` | integer | да | Стандартный тариф `1..30`, продвинутый `1..100` |

#### F. `STOCK_HISTORY_REPORT_CSV` (`StocksReportReq`)

`params` = `CommonReportFilters`

Обязательные:
- `availabilityFilters`
- `currentPeriod`
- `stockType` (`""`, `wb`, `mp`)
- `skipDeletedNm`
- `orderBy` (`field`, `mode`)

Опциональные:
- `nmIDs`, `subjectIDs`, `brandNames`, `tagIDs`

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `nmIDs` | array<int64> | нет | Артикулы WB |
| `subjectIDs` | array<int32> | нет | ID предметов |
| `brandNames` | array<string> | нет | Бренды |
| `tagIDs` | array<int64> | нет | ID ярлыков |
| `currentPeriod` | object | да | Период (`start`, `end`) |
| `stockType` | enum | да | `\"\"`, `wb`, `mp` |
| `skipDeletedNm` | boolean | да | Скрыть удалённые товары |
| `availabilityFilters` | array<enum> | да | Доступность товара |
| `orderBy` | object | да | Сортировка (`field`, `mode`) |

### Ответ `200`

```json
{
  "data": "Created"
}
```

### Ошибки

- `400`: `title`, `detail`, `requestId`, `origin`
- `401`: стандартная ошибка авторизации WB
- `403`: `title`, `detail`, `requestId`, `origin`
- `429`: два формата
  - расширенный (`title`, `detail`, `code`, `requestId`, `origin`, `status`, `statusText`, `timestamp`)
  - упрощённый дневной лимит (`title`, `detail`, `requestId`, `origin`)

Примечание: в примере дневного ограничения указано «максимум 20». Это значение зависит от действующих ограничений аккаунта.

---

## 2) GET `/api/v2/nm-report/downloads`

**Назначение:** получить список отчётов и их статусы.

### Пример запроса

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "filter[downloadIds]=06eae887-9d9f-491f-b16a-bb1766fcb8d2"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `filter[downloadIds]` | array<uuid> | нет | Фильтр по ID отчётов |

### Ответ `200`

`NmReportGetReportsResponse`:
- `data[]`:
  - `id` (uuid)
  - `status` (`WAITING`, `PROCESSING`, `SUCCESS`, `RETRY`, `FAILED`)
  - `name`
  - `size` (байты)
  - `startDate`, `endDate`
  - `createdAt` (дата/время завершения генерации)

### Ошибки

- `400`, `401`, `403`, `429`

---

## 3) POST `/api/v2/nm-report/downloads/retry`

**Назначение:** запустить повторную генерацию отчёта (обычно для статуса `FAILED`).

### Пример запроса

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads/retry" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "downloadId": "06eea887-9d9f-491f-b16a-bb1766fcb8d2"
  }'
```

### Тело запроса (`NmReportRetryReportRequest`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `downloadId` | uuid | фактически да | ID отчёта для перегенерации |

Примечание: `requestBody` обязателен, но в схеме `downloadId` не помечен как `required`. Практически без `downloadId` запрос невалиден.

### Ответ `200`

```json
{
  "data": "Retry"
}
```

### Ошибки

- `400`, `401`, `403`, `429`

---

## 4) GET `/api/v2/nm-report/downloads/file/{downloadId}`

**Назначение:** скачать готовый отчёт в ZIP (внутри CSV).

- Отчёт доступен, если был сгенерирован за последние **48 часов**.

### Пример запроса

```bash
curl -L "https://seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads/file/06eae887-9d9f-491f-b16a-bb1766fcb8d2" \
  -H "Authorization: $WB_API_TOKEN" \
  -o analytics_report.zip
```

### Path-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `downloadId` | uuid | да | ID отчёта |

### Ответ `200`

- `Content-Type: application/zip`
- Тело: бинарный ZIP-архив с CSV

### Поля CSV по типам отчётов

#### A. Воронка продаж (`DETAIL_HISTORY_REPORT` / `GROUPED_HISTORY_REPORT`)

Поля:
- `nmID` (только для `DETAIL_HISTORY_REPORT`)
- `dt`
- `openCardCount`
- `addToCartCount`
- `ordersCount`
- `ordersSumRub`
- `buyoutsCount`
- `buyoutsSumRub`
- `cancelCount`
- `cancelSumRub`
- `addToCartConversion`
- `cartToOrderConversion`
- `buyoutPercent`
- `addToWishlist`
- `currency`

#### B. Поиск по группам (`SEARCH_QUERIES_PREMIUM_REPORT_GROUP`)

Поля:
- `SubjectName`, `SubjectID`, `BrandName`, `TagID`
- `AveragePosition`, `OpenCard`, `AddToCart`, `OpenToCart`, `Orders`, `CartToOrder`, `Visibility`
- поля прошлого периода: `AveragePositionPast`, `OpenCardPast`, `AddToCartPast`, `OpenToCartPast`, `OrdersPast`, `CartToOrderPast`, `VisibilityPast`

#### C. Поиск по товарам (`SEARCH_QUERIES_PREMIUM_REPORT_PRODUCT`)

Поля:
- идентификация: `NmID`, `VendorCode`, `Name`, `SubjectName`, `BrandName`
- карточка: `IsAdvertised`, `IsRated`, `Rating`, `FeedbackRating`
- цены: `MinPrice`, `MaxPrice`
- метрики поиска текущего периода: `AveragePosition`, `OpenCard`, `AddToCart`, `OpenToCart`, `Orders`, `CartToOrder`, `Visibility`
- метрики прошлого периода: `AveragePositionPast`, `OpenCardPast`, `AddToCartPast`, `OpenToCartPast`, `OrdersPast`, `CartToOrderPast`, `VisibilityPast`
- `IsSubstitutedSKU`
- `Currency`

#### D. Поиск по текстам (`SEARCH_QUERIES_PREMIUM_REPORT_TEXT`)

Поля:
- идентификация: `Text`, `NmID`, `SubjectName`, `BrandName`, `VendorCode`, `Name`
- карточка/цена: `Rating`, `FeedbackRating`, `MinPrice`, `MaxPrice`
- частотность/позиции: `Frequency`, `MedianPosition`, `AveragePosition`
- текущий период: `OpenCard`, `OpenCardPercentile`, `AddToCart`, `AddToCartPercentile`, `OpenToCart`, `OpenToCartPercentile`, `Orders`, `OrdersPercentile`, `CartToOrder`, `CartToOrderPercentile`, `Visibility`
- прошлый период: `FrequencyPast`, `MedianPositionPast`, `AveragePositionPast`, `OpenCardPast`, `AddToCartPast`, `OpenToCartPast`, `OrdersPast`, `CartToOrderPast`, `VisibilityPast`
- `Currency`

#### E. История остатков (`STOCK_HISTORY_REPORT_CSV`)

Поля:
- карточка: `VendorCode`, `Name`, `NmID`, `SubjectName`, `BrandName`
- размер/склад: `SizeName`, `ChrtID`, `RegionName`, `OfficeName`, `Availability`
- заказы/выкупы: `OrdersCount`, `OrdersSum`, `BuyoutCount`, `BuyoutSum`, `BuyoutPercent`, `AvgOrders`
- остатки/оборачиваемость: `StockCount`, `StockSum`, `SaleRate`, `AvgStockTurnover`
- логистика/цена: `ToClientCount`, `FromClientCount`, `Price`, `OfficeMissingTime`
- упущенные: `LostOrdersCount`, `LostOrdersSum`, `LostBuyoutsCount`, `LostBuyoutsSum`
- динамические месячные столбцы: `AvgOrdersByMonth_MM.YYYY`
- `Currency`

### Ошибки

- `400`, `401`, `403`, `429`

---

## Практический сценарий работы с CSV

1. Создать задачу: `POST /api/v2/nm-report/downloads`.
2. Проверить статус: `GET /api/v2/nm-report/downloads`.
3. Если `FAILED`: `POST /api/v2/nm-report/downloads/retry`.
4. Если `SUCCESS`: `GET /api/v2/nm-report/downloads/file/{downloadId}`.
