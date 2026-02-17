# Отчёт о товарах c обязательной маркировкой

Базовый домен: `https://seller-analytics-api.wildberries.ru`

---

## POST `/api/v1/analytics/excise-report`

**Назначение:** получить отчёт по операциям с товарами обязательной маркировки.

### Лимит

- `5 ч`: 10 запросов
- интервал: 30 мин
- всплеск: 10

### Пример

```bash
curl -X POST "https://seller-analytics-api.wildberries.ru/api/v1/analytics/excise-report?dateFrom=2026-01-01&dateTo=2026-01-31" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"countries": ["RU", "AM"]}'
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | string | нет | Начало периода |
| `dateTo` | string | нет | Конец периода |

Примечание: в OpenAPI параметры есть в `components/parameters` и не помечены как required в этом методе.

### Тело запроса (`ExciseReportRequest`)

Тело необязательное.

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `countries` | array<string> | нет | ISO-коды стран: `AM`, `BY`, `KG`, `KZ`, `RU`, `UZ` |

Если `countries` не передавать или передать пустым, возвращаются все страны.

### Ответ `200` (`ExciseReportResponse`)

Структура: `response.data[]`.

Поля строки:

| Поле | Тип | Описание |
|---|---|---|
| `name` | string | Страна покупателя |
| `price` | number | Цена товара (с НДС) |
| `currency_name_short` | string | Валюта |
| `excise_short` | string | Код маркировки |
| `barcode` | string | Баркод |
| `nm_id` | integer | Артикул WB |
| `operation_type_id` | integer | Тип операции (`1` вывод из оборота, `2` возврат в оборот) |
| `fiscal_doc_number` | integer | Номер фискального документа |
| `fiscal_dt` | string | Дата фискализации (`YYYY-MM-DD`) |
| `fiscal_drive_number` | string | Номер фискального накопителя |
| `rid` | integer | Rid |
| `srid` | string | Srid |

### Ошибки

- `400` — `4xxResponse` (в т.ч. ошибка схемы request body)
- `401`, `429`
