#!/usr/bin/env python3
"""POST /api/v2/stocks-report/products/sizes
Раздел: Analytics
Источник: stock-history.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v2/stocks-report/products/sizes"

    # Обязательные query-параметры: нет
    # Обязательные поля body: nmID, currentPeriod, stockType, orderBy, includeOffice
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
    payload = {
        "nmID": 123456789,
        "currentPeriod": {
            "start": "2026-01-01",
            "end": "2026-01-31"
        },
        "stockType": "wb",
        "orderBy": {
            "field": "orders",
            "mode": "desc"
        },
        "includeOffice": "value"
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
