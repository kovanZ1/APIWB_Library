# Медиакампании

Базовый домен: `https://advert-media-api.wildberries.ru`

## Справочник значений

### Тип медиакампании

- `1` — размещение по дням
- `2` — размещение по просмотрам

### Статус медиакампании

- `1` — черновик
- `2` — модерация
- `3` — отклонена
- `4` — готова к запуску
- `5` — запланирована
- `6` — на показах
- `7` — завершена
- `8` — отменена
- `9` — приостановлена продавцом
- `10` — пауза по дневному лимиту
- `11` — пауза

---

## 1) GET `/adv/v1/count`

**Назначение:** получить количество медиакампаний с группировкой по статусам.

### Лимит

- `1 сек`: 10 запросов
- интервал: `100 мс`
- всплеск: 10

### Пример

```bash
curl -X GET "https://advert-media-api.wildberries.ru/adv/v1/count" \
  -H "Authorization: $WB_API_TOKEN"
```

### Параметры

Параметров нет.

### Ответ `200`

| Поле | Тип | Описание |
|---|---|---|
| `all` | integer | Общее количество медиакампаний |
| `adverts.type` | integer | Тип медиакампании |
| `adverts.status` | integer | Статус |
| `adverts.count` | integer | Количество кампаний в группе |

### Ошибки

- `401`, `429`.

---

## 2) GET `/adv/v1/adverts`

**Назначение:** список медиакампаний с фильтрацией/пагинацией/сортировкой.

### Лимит

- `1 сек`: 10 запросов
- интервал: `100 мс`
- всплеск: 10

### Пример

```bash
curl -G "https://advert-media-api.wildberries.ru/adv/v1/adverts" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "status=7" \
  --data-urlencode "type=2" \
  --data-urlencode "limit=50" \
  --data-urlencode "offset=0" \
  --data-urlencode "order=id" \
  --data-urlencode "direction=desc"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `status` | integer | нет | Фильтр по статусу медиакампании |
| `type` | integer | нет | Фильтр по типу (`1` или `2`) |
| `limit` | integer | нет | Количество кампаний |
| `offset` | integer | нет | Смещение |
| `order` | string | нет | Сортировка: `create` или `id` |
| `direction` | string | нет | Направление: `desc` / `asc` |

### Ответы

- `200` — массив кампаний.

Структура элемента массива:

| Поле | Тип | Описание |
|---|---|---|
| `advertId` | integer | ID медиакампании |
| `name` | string | Название |
| `brand` | string | Бренд |
| `type` | integer | Тип |
| `status` | integer | Статус |
| `createTime` | date-time | Время создания |
| `endTime` | date-time | Время завершения (может отсутствовать) |

- `204` — медиакампании не найдены.

### Ошибки

- `401`, `429`.

---

## 3) GET `/adv/v1/advert`

**Назначение:** детальная информация по одной медиакампании.

### Лимит

- `1 сек`: 10 запросов
- интервал: `100 мс`
- всплеск: 10

### Пример

```bash
curl -G "https://advert-media-api.wildberries.ru/adv/v1/advert" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "id=23569"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | integer | да | ID медиакампании |

### Ответ `200`

Основные поля кампании:

| Поле | Тип | Описание |
|---|---|---|
| `advertId` | integer | ID кампании |
| `name` | string | Название |
| `brand` | string | Бренд |
| `type` | integer | Тип кампании |
| `status` | integer | Статус |
| `createTime` | date-time | Создание |
| `extended` | object | Расширенные поля кампании |
| `items` | array | Баннеры/объекты размещения |

`extended` (ключевые поля):

| Поле | Тип | Описание |
|---|---|---|
| `reason` | string\|null | Комментарий модератора |
| `expenses` | integer | Затраты |
| `from`/`to` | date-time | Период показа |
| `updated_at` | date-time | Изменение кампании |
| `price` | integer | Стоимость размещения для типа `1` |
| `budget` | integer | Остаток бюджета для типа `2` |
| `operation` | integer | Источник списания: `1` баланс, `2` счёт |
| `contract_id` | integer | ID контракта (если есть) |

`items[]` (ключевые поля баннера):

| Поле | Тип | Описание |
|---|---|---|
| `id` | integer | ID баннера |
| `name` | string | Название/бренд |
| `status` | integer | Статус |
| `place` | integer | Позиция |
| `budget` | integer | Бюджет |
| `daily_limit` | integer | Дневной лимит |
| `category_name` | string | Категория размещения |
| `cpm` | integer | Ставка |
| `url` | string | URL перехода |
| `advert_type` | integer | Тип продвижения (`1` баннер, `2` меню, `3` email, `4` соцсети, `5` push) |
| `created_at`/`updated_at` | date-time | Временные отметки |
| `date_from`/`date_to` | date-time | Интервал работы баннера |
| `nms` | array<int> | Подборка артикулов |
| `bottomText1`/`bottomText2` | string | Тексты баннера |
| `message` | string | Текст push/email |
| `additionalSettings` | integer | Допнастройки формата/площадки |
| `receiversCount` | integer | Получатели push |
| `subject_id`/`subject_name` | integer/string | Категория товара |
| `action_name` | string | Название акции |
| `show_hours[]` | array<object> | Часы показа (`From`, `To`) |
| `Erid` | string | ID для ОРД |

### Ответы

- `204` — медиакампания не найдена.

### Ошибки

- `401`, `429`.
