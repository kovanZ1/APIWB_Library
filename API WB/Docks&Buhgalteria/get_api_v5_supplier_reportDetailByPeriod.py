#!/usr/bin/env python3
"""GET /api/v5/supplier/reportDetailByPeriod
Раздел: Docks&Buhgalteria
Источник: financial-reports.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://statistics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v5/supplier/reportDetailByPeriod"

    # Обязательные query-параметры: dateFrom, dateTo
    # Обязательные поля body: нет
    # Опциональные query-параметры: limit, rrdid, period
    # Опциональные поля body: нет
    params = {
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
