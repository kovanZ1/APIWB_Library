#!/usr/bin/env python3
"""POST /api/advert/v1/bids/min
Раздел: Marketing
Источник: campaign-creation.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/advert/v1/bids/min"

    # Обязательные query-параметры: нет
    # Обязательные поля body: advert_id, nm_ids, payment_type, placement_types
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
    payload = {
        "advert_id": 123456789,
        "nm_ids": [
            123456789
        ],
        "payment_type": "cpm",
        "placement_types": [
            "search"
        ]
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
