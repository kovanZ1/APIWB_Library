# Платное хранение

Базовый домен: `https://seller-analytics-api.wildberries.ru`

## Сценарий работы

1. Создать задание: `GET /api/v1/paid_storage`
2. Проверить статус: `GET /api/v1/paid_storage/tasks/{task_id}/status`
3. Скачать отчёт: `GET /api/v1/paid_storage/tasks/{task_id}/download`

---

## 1) GET `/api/v1/paid_storage`

**Назначение:** создать задание на отчёт о платном хранении.

### Ограничения

- Максимальный период: 8 дней.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 5

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/paid_storage" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2026-01-01" \
  --data-urlencode "dateTo=2026-01-08"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | string | да | Начало периода (RFC3339, дата или дата-время) |
| `dateTo` | string | да | Конец периода (RFC3339, дата или дата-время) |

### Ответ `200`

- `data.taskId` — ID задания.

### Ошибки

- `400` — ошибки дат, включая `DateRangeExceeded8`
- `401`, `429`

---

## 2) GET `/api/v1/paid_storage/tasks/{task_id}/status`

**Назначение:** проверить статус задания.

### Лимит

- `5 сек`: 1 запрос
- интервал: 5 сек
- всплеск: 5

### Пример

```bash
curl -X GET "https://seller-analytics-api.wildberries.ru/api/v1/paid_storage/tasks/06e06887-9d9f-491f-b16a-bb1766fcb8d2/status" \
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

## 3) GET `/api/v1/paid_storage/tasks/{task_id}/download`

**Назначение:** получить готовый отчёт по `task_id`.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -X GET "https://seller-analytics-api.wildberries.ru/api/v1/paid_storage/tasks/06e06887-9d9f-491f-b16a-bb1766fcb8d2/download" \
  -H "Authorization: $WB_API_TOKEN"
```

### Ответ `200`

Тип: `ResponsePaidStorage` (массив).

Поля строки отчёта:

| Поле | Тип | Описание |
|---|---|---|
| `date` | string | Дата расчёта/перерасчёта |
| `logWarehouseCoef` | number | Коэффициент логистики и хранения |
| `officeId` | integer | ID склада |
| `warehouse` | string | Название склада |
| `warehouseCoef` | number | Коэффициент склада |
| `giId` | integer | ID поставки |
| `chrtId` | integer | ID размера |
| `size` | string | Размер (`techSize`) |
| `barcode` | string | Баркод |
| `subject` | string | Предмет |
| `brand` | string | Бренд |
| `vendorCode` | string | Артикул продавца |
| `nmId` | integer | Артикул WB |
| `volume` | number | Объём товара |
| `calcType` | string | Тип расчёта |
| `warehousePrice` | number | Стоимость хранения |
| `barcodesCount` | integer | Тарифицируемое количество единиц |
| `palletPlaceCode` | integer | Код паллетоместа |
| `palletCount` | number | Количество паллет |
| `originalDate` | string | Дата первоначального расчёта |
| `loyaltyDiscount` | number | Скидка программы лояльности, ₽ |
| `tariffFixDate` | string | Дата фиксации тарифа |
| `tariffLowerDate` | string | Дата понижения тарифа |

### Ошибки

- `400`, `401`, `404`, `429`
