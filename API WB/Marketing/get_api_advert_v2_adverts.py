#!/usr/bin/env python3
"""GET /api/advert/v2/adverts
Раздел: Marketing
Источник: campaigns.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/advert/v2/adverts"

    # Обязательные query-параметры: нет
    # Обязательные поля body: нет
    # Опциональные query-параметры: ids, statuses, payment_type
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
