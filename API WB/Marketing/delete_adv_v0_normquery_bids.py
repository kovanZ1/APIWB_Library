#!/usr/bin/env python3
"""DELETE /adv/v0/normquery/bids
Раздел: Marketing
Источник: search-clusters.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://advert-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/adv/v0/normquery/bids"

    # Обязательные query-параметры: нет
    # Обязательные поля body: bids, bids[].advert_id, bids[].nm_id, bids[].norm_query, bids[].bid
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
    payload = {
        "bids": [
            {
                "advert_id": 1825035,
                "nm_id": 983512347,
                "norm_query": "Фраза 1",
                "bid": 1000
            }
        ]
    }

    response = requests.request(
        "DELETE",
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
