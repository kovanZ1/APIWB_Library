#!/usr/bin/env python3
"""PATCH /adv/v0/auction/nms
Раздел: Marketing
Источник: campaign-management.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/adv/v0/auction/nms"

    # Обязательные query-параметры: нет
    # Обязательные поля body: nms, advert_id
    # Опциональные query-параметры: нет
    # Опциональные поля body: nms.add, nms.delete
    params = None
    payload = {
        "nms": "value",
        "advert_id": 123456789
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
