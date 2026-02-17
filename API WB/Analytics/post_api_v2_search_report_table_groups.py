#!/usr/bin/env python3
"""POST /api/v2/search-report/table/groups
Раздел: Analytics
Источник: search-queries.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v2/search-report/table/groups"

    # Обязательные query-параметры: нет
    # Обязательные поля body: currentPeriod, orderBy, positionCluster, limit, offset
    # Опциональные query-параметры: нет
    # Опциональные поля body: pastPeriod, nmIds, subjectIds, brandNames, tagIds, includeSubstitutedSKUs, includeSearchTexts
    params = None
    payload = {
        "currentPeriod": {
            "start": "2026-01-01",
            "end": "2026-01-31"
        },
        "orderBy": {
            "field": "orders",
            "mode": "desc"
        },
        "positionCluster": "all",
        "limit": 10,
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
