# Платная приёмка

Базовый домен: `https://seller-analytics-api.wildberries.ru`

## Сценарий работы

1. Создать задание: `GET /api/v1/acceptance_report`
2. Проверить статус: `GET /api/v1/acceptance_report/tasks/{task_id}/status`
3. Скачать отчёт: `GET /api/v1/acceptance_report/tasks/{task_id}/download`

---

## 1) GET `/api/v1/acceptance_report`

**Назначение:** создать задание на отчёт о платной приёмке.

### Ограничения

- Максимальный период: 31 день.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/acceptance_report" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2025-02-28" \
  --data-urlencode "dateTo=2025-03-21"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | string (`YYYY-MM-DD`) | да | Начало отчётного периода |
| `dateTo` | string (`YYYY-MM-DD`) | да | Конец отчётного периода |

### Ответ `200`

- `data.taskId` — ID задания.

### Ошибки

- `400` — ошибки дат (`Missing...`, `Incorrect...`, `DateRangeExceeded`, `DateRanges`)
- `401`, `429`

---

## 2) GET `/api/v1/acceptance_report/tasks/{task_id}/status`

**Назначение:** проверить статус задания.

### Лимит

- `5 сек`: 1 запрос
- интервал: 5 сек
- всплеск: 1

### Пример

```bash
curl -X GET "https://seller-analytics-api.wildberries.ru/api/v1/acceptance_report/tasks/06e06887-9d9f-491f-b16a-bb1766fcb8d2/status" \
  -H "Authorization: $WB_API_TOKEN"
```

### Path-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `task_id` | string(UUID) | да | ID задания |

### Ответ `200`

- `data.id`
- `data.status`: `new`, `processing`, `done`, `purged`, `canceled`

### Ошибки

- `400`, `401`, `404`, `429`

---

## 3) GET `/api/v1/acceptance_report/tasks/{task_id}/download`

**Назначение:** получить готовый отчёт по `task_id`.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -X GET "https://seller-analytics-api.wildberries.ru/api/v1/acceptance_report/tasks/06e06887-9d9f-491f-b16a-bb1766fcb8d2/download" \
  -H "Authorization: $WB_API_TOKEN"
```

### Ответ `200`

Тип: `array<object>`.

| Поле | Тип | Описание |
|---|---|---|
| `count` | integer | Количество товаров, шт. |
| `giCreateDate` | date | Дата создания поставки |
| `incomeId` | integer | Номер поставки |
| `nmID` | integer | Артикул WB |
| `shkCreateDate` | date | Дата приёмки |
| `subjectName` | string | Предмет |
| `total` | number | Суммарная стоимость приёмки, ₽ |

### Ошибки

- `400`, `401`, `404`, `429`
