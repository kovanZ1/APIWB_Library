# Кампании

Базовый домен: `https://advert-api.wildberries.ru`

---

## 1) GET `/adv/v1/promotion/count`

**Назначение:** получить списки всех рекламных кампаний продавца, сгруппированные по типу и статусу.

### Лимит

- `1 сек`: 5 запросов
- интервал: `200 мс`
- всплеск: 5

### Пример запроса

```bash
curl -X GET "https://advert-api.wildberries.ru/adv/v1/promotion/count" \
  -H "Authorization: $WB_API_TOKEN"
```

### Параметры

Параметров запроса нет.

### Ответ `200`

| Поле | Тип | Описание |
|---|---|---|
| `adverts` | array\|null | Список групп кампаний |
| `all` | integer | Общее количество кампаний |

Структура элемента `adverts[]`:

| Поле | Тип | Описание |
|---|---|---|
| `type` | integer | Тип кампании: `8` (устаревший), `9` (единая/ручная ставка) |
| `status` | integer | Статус кампаний в группе |
| `count` | integer | Количество кампаний в группе |
| `advert_list` | array | Список кампаний |

Структура `advert_list[]`:

| Поле | Тип | Описание |
|---|---|---|
| `advertId` | integer | ID кампании |
| `changeTime` | date-time | Последнее изменение кампании |

### Ошибки

- `401` — не авторизован
- `429` — превышен лимит

---

## 2) GET `/api/advert/v2/adverts`

**Назначение:** получить детальную информацию о кампаниях по фильтрам (ID, статус, тип оплаты).

### Лимит

- `1 сек`: 5 запросов
- интервал: `200 мс`
- всплеск: 5

### Пример запроса

```bash
curl -G "https://advert-api.wildberries.ru/api/advert/v2/adverts" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "ids=12345,23456" \
  --data-urlencode "statuses=9,11" \
  --data-urlencode "payment_type=cpm"
```

### Query-параметры

| Параметр | Тип | Обяз. | Ограничения и смысл |
|---|---|---|---|
| `ids` | string | нет | ID кампаний через запятую, максимум 50 ID |
| `statuses` | string | нет | Список статусов через запятую: `-1,4,7,8,9,11` |
| `payment_type` | string | нет | `cpm` (за показы) или `cpc` (за клик) |

### Ответ `200`

Формат: объект `GetAdverts`.

| Поле | Тип | Описание |
|---|---|---|
| `adverts` | array | Список кампаний |

Структура `adverts[]`:

| Поле | Тип | Описание |
|---|---|---|
| `id` | int64 | ID кампании |
| `bid_type` | string | Тип ставки: `unified` / `manual` |
| `status` | integer | Статус: `-1,4,7,8,9,11` |
| `settings` | object | Настройки кампании |
| `nm_settings` | array | Настройки по товарам |
| `timestamps` | object | Временные отметки |

`settings`:

| Поле | Тип | Описание |
|---|---|---|
| `name` | string | Название кампании |
| `payment_type` | enum | `cpm` / `cpc` |
| `placements.search` | boolean | Размещение в поиске |
| `placements.recommendations` | boolean | Размещение в рекомендациях |

`nm_settings[]`:

| Поле | Тип | Описание |
|---|---|---|
| `nm_id` | int64 | Артикул WB |
| `subject.id` | integer | ID предмета |
| `subject.name` | string | Название предмета |
| `bids_kopecks.search` | int64 | Ставка в поиске, копейки |
| `bids_kopecks.recommendations` | int64 | Ставка в рекомендациях, копейки |

`timestamps`:

| Поле | Тип | Описание |
|---|---|---|
| `created` | date-time | Создание |
| `updated` | date-time | Последнее изменение |
| `started` | date-time\|null | Последний запуск |
| `deleted` | date-time | Время удаления (или дата в будущем, если не удалена) |

### Ошибки

- `400` — некорректные параметры фильтра (`response400`)
- `401` — не авторизован
- `429` — превышен лимит
