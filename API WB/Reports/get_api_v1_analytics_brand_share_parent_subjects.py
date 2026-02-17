#!/usr/bin/env python3
"""GET /api/v1/analytics/brand-share/parent-subjects
Раздел: Reports
Источник: brand-share.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v1/analytics/brand-share/parent-subjects"

    # Обязательные query-параметры: brand, dateFrom, dateTo
    # Обязательные поля body: нет
    # Опциональные query-параметры: locale
    # Опциональные поля body: нет
    params = {
        "brand": "example",
        "dateFrom": "2026-01-01",
        "dateTo": "2026-01-31"
    }
    payload = None

    response = requests.request(
        "GET",
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
