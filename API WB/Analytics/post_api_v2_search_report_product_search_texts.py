#!/usr/bin/env python3
"""POST /api/v2/search-report/product/search-texts
Раздел: Analytics
Источник: search-queries.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v2/search-report/product/search-texts"

    # Обязательные query-параметры: нет
    # Обязательные поля body: currentPeriod, nmIds, topOrderBy, orderBy, limit
    # Опциональные query-параметры: нет
    # Опциональные поля body: pastPeriod, includeSubstitutedSKUs, includeSearchTexts
    params = None
    payload = {
        "currentPeriod": {
            "start": "2026-01-01",
            "end": "2026-01-31"
        },
        "nmIds": [
            123456789
        ],
        "topOrderBy": "orders",
        "orderBy": {
            "field": "orders",
            "mode": "desc"
        },
        "limit": 10
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
