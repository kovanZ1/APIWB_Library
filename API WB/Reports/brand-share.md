# Доля бренда в продажах

Базовый домен: `https://seller-analytics-api.wildberries.ru`

---

## 1) GET `/api/v1/analytics/brand-share/brands`

**Назначение:** получить бренды продавца для отчёта доли бренда.

### Ограничения

Возвращаются бренды, которые:
- продавались за последние 90 дней;
- есть на складе WB.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 10

### Пример

```bash
curl -X GET "https://seller-analytics-api.wildberries.ru/api/v1/analytics/brand-share/brands" \
  -H "Authorization: $WB_API_TOKEN"
```

### Ответ `200` (`SuccessBrandsResponse`)

- `data[]` — массив строк с названиями брендов.

### Ошибки

- `401`, `429`

---

## 2) GET `/api/v1/analytics/brand-share/parent-subjects`

**Назначение:** получить родительские категории выбранного бренда.

### Ограничения

- Период максимум 365 дней.
- Данные доступны с 2022-11-01.

### Лимит

- `5 сек`: 1 запрос
- интервал: 5 сек
- всплеск: 20

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/analytics/brand-share/parent-subjects" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "brand=H%26M" \
  --data-urlencode "locale=ru" \
  --data-urlencode "dateFrom=2026-01-01" \
  --data-urlencode "dateTo=2026-01-31"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `locale` | enum | нет | Язык `parentName`: `ru`, `en`, `zh` |
| `brand` | string | да | Бренд |
| `dateFrom` | string (`YYYY-MM-DD`) | да | Начало периода |
| `dateTo` | string (`YYYY-MM-DD`) | да | Конец периода |

### Ответ `200` (`SuccessParentsResponse`)

- `data[]`:
  - `parentId`
  - `parentName`

### Ошибки

- `400` — неверные даты, `locale`, отсутствует `brand`
- `401`, `429`

---

## 3) GET `/api/v1/analytics/brand-share`

**Назначение:** получить отчёт доли бренда в родительской категории.

### Ограничения

- Период максимум 365 дней.
- Данные доступны с 2022-11-01.

### Лимит

- `5 сек`: 1 запрос
- интервал: 5 сек
- всплеск: 20

### Пример

```bash
curl -G "https://seller-analytics-api.wildberries.ru/api/v1/analytics/brand-share" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "parentId=1" \
  --data-urlencode "brand=H%26M" \
  --data-urlencode "dateFrom=2026-01-01" \
  --data-urlencode "dateTo=2026-01-31"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `parentId` | integer | да | ID родительской категории |
| `brand` | string | да | Бренд |
| `dateFrom` | string (`YYYY-MM-DD`) | да | Начало периода |
| `dateTo` | string (`YYYY-MM-DD`) | да | Конец периода |

### Ответ `200` (`SuccessBrandShareResponse`)

`report[]`:

| Поле | Тип | Описание |
|---|---|---|
| `applyDate` | string | Дата (`YYYY-MM-DD`) |
| `brandRating` | integer | Рейтинг бренда в категории |
| `pricePercent` | float | Доля в продажах по сумме, % |
| `qtyPercent` | float | Доля в продажах по количеству, % |

### Ошибки

- `400` — неверные даты, отсутствует `parentId`/`brand`, диапазон >365
- `401`, `429`
