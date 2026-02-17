#!/usr/bin/env python3
"""PATCH /api/advert/v1/bids
Раздел: Marketing
Источник: campaign-management.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/advert/v1/bids"

    # Обязательные query-параметры: нет
    # Обязательные поля body: bids, advert_id, nm_bids, nm_id, bid_kopecks, placement
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
    payload = {
        "bids": [
            123456789
        ],
        "advert_id": 123456789,
        "nm_bids": [
            123456789
        ],
        "nm_id": 123456789,
        "bid_kopecks": 250,
        "placement": "value"
    }

    response = requests.request(
        "PATCH",
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
