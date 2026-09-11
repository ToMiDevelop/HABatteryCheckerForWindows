# basic imports

import requests
from datetime import datetime
import os
from typing import cast

class HAData:
    def __init__(self):
        #haToken = os.getenv("HA_TOKEN")
        self.haToken = cast(str, os.getenv("HA_TOKEN"))
        self.haUrl = cast(str, os.getenv("HA_URL"))
        self.headers = {
            "Authorization": f"Bearer {self.haToken}",
            "Content-Type": "application/json"
        }

    def requestOne(self,
                   entity_id: str
    ) -> requests.Response | None:
        try:
            response = requests.get(
                url=f"{self.haUrl}/api/states/{entity_id}",
                headers=self.headers,
                timeout=10,
                verify=False
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching {entity_id} data: {e}")
            return None

    def requestHistory(self,
                    entity_id: str,
                    startTime: datetime,
                    endTime: datetime
    ) -> requests.Response | None:
        try:
            response = requests.get(
                url = f"{self.haUrl}/api/history/period/{startTime.isoformat()}",
                headers = self.headers,
                params = {
                    "filter_entity_id": entity_id,
                    "end_time": endTime.isoformat()
                },
                timeout = 10,
                verify=False
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching {entity_id} data: {e}")
            return None