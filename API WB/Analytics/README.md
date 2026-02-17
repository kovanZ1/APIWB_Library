# WB API Analytics

Документация по разделу **Аналитика и данные** WB API.

## Что внутри

- `sales-funnel.md` — 3 эндпоинта по воронке продаж
- `search-queries.md` — 5 эндпоинтов по поисковым запросам
- `stock-history.md` — 4 эндпоинта по истории остатков
- `seller-analytics-csv.md` — 4 эндпоинта по CSV-отчётам

## Базовые правила

- Базовый URL: `https://seller-analytics-api.wildberries.ru`
- Авторизация: заголовок `Authorization` (тип `apiKey`)
- Формат дат: `YYYY-MM-DD`
- Большинство эндпоинтов обновляют данные 1 раз в час
- Базовый лимит для методов раздела: **3 запроса / 1 минута**, интервал `20 сек`, всплеск `3`

## Список эндпоинтов

### Воронка продаж

1. `POST /api/analytics/v3/sales-funnel/products`
2. `POST /api/analytics/v3/sales-funnel/products/history`
3. `POST /api/analytics/v3/sales-funnel/grouped/history`

### Аналитика продавца CSV

4. `POST /api/v2/nm-report/downloads`
5. `GET /api/v2/nm-report/downloads`
6. `POST /api/v2/nm-report/downloads/retry`
7. `GET /api/v2/nm-report/downloads/file/{downloadId}`

### Поисковые запросы по вашим товарам

8. `POST /api/v2/search-report/report`
9. `POST /api/v2/search-report/table/groups`
10. `POST /api/v2/search-report/table/details`
11. `POST /api/v2/search-report/product/search-texts`
12. `POST /api/v2/search-report/product/orders`

### История остатков

13. `POST /api/v2/stocks-report/products/groups`
14. `POST /api/v2/stocks-report/products/products`
15. `POST /api/v2/stocks-report/products/sizes`
16. `POST /api/v2/stocks-report/offices`
