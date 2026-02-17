#!/usr/bin/env python3
"""POST /api/v2/nm-report/downloads/retry
Раздел: Analytics
Источник: seller-analytics-csv.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v2/nm-report/downloads/retry"

    # Обязательные query-параметры: нет
    # Обязательные поля body: downloadId
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
    payload = {
        "downloadId": "06eae887-9d9f-491f-b16a-bb1766fcb8d2"
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
