# WB API Documents & Accounting

Документация по разделу **Документы и бухгалтерия** WB API.

## Что внутри

- `balance.md` — Баланс (1 метод)
- `financial-reports.md` — Финансовые отчёты (1 метод)
- `documents.md` — Документы (4 метода)

Всего: **6 методов**.

## Базовые домены

- `https://finance-api.wildberries.ru`
- `https://statistics-api.wildberries.ru`
- `https://documents-api.wildberries.ru`

## Базовые правила

- Авторизация: заголовок `Authorization` (`HeaderApiKey`).
- Общие ошибки для всех методов:
  - `401` — не авторизован
  - `429` — превышен лимит

## Карта эндпоинтов

### Баланс

1. `GET /api/v1/account/balance`

### Финансовые отчёты

2. `GET /api/v5/supplier/reportDetailByPeriod`

### Документы

3. `GET /api/v1/documents/categories`
4. `GET /api/v1/documents/list`
5. `GET /api/v1/documents/download`
6. `POST /api/v1/documents/download/all`
