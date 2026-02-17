# Календарь акций

Базовый домен: `https://dp-calendar-api.wildberries.ru`

## Общий лимит категории

Для всех методов категории **Календарь акций**:
- `6 сек`: 10 запросов
- интервал: `600 мс`
- всплеск: 5

## Важно

- Методы работы со списком товаров и загрузкой (`nomenclatures`, `upload`) не применяются к автоакциям.

---

## 1) GET `/api/v1/calendar/promotions`

**Назначение:** получить список акций с периодами проведения.

### Пример

```bash
curl -G "https://dp-calendar-api.wildberries.ru/api/v1/calendar/promotions" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "startDateTime=2026-01-01T00:00:00Z" \
  --data-urlencode "endDateTime=2026-01-31T23:59:59Z" \
  --data-urlencode "allPromo=false" \
  --data-urlencode "limit=100" \
  --data-urlencode "offset=0"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `startDateTime` | date-time | да | Начало периода, формат `YYYY-MM-DDTHH:MM:SSZ` |
| `endDateTime` | date-time | да | Конец периода, формат `YYYY-MM-DDTHH:MM:SSZ` |
| `allPromo` | boolean | да | `false` — только доступные, `true` — все акции |
| `limit` | integer | нет | Количество акций, `1..1000` |
| `offset` | integer | нет | Смещение, `>=0` |

### Ответ `200` (`PromotionsSuccessResponse`)

| Поле | Тип | Описание |
|---|---|---|
| `data.promotions[]` | array | Список акций |
| `promotions[].id` | integer | ID акции |
| `promotions[].name` | string | Название |
| `promotions[].startDateTime` | date-time | Начало |
| `promotions[].endDateTime` | date-time | Конец |
| `promotions[].type` | enum | `regular` / `auto` |

### Ошибки

- `400` — `ErrorFailedParseData`
- `401`, `429`

---

## 2) GET `/api/v1/calendar/promotions/details`

**Назначение:** получить детальную информацию об акциях по ID.

### Пример

```bash
curl -G "https://dp-calendar-api.wildberries.ru/api/v1/calendar/promotions/details" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "promotionIDs=1,3,64"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `promotionIDs` | string | да | Список ID акций |

### Ответ `200` (`PromotionsGetByIDSuccessResponse`)

Ключевые поля `data.promotions[]`:

| Поле | Тип | Описание |
|---|---|---|
| `id`, `name`, `description` | integer/string | Идентификатор и описание акции |
| `advantages[]` | array<string> | Преимущества акции |
| `startDateTime`, `endDateTime` | date-time | Время проведения |
| `inPromoActionLeftovers`, `inPromoActionTotal` | integer | Товары в акции |
| `notInPromoActionLeftovers`, `notInPromoActionTotal` | integer | Товары вне акции |
| `participationPercentage` | integer | Доля участвующих товаров |
| `type` | enum | `regular` / `auto` |
| `exceptionProductsCount` | integer | Исключённые товары (для `auto`) |
| `ranging[]` | array<object> | Условия ранжирования (`condition`, `participationRate`, `boost`) |

### Ошибки

- `400` — `ErrorFailedParseData`
- `401`, `429`

---

## 3) GET `/api/v1/calendar/promotions/nomenclatures`

**Назначение:** получить список товаров, подходящих для участия в акции.

### Важно

- Метод не применим для автоакций.

### Пример

```bash
curl -G "https://dp-calendar-api.wildberries.ru/api/v1/calendar/promotions/nomenclatures" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "promotionID=1" \
  --data-urlencode "inAction=false" \
  --data-urlencode "limit=100" \
  --data-urlencode "offset=0"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `promotionID` | integer | да | ID акции |
| `inAction` | boolean | да | `true` — уже в акции, `false` — не участвуют |
| `limit` | integer | нет | Количество товаров, `1..1000` |
| `offset` | integer | нет | Смещение |

### Ответ `200` (`ResponsePromotionsGoodsLists`)

| Поле | Тип | Описание |
|---|---|---|
| `data.nomenclatures[]` | array | Товары |
| `id` | integer | Артикул WB |
| `inAction` | boolean | Участвует ли товар в акции |
| `price` | float | Текущая розничная цена |
| `currencyCode` | string | Валюта ISO 4217 |
| `planPrice` | float | Плановая цена в акции |
| `discount` | integer | Текущая скидка |
| `planDiscount` | integer | Рекомендуемая скидка |

### Ошибки

- `400` — `ErrorWrongParameters`
- `401`
- `422` — `ErrParameterValuesIncorrect`
- `429`

---

## 4) POST `/api/v1/calendar/promotions/upload`

**Назначение:** создать задачу на загрузку товаров в акцию.

### Важно

- Метод не применим для автоакций.
- Загрузка асинхронная, статус задачи проверяется в методах истории задач цен/скидок.

### Пример

```bash
curl -X POST "https://dp-calendar-api.wildberries.ru/api/v1/calendar/promotions/upload" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "promotionID": 1,
      "uploadNow": true,
      "nomenclatures": [75632091, 31322455, 642080796]
    }
  }'
```

### Тело запроса (`PromotionsSupplierTaskRequest`)

| Поле | Тип | Обяз. | Ограничения |
|---|---|---|---|
| `data.promotionID` | integer | да | ID акции, `>=1` |
| `data.uploadNow` | boolean | нет | `true` — применить сейчас, `false` — в момент старта акции |
| `data.nomenclatures` | array<integer> | да | Артикулы WB, `1..1000`, уникальные |

### Ответ `200` (`UploadSuccessResponse`)

| Поле | Тип | Описание |
|---|---|---|
| `data.alreadyExists` | boolean | Такая загрузка уже существует |
| `data.uploadID` | integer | ID задачи загрузки |

### Ошибки

- `400` — `ErrorWrongParameters`
- `401`
- `422` — `UnprocessableEntity`
- `429`
