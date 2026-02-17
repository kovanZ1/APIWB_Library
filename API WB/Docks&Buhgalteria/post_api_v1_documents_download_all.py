#!/usr/bin/env python3
"""POST /api/v1/documents/download/all
Раздел: Docks&Buhgalteria
Источник: documents.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://documents-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v1/documents/download/all"

    # Обязательные query-параметры: нет
    # Обязательные поля body: params, serviceName, extension
    # Опциональные query-параметры: нет
    # Опциональные поля body: нет
    params = None
    payload = {
        "params": "value",
        "serviceName": "redeem-notification-44841941",
        "extension": "zip"
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
