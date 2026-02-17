#!/usr/bin/env python3
"""GET /api/analytics/v1/measurement-penalties
Раздел: Reports
Источник: deductions.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/analytics/v1/measurement-penalties"

    # Обязательные query-параметры: dateTo, limit
    # Обязательные поля body: нет
    # Опциональные query-параметры: dateFrom, offset
    # Опциональные поля body: нет
    params = {
        "dateTo": "2026-01-31",
        "limit": 10
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
