#!/usr/bin/env python3
"""POST /adv/v1/budget/deposit
Раздел: Marketing
Источник: finance.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/adv/v1/budget/deposit"

    # Обязательные query-параметры: id
    # Обязательные поля body: нет
    # Опциональные query-параметры: нет
    # Опциональные поля body: sum, type, return
    params = {
        "id": 123456789
    }
    payload = None
    # В этом примере body не обязателен по документации.

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
