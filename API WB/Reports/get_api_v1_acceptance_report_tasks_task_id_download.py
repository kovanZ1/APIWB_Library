#!/usr/bin/env python3
"""GET /api/v1/acceptance_report/tasks/{task_id}/download
Раздел: Reports
Источник: paid-acceptance.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    task_id = "06e06887-9d9f-491f-b16a-bb1766fcb8d2"
    url = f"{BASE_URL}/api/v1/acceptance_report/tasks/{task_id}/download"

    # Обязательные query-параметры: нет
    # Обязательные поля body: нет
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
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
