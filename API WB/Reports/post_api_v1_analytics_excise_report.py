#!/usr/bin/env python3
"""POST /api/v1/analytics/excise-report
Раздел: Reports
Источник: excise-report.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v1/analytics/excise-report"

    # Обязательные query-параметры: нет
    # Обязательные поля body: нет
    # Опциональные query-параметры: dateFrom, dateTo
    # Опциональные поля body: countries
    params = None
    payload = None
    # В этом примере body не обязателен по документации.

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
