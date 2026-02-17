#!/usr/bin/env python3
"""POST /adv/v0/rename
Раздел: Marketing
Источник: campaign-management.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/adv/v0/rename"

    # Обязательные query-параметры: нет
    # Обязательные поля body: advertId, name
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
    payload = {
        "advertId": 123456789,
        "name": "example"
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
