#!/usr/bin/env python3
"""GET /api/v1/calendar/promotions
Раздел: Marketing
Источник: promo-calendar.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://dp-calendar-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v1/calendar/promotions"

    # Обязательные query-параметры: startDateTime, endDateTime, allPromo
    # Обязательные поля body: нет
    # Опциональные query-параметры: limit, offset
    # Опциональные поля body: нет
    params = {
        "startDateTime": "2026-01-01T00:00:00Z",
        "endDateTime": "2026-01-01T00:00:00Z",
        "allPromo": false
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
