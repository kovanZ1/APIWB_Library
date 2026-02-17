# Скрытые товары

Базовый домен: `https://seller-analytics-api.wildberries.ru`

---

## 1) GET `/api/v1/analytics/banned-products/blocked`

**Назначение:** список заблокированных карточек с причинами блокировки.

### Лимит

- `10 сек`: 1 запрос
- интервал: 10 сек
- всплеск: 6

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/analytics/banned-products/blocked" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "sort=nmId" \
  --data-urlencode "order=asc"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `sort` | enum | да | `brand`, `nmId`, `title`, `vendorCode`, `reason` |
| `order` | enum | да | `desc` / `asc` |

### Ответ `200`

- `report[]`:
  - `brand`
  - `nmId`
  - `title`
  - `vendorCode`
  - `reason`

### Ошибки

- `400` — объект с полями `title`, `status`, `detail`, `requestId`, `origin`
- `401`, `429`

---

## 2) GET `/api/v1/analytics/banned-products/shadowed`

**Назначение:** список товаров, скрытых из каталога.

### Лимит

- `10 сек`: 1 запрос
- интервал: 10 сек
- всплеск: 6

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/analytics/banned-products/shadowed" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "sort=title" \
  --data-urlencode "order=desc"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `sort` | enum | да | `brand`, `nmId`, `title`, `vendorCode`, `nmRating` |
| `order` | enum | да | `desc` / `asc` |

### Ответ `200`

- `report[]`:
  - `brand`
  - `nmId`
  - `title`
  - `vendorCode`
  - `nmRating`

### Ошибки

- `400` — объект с полями `title`, `status`, `detail`, `requestId`, `origin`
- `401`, `429`
