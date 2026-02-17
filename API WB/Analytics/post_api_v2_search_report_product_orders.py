#!/usr/bin/env python3
"""POST /api/v2/search-report/product/orders
Раздел: Analytics
Источник: search-queries.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v2/search-report/product/orders"

    # Обязательные query-параметры: нет
    # Обязательные поля body: period, nmId, searchTexts
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
    payload = {
        "period": {
            "start": "2026-01-01",
            "end": "2026-01-31"
        },
        "nmId": 123456789,
        "searchTexts": [
            "пример запроса"
        ]
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
