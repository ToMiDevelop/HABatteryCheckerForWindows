# basic imports

import requests
from datetime import datetime
import os
from typing import cast


class HAData:
    def __init__(self):
        self.haToken = cast(str, os.getenv("HA_TOKEN"))
        # Czyszczenie adresu z ewentualnego slasha na końcu
        raw_url = cast(str, os.getenv("HA_URL", ""))
        self.haUrl = raw_url.rstrip("/")

        self.headers = {
            "Authorization": f"Bearer {self.haToken}",
            "Content-Type": "application/json"
        }

    def requestOne(self, entity_id: str) -> requests.Response | None:
        try:
            response = requests.get(
                url=f"{self.haUrl}/api/states/{entity_id}",
                headers=self.headers,
                timeout=10,
                verify=False
            )
            response.raise_for_status()  # Wyrzuci błąd dla statusów 4xx/5xx zamiast próbować czytać JSON
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching data for {entity_id}: {e}")
            return None

    def requestHistory(self, entity_id: str, startTime: datetime, endTime: datetime) -> requests.Response | None:
        try:
            # WAŻNE: Dodany slash przed znakiem zapytania w okresie historii
            url = f"{self.haUrl}/api/history/period/{startTime.isoformat()}"
            response = requests.get(
                url=url,
                headers=self.headers,
                params={
                    "filter_entity_id": entity_id,
                    "end_time": endTime.isoformat()
                },
                timeout=10,
                verify=False
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching history data for {entity_id}: {e}")
            return None