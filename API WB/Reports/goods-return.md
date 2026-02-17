# Отчёт о возвратах и перемещении товаров

Базовый домен: `https://seller-analytics-api.wildberries.ru`

---

## GET `/api/v1/analytics/goods-return`

**Назначение:** получить отчёт о возвратах товаров продавцу.

### Ограничения

- Максимальный период: 31 день.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 10

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/analytics/goods-return" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2026-01-01" \
  --data-urlencode "dateTo=2026-01-31"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | date | да | Дата начала периода |
| `dateTo` | date | да | Дата конца периода |

### Ответ `200`

Формат: объект с массивом `report[]`.

Поля записи возврата:

| Поле | Тип | Описание |
|---|---|---|
| `barcode` | string | Баркод |
| `brand` | string | Бренд |
| `completedDt` | string\|null | Дата выдачи возврата продавцу |
| `dstOfficeAddress` | string | Адрес ПВЗ выдачи |
| `dstOfficeId` | integer | ID ПВЗ выдачи |
| `expiredDt` | string\|null | Дата истечения срока хранения |
| `isStatusActive` | enum | `0` архивный, `1` активный |
| `nmId` | integer | Артикул WB |
| `orderDt` | date | Дата заказа на возврат |
| `orderId` | integer | Номер сборочного задания |
| `readyToReturnDt` | string\|null | Готовность к выдаче |
| `reason` | string | Причина возврата |
| `returnType` | string | Тип возврата |
| `shkId` | integer | Штрихкод |
| `srid` | string | Уникальный ID возврата |
| `status` | string | Статус возврата |
| `stickerId` | string | Стикер возврата |
| `subjectName` | string | Предмет |
| `techSize` | string | Размер |

### Ошибки

- `400` — ошибки дат и диапазона
- `401`, `429`
