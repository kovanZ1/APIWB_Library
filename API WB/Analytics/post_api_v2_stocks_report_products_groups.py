#!/usr/bin/env python3
"""POST /api/v2/stocks-report/products/groups
Раздел: Analytics
Источник: stock-history.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v2/stocks-report/products/groups"

    # Обязательные query-параметры: нет
    # Обязательные поля body: currentPeriod, stockType, skipDeletedNm, availabilityFilters, orderBy, offset
    # Опциональные query-параметры: нет
    # Опциональные поля body: nmIDs, subjectIDs, brandNames, tagIDs, limit
    params = None
    payload = {
        "currentPeriod": {
            "start": "2026-01-01",
            "end": "2026-01-31"
        },
        "stockType": "wb",
        "skipDeletedNm": true,
        "availabilityFilters": [
            "ALL"
        ],
        "orderBy": {
            "field": "orders",
            "mode": "desc"
        },
        "offset": 0
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
