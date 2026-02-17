#!/usr/bin/env python3
"""GET /adv/v3/fullstats
Раздел: Marketing
Источник: statistics.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/adv/v3/fullstats"

    # Обязательные query-параметры: ids, beginDate, endDate
    # Обязательные поля body: нет
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = {
        "ids": "1234567,7654321",
        "beginDate": "2026-01-01",
        "endDate": "2026-01-31"
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
