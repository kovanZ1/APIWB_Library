#!/usr/bin/env python3
"""POST /api/v2/nm-report/downloads
Раздел: Analytics
Источник: seller-analytics-csv.md"""

import os
import requests

TOKEN = os.getenv("WB_API_TOKEN", "YOUR_WB_TOKEN")
BASE_URL = "https://seller-analytics-api.wildberries.ru"

def main() -> None:
    headers = {"Authorization": TOKEN}

    url = f"{BASE_URL}/api/v2/nm-report/downloads"

    # Обязательные query-параметры: нет
    # Обязательные поля body: id, reportType, params, startDate, endDate, currentPeriod, subjectIds, orderBy, positionCluster, topOrderBy, limit, stockType, skipDeletedNm, availabilityFilters
    # Опциональные query-параметры: нет
    # Опциональные поля body: userReportName, nmIDs, brandNames, tagIds, timezone, aggregationLevel, pastPeriod, nmIds, includeSubstitutedSKUs, includeSearchTexts, subjectId, brandName, tagId, subjectIDs, tagIDs
    params = None
    payload = {
        "id": "06eae887-9d9f-491f-b16a-bb1766fcb8d2",
        "reportType": "DETAIL_HISTORY_REPORT",
        "params": {
            "startDate": "2026-01-01",
            "endDate": "2026-01-31"
        }
    }
    # Для других reportType состав params меняется (см. seller-analytics-csv.md).

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
