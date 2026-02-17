# Отчёты об удержаниях

Базовый домен: `https://seller-analytics-api.wildberries.ru`

---

## 1) GET `/api/analytics/v1/measurement-penalties`

**Назначение:** удержания за занижение габаритов упаковки.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/analytics/v1/measurement-penalties" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2025-02-01T15:00:00Z" \
  --data-urlencode "dateTo=2025-10-11T18:00:00Z" \
  --data-urlencode "limit=100" \
  --data-urlencode "offset=0"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | date-time | нет | Начало периода (по умолчанию дата первого появления данных) |
| `dateTo` | date-time | да | Конец периода |
| `limit` | integer | да | Количество записей, максимум 1000 |
| `offset` | integer | нет | Смещение, default `0` |

### Ответ `200` (`MeasurementPenalties`)

| Поле | Тип | Описание |
|---|---|---|
| `data.reports[]` | array | Список удержаний |
| `data.total` | integer | Общее количество (без учёта `limit/offset`) |

Поля записи `reports[]`:
- товар: `nmId`, `subjectName`
- замер: `dimId`, `volume`, `width`, `length`, `height`
- карточка: `volumeSup`, `widthSup`, `lengthSup`, `heightSup`
- отклонение: `prcOver`
- медиа: `photoUrls[]`
- штраф: `dtBonus`, `penaltyAmount`
- валидация/сторно: `isValid`, `isValidDt`, `reversalAmount`

### Ошибки

- `400` — `Response400Retentions`
- `401`
- `403` — `Response403Retentions`
- `429`

---

## 2) GET `/api/analytics/v1/warehouse-measurements`

**Назначение:** отчёт о замерах склада.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/analytics/v1/warehouse-measurements" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateTo=2025-10-11T18:00:00Z" \
  --data-urlencode "limit=100" \
  --data-urlencode "offset=0"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | date-time | нет | Начало периода |
| `dateTo` | date-time | да | Конец периода |
| `limit` | integer | да | Количество замеров, максимум 1000 |
| `offset` | integer | нет | Смещение |

### Ответ `200` (`WHM`)

- `data.reports[]` — замеры
- `data.total` — общее количество

Поля `reports[]`:
- `nmId`, `subjectName`, `dimId`
- `volume`, `width`, `length`, `height`
- `photoUrls[]`
- `dt`

### Ошибки

- `400`, `401`, `403`, `429`

---

## 3) GET `/api/analytics/v1/deductions`

**Назначение:** удержания за подмены и неверные вложения.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/analytics/v1/deductions" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateTo=2025-10-11T18:00:00Z" \
  --data-urlencode "sort=dtBonus" \
  --data-urlencode "order=desc" \
  --data-urlencode "limit=100" \
  --data-urlencode "offset=0"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | date-time | нет | Начало периода |
| `dateTo` | date-time | да | Конец периода |
| `sort` | enum | нет | `nmId`, `dtBonus`, `bonusSumm`; default `dtBonus` |
| `order` | enum | нет | `desc` / `asc`; default `desc` |
| `limit` | integer | да | Количество записей, максимум 1000 |
| `offset` | integer | нет | Смещение |

### Ответ `200` (`SuccessSubstIncorAttachResponse`)

- `data.reports[]` — удержания
- `data.total`

Поля `reports[]`:
- время/причина/сумма: `dtBonus`, `bonusType`, `bonusSumm`
- товар: `nmId`
- старые значения: `oldShkId`, `oldColor`, `oldSize`, `oldSku`, `oldVendorCode`
- новые значения: `newShkId`, `newColor`, `newSize`, `newSku`, `newVendorCode`
- доказательства: `photoUrls[]`

### Ошибки

- `400`, `401`, `403`, `429`

---

## 4) GET `/api/v1/analytics/antifraud-details`

**Назначение:** удержания за самовыкупы.

### Особенности

- Отчёт формируется еженедельно по средам (до 07:00 МСК), содержит данные за неделю.
- Данные доступны с августа 2023.
- Удержание: 30% стоимости, с пороговыми условиями по сумме (по описанию метода).

### Лимит

- `10 мин`: 1 запрос
- интервал: 10 мин
- всплеск: 10

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/analytics/antifraud-details" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "date=2025-01-15"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `date` | string (`YYYY-MM-DD`) | нет | Дата внутри отчётного периода; если не указать — всё время с августа 2023 |

### Ответ `200` (`SuccessTaskResponse`)

- `details[]`:
  - `nmID`
  - `sum`
  - `currency`
  - `dateFrom`, `dateTo`

### Ошибки

- `400` — неверная дата
- `401`, `429`

---

## 5) GET `/api/v1/analytics/goods-labeling`

**Назначение:** штрафы за отсутствие/нечитаемость обязательной маркировки.

### Ограничения

- Период максимум 31 день.
- Данные доступны с марта 2024.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 10

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/analytics/goods-labeling" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2026-01-01" \
  --data-urlencode "dateTo=2026-01-31"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | date | да | Начало периода |
| `dateTo` | date | да | Конец периода |

### Ответ `200` (`SuccessGoodsLabelingResponse`)

- `report[]`:
  - `amount` — сумма штрафа
  - `date`
  - `incomeId`
  - `nmID`
  - `photoUrls[]`
  - `shkID`
  - `sku`

### Ошибки

- `400` — ошибки формата дат и диапазона (`DateRangeExceeded`, `DateRanges`, и др.)
- `401`, `429`
