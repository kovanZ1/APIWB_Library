#!/usr/bin/env python3
"""POST /api/analytics/v3/sales-funnel/products
Раздел: Analytics
Источник: sales-funnel.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/analytics/v3/sales-funnel/products"

    # Обязательные query-параметры: нет
    # Обязательные поля body: selectedPeriod, field, mode
    # Опциональные query-параметры: нет
    # Опциональные поля body: pastPeriod, nmIds, brandNames, subjectIds, tagIds, skipDeletedNm, orderBy, limit, offset
    params = None
    payload = {
        "selectedPeriod": {
            "start": "2026-01-01",
            "end": "2026-01-31"
        },
        "field": "orders",
        "mode": "desc"
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
