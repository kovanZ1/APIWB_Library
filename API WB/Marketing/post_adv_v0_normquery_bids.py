#!/usr/bin/env python3
"""POST /adv/v0/normquery/bids
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
                "advert_id": 123456789,
                "nm_id": 123456789,
                "norm_query": 250,
                "bid": 123456789
            }
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
