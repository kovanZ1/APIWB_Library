# Баланс

Базовый домен: `https://finance-api.wildberries.ru`

---

## GET `/api/v1/account/balance`

**Назначение:** получить данные виджета баланса продавца с главной страницы портала продавцов.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример запроса

```bash
curl -X GET "https://finance-api.wildberries.ru/api/v1/account/balance" \
  -H "Authorization: $WB_API_TOKEN"
```

### Параметры

Параметров запроса нет.

### Ответ `200`

| Поле | Тип | Описание |
|---|---|---|
| `currency` | string | Валюта (пример: `RUB`) |
| `current` | number | Текущий баланс продавца |
| `for_withdraw` | number | Сумма, доступная к выводу |

Пример:

```json
{
  "currency": "RUB",
  "current": 10196.21,
  "for_withdraw": 6395.8
}
```

### Ошибки

- `401` — не авторизован
- `429` — слишком много запросов
