# Отчёт об остатках на складах

Базовый домен: `https://seller-analytics-api.wildberries.ru`

## Сценарий работы

1. Создать задание: `GET /api/v1/warehouse_remains`
2. Проверить статус: `GET /api/v1/warehouse_remains/tasks/{task_id}/status`
3. Скачать отчёт: `GET /api/v1/warehouse_remains/tasks/{task_id}/download`

---

## 1) GET `/api/v1/warehouse_remains`

**Назначение:** создать задание на генерацию отчёта об остатках на складах WB.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 5

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "locale=ru" \
  --data-urlencode "groupByBrand=true" \
  --data-urlencode "groupBySubject=true" \
  --data-urlencode "groupByNm=true" \
  --data-urlencode "filterPics=0" \
  --data-urlencode "filterVolume=0"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `locale` | string | нет | Язык `subjectName` и `warehouseName`: `ru` / `en` / `zh` |
| `groupByBrand` | boolean | нет | Разбивка по брендам |
| `groupBySubject` | boolean | нет | Разбивка по предметам |
| `groupBySa` | boolean | нет | Разбивка по артикулу продавца |
| `groupByNm` | boolean | нет | Разбивка по артикулу WB (в ответе появится `volume`) |
| `groupByBarcode` | boolean | нет | Разбивка по баркоду |
| `groupBySize` | boolean | нет | Разбивка по размеру |
| `filterPics` | integer | нет | `-1` без фото, `0` без фильтра, `1` с фото |
| `filterVolume` | integer | нет | `-1` без габаритов, `0` без фильтра, `3` свыше 3 л |

### Ответ `200`

`CreateTaskResponse`:
- `data.taskId` — ID задания.

### Ошибки

- `400` — `4xxResponse` (например, пустое значение query-параметра)
- `401`, `429`

---

## 2) GET `/api/v1/warehouse_remains/tasks/{task_id}/status`

**Назначение:** проверить статус задания генерации.

### Лимит

- `5 сек`: 1 запрос
- интервал: 5 сек
- всплеск: 5

### Пример

```bash
curl -X GET "https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/06e06887-9d9f-491f-b16a-bb1766fcb8d2/status" \
  -H "Authorization: $WB_API_TOKEN"
```

### Path-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `task_id` | string(UUID) | да | ID задания |

### Ответ `200`

`GetTasksResponse`:
- `data.id` — ID задания
- `data.status` — статус: `new`, `processing`, `done`, `purged`, `canceled`

### Ошибки

- `400` — неверный формат `task_id`
- `401`
- `404` — задание не найдено
- `429`

---

## 3) GET `/api/v1/warehouse_remains/tasks/{task_id}/download`

**Назначение:** получить готовый отчёт по `task_id`.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -X GET "https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/06e06887-9d9f-491f-b16a-bb1766fcb8d2/download" \
  -H "Authorization: $WB_API_TOKEN"
```

### Path-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `task_id` | string(UUID) | да | ID задания |

### Ответ `200`

Тип: `array<object>`.

Поля строки отчёта:

| Поле | Тип | Описание |
|---|---|---|
| `brand` | string | Бренд |
| `subjectName` | string | Предмет |
| `vendorCode` | string | Артикул продавца |
| `nmId` | integer | Артикул WB |
| `barcode` | string | Баркод |
| `techSize` | string | Размер |
| `volume` | number | Объём, литры |
| `warehouses` | array | Остатки и товары в пути |

`warehouses[]`:
- `warehouseName`
- `quantity`

Примечание: `warehouses` включается только при ненулевом `quantity`.

### Ошибки

- `400` — неверный `task_id`
- `401`
- `404` — не найдено
- `429`
