# Продажи по регионам

Базовый домен: `https://seller-analytics-api.wildberries.ru`

---

## GET `/api/v1/analytics/region-sale`

**Назначение:** отчёт по продажам, сгруппированным по регионам стран.

### Ограничения

- Максимальный период: 31 день.

### Лимит

- `10 сек`: 1 запрос
- интервал: 10 сек
- всплеск: 5

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/analytics/region-sale" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2026-01-01" \
  --data-urlencode "dateTo=2026-01-31"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | string (`YYYY-MM-DD`) | да | Начало периода |
| `dateTo` | string (`YYYY-MM-DD`) | да | Конец периода |

### Ответ `200` (`SuccessRegionSaleResponse`)

`report[]`:

| Поле | Тип | Описание |
|---|---|---|
| `cityName` | string | Населённый пункт |
| `countryName` | string | Страна |
| `foName` | string | Федеральный округ |
| `regionName` | string | Регион |
| `nmID` | integer | Артикул WB |
| `sa` | string | Артикул продавца |
| `saleItemInvoiceQty` | integer | Выкупили, шт. |
| `saleInvoiceCostPrice` | float | К перечислению за товар, ₽ |
| `saleInvoiceCostPricePerc` | float | Доля, % |

### Ошибки

- `400` — ошибки дат/диапазона
- `401`, `429`
