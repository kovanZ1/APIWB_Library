# WB API Reports

Документация по разделу **Отчёты** WB API.

## Что внутри

- `core-reports.md` — Основные отчёты (4 метода)
- `warehouse-remains.md` — Отчёт об остатках на складах (3 метода)
- `excise-report.md` — Отчёт о товарах c обязательной маркировкой (1 метод)
- `deductions.md` — Отчёты об удержаниях (5 методов)
- `paid-acceptance.md` — Платная приёмка (3 метода)
- `paid-storage.md` — Платное хранение (3 метода)
- `region-sales.md` — Продажи по регионам (1 метод)
- `brand-share.md` — Доля бренда в продажах (3 метода)
- `hidden-products.md` — Скрытые товары (2 метода)
- `goods-return.md` — Отчёт о возвратах и перемещении товаров (1 метод)

Всего: **26 методов**.

## Базовые домены

- `https://statistics-api.wildberries.ru`
- `https://seller-analytics-api.wildberries.ru`

## Базовые правила

- Авторизация: заголовок `Authorization` (`HeaderApiKey`).
- Для инкрементальной выгрузки в основных отчётах используйте `dateFrom` из `lastChangeDate` последней строки предыдущей выгрузки.
- Часть отчётов формируется асинхронно по `task_id`:
  1. создание задания
  2. проверка статуса
  3. скачивание результата
- Общие ошибки авторизации и лимитов:
  - `401` — не авторизован
  - `429` — превышен лимит

## Карта эндпоинтов

### Основные отчёты

1. `GET /api/v1/supplier/incomes` (устарел)
2. `GET /api/v1/supplier/stocks`
3. `GET /api/v1/supplier/orders`
4. `GET /api/v1/supplier/sales`

### Отчёт об остатках на складах

5. `GET /api/v1/warehouse_remains`
6. `GET /api/v1/warehouse_remains/tasks/{task_id}/status`
7. `GET /api/v1/warehouse_remains/tasks/{task_id}/download`

### Отчёт о товарах c обязательной маркировкой

8. `POST /api/v1/analytics/excise-report`

### Отчёты об удержаниях

9. `GET /api/analytics/v1/measurement-penalties`
10. `GET /api/analytics/v1/warehouse-measurements`
11. `GET /api/analytics/v1/deductions`
12. `GET /api/v1/analytics/antifraud-details`
13. `GET /api/v1/analytics/goods-labeling`

### Платная приёмка

14. `GET /api/v1/acceptance_report`
15. `GET /api/v1/acceptance_report/tasks/{task_id}/status`
16. `GET /api/v1/acceptance_report/tasks/{task_id}/download`

### Платное хранение

17. `GET /api/v1/paid_storage`
18. `GET /api/v1/paid_storage/tasks/{task_id}/status`
19. `GET /api/v1/paid_storage/tasks/{task_id}/download`

### Продажи по регионам

20. `GET /api/v1/analytics/region-sale`

### Доля бренда в продажах

21. `GET /api/v1/analytics/brand-share/brands`
22. `GET /api/v1/analytics/brand-share/parent-subjects`
23. `GET /api/v1/analytics/brand-share`

### Скрытые товары

24. `GET /api/v1/analytics/banned-products/blocked`
25. `GET /api/v1/analytics/banned-products/shadowed`

### Отчёт о возвратах и перемещении товаров

26. `GET /api/v1/analytics/goods-return`
