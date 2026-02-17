# WB API Marketing

Документация по разделу **Маркетинг и продвижение** WB API.

## Что внутри

- `campaigns.md` — кампании (2 метода)
- `campaign-creation.md` — создание кампаний (4 метода)
- `campaign-management.md` — управление кампаниями (8 методов)
- `search-clusters.md` — поисковые кластеры (6 методов)
- `finance.md` — финансы (5 методов)
- `media.md` — медиакампании (3 метода)
- `statistics.md` — статистика (4 метода)
- `promo-calendar.md` — календарь акций (4 метода)

Всего: **36 API-методов**.

## Базовые правила

- Авторизация: заголовок `Authorization` (`HeaderApiKey`).
- Основные домены:
  - `https://advert-api.wildberries.ru`
  - `https://advert-media-api.wildberries.ru`
  - `https://dp-calendar-api.wildberries.ru`
- Синхронизация данных по разделу (по документации WB):
  - данные — раз в 3 минуты
  - статусы кампаний — раз в минуту
  - ставки кампаний — раз в 30 секунд
- Формат дат: обычно `YYYY-MM-DD`, для даты-времени — `RFC3339/ISO-8601`.

## Карта эндпоинтов

### Кампании

1. `GET /adv/v1/promotion/count`
2. `GET /api/advert/v2/adverts`

### Создание кампаний

3. `POST /api/advert/v1/bids/min`
4. `POST /adv/v2/seacat/save-ad`
5. `GET /adv/v1/supplier/subjects`
6. `POST /adv/v2/supplier/nms`

### Управление кампаниями

7. `GET /adv/v0/delete`
8. `POST /adv/v0/rename`
9. `GET /adv/v0/start`
10. `GET /adv/v0/pause`
11. `GET /adv/v0/stop`
12. `PUT /adv/v0/auction/placements`
13. `PATCH /api/advert/v1/bids`
14. `PATCH /adv/v0/auction/nms`

### Поисковые кластеры

15. `POST /adv/v0/normquery/get-bids`
16. `POST /adv/v0/normquery/bids`
17. `DELETE /adv/v0/normquery/bids`
18. `POST /adv/v0/normquery/get-minus`
19. `POST /adv/v0/normquery/set-minus`
20. `POST /adv/v0/normquery/list`

### Финансы

21. `GET /adv/v1/balance`
22. `GET /adv/v1/budget`
23. `POST /adv/v1/budget/deposit`
24. `GET /adv/v1/upd`
25. `GET /adv/v1/payments`

### Медиа

26. `GET /adv/v1/count`
27. `GET /adv/v1/adverts`
28. `GET /adv/v1/advert`

### Статистика

29. `GET /adv/v3/fullstats`
30. `POST /adv/v1/stats`
31. `POST /adv/v0/normquery/stats`
32. `POST /adv/v1/normquery/stats`

### Календарь акций

33. `GET /api/v1/calendar/promotions`
34. `GET /api/v1/calendar/promotions/details`
35. `GET /api/v1/calendar/promotions/nomenclatures`
36. `POST /api/v1/calendar/promotions/upload`
