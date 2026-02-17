# Основные отчёты

Базовый домен: `https://statistics-api.wildberries.ru`

## Общие правила раздела

- Для `orders` и `sales` данные обновляются раз в 30 минут.
- Хранение данных по заказам/продажам: до 90 дней с момента оформления.
- Время в параметрах и полях (если зона не указана) трактуется как `UTC+3` (Москва).
- Формат `dateFrom`: RFC3339 (можно передавать только дату, либо дату со временем).

Примеры `dateFrom`:
- `2019-06-20`
- `2019-06-20T23:59:59`
- `2019-06-20T00:00:00.12345`
- `2017-03-25T00:00:00`

## Параметр `flag` (для `orders` и `sales`)

| Значение | Логика |
|---|---|
| `0` или не указан | выгрузка по `lastChangeDate >= dateFrom` |
| `1` | выгрузка за календарную дату `dateFrom` (время игнорируется) |

---

## 1) GET `/api/v1/supplier/incomes` (устаревший)

**Статус:** `deprecated`.

### Важно

В описании OpenAPI: метод будет удалён 11 марта (ссылка на release notes WB).

### Пример

```bash
curl -G "https://statistics-api.wildberries.ru/api/v1/supplier/incomes" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2026-01-01"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | date-time | да | Дата/время последнего изменения по поставке |

### Ответ `200`

Тип: `array<IncomesItem>`.

`IncomesItem`:
- `incomeId` — номер поставки
- `number` — номер УПД
- `date` — дата поступления
- `lastChangeDate` — дата обновления (ключ инкрементальной выгрузки)
- `supplierArticle`, `techSize`, `barcode`
- `quantity`, `totalPrice`
- `dateClose` — дата принятия поставки
- `warehouseName`, `nmId`, `status` (`Принято`)

### Ошибки

- `400` — `responseErrorStatistics`/`responseErrorStatistics2`
- `401`, `429`

---

## 2) GET `/api/v1/supplier/stocks`

**Назначение:** остатки товаров на складах WB.

### Особенности

- Отчёт может отставать от реальных изменений на несколько часов.
- Это только «срез сейчас», история остатков не хранится.
- Для полного выгрузки используйте пагинацию по `lastChangeDate` (лимит около 60000 строк на ответ).

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -G "https://statistics-api.wildberries.ru/api/v1/supplier/stocks" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2019-06-20"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | date-time | да | Дата/время последнего изменения по товару |

### Ответ `200`

Тип: `array<StocksItem>`.

Поля `StocksItem`:
- `lastChangeDate`
- `warehouseName`
- `supplierArticle`, `nmId`, `barcode`
- `quantity` — доступно к продаже
- `inWayToClient`, `inWayFromClient`
- `quantityFull` — полный остаток (= `quantity` + в пути)
- `category`, `subject`, `brand`, `techSize`
- `Price`, `Discount`
- `isSupply`, `isRealization`, `SCCode`

### Ошибки

- `400`, `401`, `429`

---

## 3) GET `/api/v1/supplier/orders`

**Назначение:** заказы (оперативный предварительный отчёт).

### Особенности

- 1 строка = 1 заказ = 1 сборочное задание = 1 единица товара.
- Для идентификации заказа WB рекомендует `srid`.
- Возможны отсутствующие записи по заказам без подтверждённой оплаты.
- Для полного финансового сверочного учёта используйте отчёты реализации.
- При `flag=0` условный лимит около 80000 строк на один ответ.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -G "https://statistics-api.wildberries.ru/api/v1/supplier/orders" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2026-01-01" \
  --data-urlencode "flag=0"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | date-time | да | Дата и время изменения по заказу |
| `flag` | integer | нет | Режим выгрузки (`0`/`1`) |

### Ответ `200`

Тип: `array<OrdersItem>`.

Ключевые поля `OrdersItem`:
- время: `date`, `lastChangeDate`, `cancelDate`
- география/склад: `warehouseName`, `warehouseType`, `countryName`, `oblastOkrugName`, `regionName`
- товар: `supplierArticle`, `nmId`, `barcode`, `category`, `subject`, `brand`, `techSize`
- поставка/контракт: `incomeID`, `isSupply`, `isRealization`
- финансы: `totalPrice`, `discountPercent`, `spp`, `finishedPrice`, `priceWithDisc`
- статус: `isCancel`
- идентификаторы: `sticker`, `gNumber`, `srid`

### Ошибки

- `400`, `401`, `429`

---

## 4) GET `/api/v1/supplier/sales`

**Назначение:** продажи и возвраты (оперативный предварительный отчёт).

### Особенности

- 1 строка = 1 продажа/возврат = 1 единица товара.
- Идентификатор заказа: `srid`.
- Для `flag=0` условный лимит 80000 строк.
- Поля `finishedPrice`, `priceWithDisc`, `forPay` могут временно быть `0` (асинхронная синхронизация до 24 часов).
- Для точных финансовых расчётов используйте детализацию отчётов реализации.

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример

```bash
curl -G "https://statistics-api.wildberries.ru/api/v1/supplier/sales" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2026-01-01" \
  --data-urlencode "flag=0"
```

### Query-параметры

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `dateFrom` | date-time | да | Дата и время изменения по продаже/возврату |
| `flag` | integer | нет | Режим выгрузки (`0`/`1`) |

### Ответ `200`

Тип: `array<SalesItem>`.

Ключевые поля `SalesItem`:
- время: `date`, `lastChangeDate`
- география/склад: `warehouseName`, `warehouseType`, `countryName`, `oblastOkrugName`, `regionName`
- товар: `supplierArticle`, `nmId`, `barcode`, `category`, `subject`, `brand`, `techSize`
- поставка/контракт: `incomeID`, `isSupply`, `isRealization`
- финансы: `totalPrice`, `discountPercent`, `spp`, `paymentSaleAmount`, `forPay`, `finishedPrice`, `priceWithDisc`
- тип операции: `saleID` (`S...` продажа, `R...` возврат)
- идентификаторы: `sticker`, `gNumber`, `srid`

### Ошибки

- `400`, `401`, `429`
