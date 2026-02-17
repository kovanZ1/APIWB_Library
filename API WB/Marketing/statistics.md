# Статистика

## 1) GET `/adv/v3/fullstats`

Базовый домен: `https://advert-api.wildberries.ru`

**Назначение:** полная статистика кампаний независимо от типа.

### Ограничения и применимость

- Максимальный период: 31 день.
- Для кампаний в статусах `7`, `9`, `11`.

### Лимит

- `1 мин`: 3 запроса
- интервал: `20 сек`
- всплеск: 1

### Пример

```bash
curl -G "https://advert-api.wildberries.ru/adv/v3/fullstats" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "ids=22161678,28449281" \
  --data-urlencode "beginDate=2026-01-01" \
  --data-urlencode "endDate=2026-01-31"
```

### Query-параметры

| Параметр | Тип | Обяз. | Ограничения |
|---|---|---|---|
| `ids` | string | да | ID кампаний через запятую, максимум 50 |
| `beginDate` | date | да | Начало периода |
| `endDate` | date | да | Конец периода |

### Ответ `200`

Тип: `array<FullStatsItem>`.

Ключевые агрегированные поля `FullStatsItem`:

| Поле | Тип | Описание |
|---|---|---|
| `advertId` | integer | ID кампании |
| `views` | integer | Просмотры |
| `clicks` | integer | Клики |
| `atbs` | integer | Добавления в корзину |
| `orders` | integer | Заказы |
| `shks` | integer | Заказанные товары, шт. |
| `sum` | double | Затраты, ₽ |
| `sum_price` | double | Сумма заказов, ₽ |
| `ctr` | double | CTR, % |
| `cr` | double | CR |
| `cpc` | double | Средняя стоимость клика, ₽ |
| `canceled` | integer | Отмены, шт. |
| `days` | array | Разбивка по дням |
| `boosterStats` | array | Средняя позиция (для кампаний с единой ставкой) |

`days[]`:
- суточные метрики (`views`, `clicks`, `atbs`, `orders`, `sum`, `date`, ...)
- `apps[]` — разрез по платформам (`appType`: `1` сайт, `32` Android, `64` iOS)
- в каждом `apps[]` есть `nms[]` со статистикой по артикулам WB.

### Ошибки

- `400` — `FullStatsError`
- `401`, `429`

---

## 2) POST `/adv/v1/stats`

Базовый домен: `https://advert-media-api.wildberries.ru`

**Назначение:** статистика кампаний WB Медиа.

### Лимит

- `1 сек`: 10 запросов
- интервал: `100 мс`
- всплеск: 10

### Особенность формата запроса

Тело — массив (от 1 до 100 элементов), каждый элемент — один из вариантов:

1. `RequestWithDate`: `id` + `dates[]`
2. `RequestWithInterval`: `id` + `interval.begin/end`
3. `RequestWithCampaignID`: только `id` (без фильтра)

Можно смешивать варианты в одном запросе.

### Пример

```bash
curl -X POST "https://advert-media-api.wildberries.ru/adv/v1/stats" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {"id": 8960367, "dates": ["2026-01-07", "2026-01-06"]},
    {"id": 9876543, "interval": {"begin": "2026-01-01", "end": "2026-01-10"}},
    {"id": 107024}
  ]'
```

### Ответ `200`

Тип: `array`, элементы `oneOf`:
- `StatDate` (если запрос был с `dates`)
- `StatInterval` (если запрос был с `interval`)
- `Stat` (если только `id`)

Во всех вариантах есть `stats[]` (блок статистики по баннерам):

Ключевые поля `stats[]`:
- `item_id`, `item_name`, `category_name`, `advert_type`, `place`
- `views`, `clicks`, `ctr`, `cr`, `orders`, `atbs`
- `price`, `expenses`, `cpc`
- `date_from`, `date_to`, `status`
- `daily_stats[]` с разрезом по платформам
- дополнительные коэффициенты: `cr1`, `cr2`

### Ошибки

- `400` — `responseAdvError1`
- `401`, `429`

---

## 3) POST `/adv/v0/normquery/stats`

Базовый домен: `https://advert-api.wildberries.ru`

**Назначение:** статистика поисковых кластеров за период (агрегированная версия).

### Применимость

- Только для кампаний с `payment_type=cpm`.

### Лимит

- `1 мин`: 10 запросов
- интервал: `6 сек`
- всплеск: 20

### Пример

```bash
curl -X POST "https://advert-api.wildberries.ru/adv/v0/normquery/stats" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "2026-01-01",
    "to": "2026-01-07",
    "items": [{"advert_id": 1825035, "nm_id": 983512347}]
  }'
```

### Тело запроса (`V0GetNormQueryStatsRequest`)

| Поле | Тип | Обяз. | Ограничения |
|---|---|---|---|
| `from` | date | да | Начало периода |
| `to` | date | да | Конец периода |
| `items` | array<object> | да | максимум 100 |
| `items[].advert_id` | integer | да | ID кампании |
| `items[].nm_id` | integer | да | Артикул WB |

### Ответ `200` (`V0GetNormQueryStatsResponse`)

| Поле | Тип | Описание |
|---|---|---|
| `stats` | array | Статистика по товарам/кампаниям |

Элемент `stats[]`:

| Поле | Тип | Описание |
|---|---|---|
| `advert_id` | integer | ID кампании |
| `nm_id` | integer | Артикул |
| `stats[]` | array | Показатели по кластерам |

Элемент внутреннего `stats[]`:
- `norm_query`, `views`, `clicks`, `atbs`, `orders`
- `ctr`, `cpc`, `cpm`, `avg_pos`
- `shks`, `spend`

### Ошибки

- `400`, `401`, `403` (`AccessDenied`), `429`

---

## 4) POST `/adv/v1/normquery/stats`

Базовый домен: `https://advert-api.wildberries.ru`

**Назначение:** статистика поисковых кластеров за период с детализацией по дням.

### Лимит

- `1 мин`: 10 запросов
- интервал: `6 сек`
- всплеск: 20

### Пример

```bash
curl -X POST "https://advert-api.wildberries.ru/adv/v1/normquery/stats" \
  -H "Authorization: $WB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "2026-01-01",
    "to": "2026-01-30",
    "items": [{"advertId": 123456789, "nmId": 987654321}]
  }'
```

### Тело запроса (`V1GetNormQueryStatsRequest`)

| Поле | Тип | Обяз. | Ограничения |
|---|---|---|---|
| `from` | date | да | Начало периода |
| `to` | date | да | Конец периода |
| `items` | array<object> | да | максимум 100 |
| `items[].advertId` | int64 | да | ID кампании |
| `items[].nmId` | int64 | да | Артикул WB |

### Ответ `200` (`V1GetNormQueryStatsResponse`)

| Поле | Тип | Описание |
|---|---|---|
| `items` | array | Результаты по каждому `(advertId, nmId)` |

Элемент `items[]`:

| Поле | Тип | Описание |
|---|---|---|
| `advertId` | int64 | ID кампании |
| `nmId` | int64 | Артикул WB |
| `dailyStats` | array | Статистика по дням |

Элемент `dailyStats[]`:

| Поле | Тип | Описание |
|---|---|---|
| `date` | date | Дата |
| `stat.normQuery` | string | Поисковый кластер |
| `stat.views` | integer | Просмотры |
| `stat.clicks` | integer | Клики |
| `stat.atbs` | integer | Добавления в корзину |
| `stat.orders` | integer | Заказы |
| `stat.shks` | integer | Заказанные товары, шт. |
| `stat.spend` | double | Затраты |
| `stat.ctr` | float | CTR, % |
| `stat.cpc` | float | Средняя стоимость клика, ₽ |
| `stat.cpm` | float | Средняя стоимость 1000 показов, ₽ |
| `stat.avgPos` | float | Средняя позиция товара |

### Ошибки

- `400`, `401`, `429`.
