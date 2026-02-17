# Финансовые отчёты

Базовый домен: `https://statistics-api.wildberries.ru`

---

## GET `/api/v5/supplier/reportDetailByPeriod`

**Назначение:** детализации к отчётам реализации (продажи по реализации).

### Особенности

- Данные доступны с **2024-01-29**.
- Поддерживается постраничная выгрузка через `rrdid`:
  1. первый запрос с `rrdid=0`
  2. следующий запрос с `rrdid` из поля `rrd_id` последней строки предыдущего ответа
  3. завершение выгрузки — ответ `204`

### Лимит

- `1 мин`: 1 запрос
- интервал: 1 мин
- всплеск: 1

### Пример запроса

```bash
curl -G "https://statistics-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod" \
  -H "Authorization: $WB_API_TOKEN" \
  --data-urlencode "dateFrom=2026-01-01" \
  --data-urlencode "dateTo=2026-01-31" \
  --data-urlencode "limit=100000" \
  --data-urlencode "rrdid=0" \
  --data-urlencode "period=weekly"
```

### Query-параметры

| Параметр | Тип | Обяз. | Ограничения и описание |
|---|---|---|---|
| `dateFrom` | date-time | да | Начальная дата отчёта (RFC3339, дата или дата-время, МСК UTC+3) |
| `dateTo` | date-time | да | Конечная дата отчёта |
| `limit` | integer | нет | Количество строк, default `100000`, max `100000` |
| `rrdid` | integer | нет | ID строки отчёта для выгрузки частями, default `0` |
| `period` | enum | нет | `weekly` (default) или `daily` |

### Ответ `200`

Тип: `array<DetailReportItem>`.

Ниже поля строки `DetailReportItem`:

#### Идентификация отчёта и периода

| Поле | Тип | Описание |
|---|---|---|
| `realizationreport_id` | integer | Номер отчёта |
| `date_from` | date | Дата начала отчётного периода |
| `date_to` | date | Дата конца отчётного периода |
| `create_dt` | date | Дата формирования отчёта |
| `currency_name` | string | Валюта отчёта |
| `suppliercontract_code` | object\|null | Договор |
| `rrd_id` | integer | Номер строки (ключ пагинации) |

#### Товар и поставка

| Поле | Тип | Описание |
|---|---|---|
| `gi_id` | integer | Номер поставки |
| `subject_name` | string | Предмет |
| `nm_id` | integer | Артикул WB |
| `brand_name` | string | Бренд |
| `sa_name` | string | Артикул продавца |
| `ts_name` | string | Размер |
| `barcode` | string | Баркод |
| `shk_id` | integer | Штрихкод |
| `sticker_id` | string | Цифровое значение стикера |
| `assembly_id` | integer | Номер сборочного задания |
| `kiz` | string | Код маркировки (если есть) |
| `srid` | string | Уникальный ID заказа |
| `order_uid` | string | ID транзакции корзины |
| `trbx_id` | string | Номер короба для обработки товара |

#### Цены, скидки и комиссии

| Поле | Тип | Описание |
|---|---|---|
| `retail_price` | number | Розничная цена |
| `retail_amount` | number | Реализовано WB (Пр) |
| `sale_percent` | integer | Согласованный продуктовый дисконт, % |
| `commission_percent` | number | Размер кВВ, % |
| `retail_price_withdisc_rub` | number | Розничная цена с учётом согласованной скидки |
| `product_discount_for_report` | number | Итоговая согласованная скидка, % |
| `supplier_promo` | number | Промокод, % |
| `ppvz_spp_prc` | number | Скидка постоянного покупателя (СПП), % |
| `ppvz_kvw_prc_base` | number | Базовый кВВ без НДС, % |
| `ppvz_kvw_prc` | number | Итоговый кВВ без НДС, % |
| `sup_rating_prc_up` | number | Снижение кВВ из-за рейтинга, % |
| `is_kgvp_v2` | number | Снижение кВВ из-за акции, % |
| `ppvz_sales_commission` | number | Вознаграждение с продаж до вычета услуг поверенного, без НДС |
| `ppvz_for_pay` | number | К перечислению продавцу |
| `ppvz_reward` | number | Возмещение за выдачу и возврат на ПВЗ |
| `ppvz_vw` | number | Вознаграждение WB (ВВ), без НДС |
| `ppvz_vw_nds` | number | НДС с вознаграждения WB |

#### Эквайринг и платежи

| Поле | Тип | Описание |
|---|---|---|
| `acquiring_fee` | number | Эквайринг / комиссии за организацию платежей |
| `acquiring_percent` | number | Размер комиссии эквайринга, % |
| `payment_processing` | string | Тип платежа по эквайрингу |
| `acquiring_bank` | string | Банк-эквайер |
| `payment_schedule` | number | Разовое изменение срока перечисления |

#### Логистика, склад, хранение и удержания

| Поле | Тип | Описание |
|---|---|---|
| `office_name` | string | Склад |
| `gi_box_type_name` | string | Тип коробов |
| `delivery_amount` | integer | Количество доставок |
| `return_amount` | integer | Количество возвратов |
| `delivery_rub` | number | Услуги по доставке |
| `rebill_logistic_cost` | number | Возмещение издержек по перевозке/складским операциям |
| `rebill_logistic_org` | string | Организатор перевозки |
| `storage_fee` | number | Хранение |
| `deduction` | number | Удержания |
| `acceptance` | number | Операции на приёмке |
| `penalty` | number | Общая сумма штрафов |
| `additional_payment` | number | Корректировка вознаграждения WB |

#### Даты и статусы

| Поле | Тип | Описание |
|---|---|---|
| `doc_type_name` | string | Тип документа |
| `supplier_oper_name` | string | Обоснование для оплаты |
| `order_dt` | date-time | Дата заказа |
| `sale_dt` | date-time | Дата продажи |
| `rr_dt` | date | Дата операции |
| `site_country` | string | Страна продажи |
| `srv_dbs` | boolean | Признак услуги платной доставки |
| `report_type` | enum | Тип отчёта: `1` стандартный, `2` уведомление о выкупе, `3`/`4` для Грузии |
| `is_legal_entity` | boolean | Признак B2B-продажи |

#### Программы лояльности, акции, промокоды

| Поле | Тип | Описание |
|---|---|---|
| `installment_cofinancing_amount` | number | Скидка по программе софинансирования |
| `wibes_wb_discount_percent` | number | Скидка Wibes, % |
| `cashback_amount` | number | Сумма удержаний за начисленные баллы |
| `cashback_discount` | number | Компенсация скидки по программе лояльности |
| `cashback_commission_change` | number | Стоимость участия в программе лояльности |
| `seller_promo_id` | integer | ID собственной акции продавца |
| `seller_promo_discount` | number | Скидка по собственной акции, % |
| `loyalty_id` | integer | ID скидки лояльности продавца |
| `loyalty_discount` | number | Размер скидки лояльности, % |
| `uuid_promocode` | string | ID промокода |
| `sale_price_promocode_discount_prc` | number | Скидка за промокод, % |

### Ответ `204`

- Нет данных (часто используется как признак завершения постраничной выгрузки по `rrdid`).

### Ошибки

- `400` — `response400rDBP` (например, отсутствует `dateTo`)
- `401`
- `429`
