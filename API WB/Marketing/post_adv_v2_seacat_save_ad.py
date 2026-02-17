#!/usr/bin/env python3
"""POST /adv/v2/seacat/save-ad
Раздел: Marketing
Источник: campaign-creation.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/adv/v2/seacat/save-ad"

    # Обязательные query-параметры: нет
    # Обязательные поля body: нет
    # Опциональные query-параметры: нет
    # Опциональные поля body: name, nms, bid_type, payment_type, placement_types
    params = None
    payload = {
        "name": "Телефоны",
        "nms": [
            146168367
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
