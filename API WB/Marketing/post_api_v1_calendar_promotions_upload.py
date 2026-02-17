#!/usr/bin/env python3
"""POST /api/v1/calendar/promotions/upload
Раздел: Marketing
Источник: promo-calendar.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://dp-calendar-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v1/calendar/promotions/upload"

    # Обязательные query-параметры: нет
    # Обязательные поля body: data.promotionID, data.nomenclatures
    # Опциональные query-параметры: нет
    # Опциональные поля body: data.uploadNow
    params = None
    payload = {
        "data": {
            "promotionID": 123456789,
            "nomenclatures": "value"
        }
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=params,
        json=payload,
        timeout=30,
    )

    print("Status:", response.status_code)
    try:
        print(response.json())
    except ValueError:
        print(response.text)

if __name__ == "__main__":
    main()
