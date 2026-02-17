#!/usr/bin/env python3
"""POST /adv/v0/normquery/set-minus
Раздел: Marketing
Источник: search-clusters.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/adv/v0/normquery/set-minus"

    # Обязательные query-параметры: нет
    # Обязательные поля body: advert_id, nm_id, norm_queries
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
    payload = {
        "advert_id": 123456789,
        "nm_id": 123456789,
        "norm_queries": "value"
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
