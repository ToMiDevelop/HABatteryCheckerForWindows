# basic imports

from datetime import datetime, timedelta

# custom imports

from devices import devicesBatteryValueList, devicesBatteryTypeList, devicesLQIList, devicesRSSIList
from database import HADBData, _BatteryPercentClass, _BatteryTypeClass, _LQIClass, _RSSIClass
from homeassistant import HAData

# classes definitions

class InitialSeed:
    def __init__(self):
        self.devicesBatteryValueList = devicesBatteryValueList
        self.devicesBatteryTypeList = devicesBatteryTypeList
        self.devicesLQIList = devicesLQIList
        self.devicesRSSIList = devicesRSSIList
        self.haData = HAData()
        self.hadbData = HADBData()

    def seedBatteryValues(self):
        entries: list[_BatteryPercentClass] = []
        for name, entity_id in self.devicesBatteryValueList.items():
            try:
                endTime = datetime.now()
                startTime = endTime - timedelta(days=365)
                response = self.haData.requestHistory(
                    entity_id = entity_id,
                    startTime = startTime,
                    endTime = endTime
                )
                if response is not None:
                    if response.json():
                        data = response.json()[0]
                        for item in data:
                            rawState = item.get("state")
                            rawDate = item.get("last_updated")
                            if rawState in ("unavailable", "unknown", None):
                                rawState = "0"
                            if rawDate:
                                finalDate = datetime.fromisoformat(rawDate.replace("Z", "+00:00"))
                                entry = _BatteryPercentClass(
                                    name = name,
                                    entity_id = entity_id,
                                    value = rawState,
                                    date = finalDate
                                )
                                entries.append(entry)
                    else:
                        print(f"No history available for {entity_id}.")
                else:
                    print(f"No history available for {entity_id}.")
            except Exception as e:
                print(f"Error while fetching history for {entity_id}: {e}")
        self.hadbData.addBatteryPercentEntries(entries)

    def seedBatteryTypes(self):
        for name, entity_id in self.devicesBatteryTypeList.items():
            try:
                response = self.haData.requestOne(
                    entity_id = entity_id, )
                if response is not None:
                    if response.json():
                        rawDate = response.json().get("last_updated")
                        if rawDate is not None:
                            finalDate = datetime.fromisoformat(rawDate.replace("Z", "+00:00"))
                            entry = _BatteryTypeClass(
                                name = name,
                                entity_id = entity_id,
                                value = response.json()["state"],
                                date = finalDate
                            )
                            self.hadbData.addBatteryTypeEntry(entry)
                    else:
                        print(f"No battery type available for {entity_id}.")
                else:
                    print(f"No battery type available for {entity_id}.")
            except Exception as e:
                print(f"Error while fetching battery type for {entity_id}: {e}")

    def seedLQIValues(self):
        entries: list[_LQIClass] = []
        for name, entity_id in self.devicesLQIList.items():
            try:
                endTime = datetime.now()
                startTime = endTime - timedelta(days=365)
                response = self.haData.requestHistory(
                    entity_id = entity_id,
                    startTime = startTime,
                    endTime = endTime
                )
                if response is not None:
                    if response.json():
                        data = response.json()[0]
                        for item in data:
                            rawState = item.get("state")
                            rawDate = item.get("last_updated")
                            if rawState in ("unavailable", "unknown", None):
                                rawState = "0"
                            if rawDate:
                                finalDate = datetime.fromisoformat(rawDate.replace("Z", "+00:00"))
                                entry = _LQIClass(
                                    name = name,
                                    entity_id = entity_id,
                                    value = rawState,
                                    date = finalDate
                                )
                                entries.append(entry)
                    else:
                        print(f"No history available for {entity_id}.")
                else:
                    print(f"No history available for {entity_id}.")
            except Exception as e:
                print(f"Error while fetching history for {entity_id}: {e}")
        self.hadbData.addLQIEntries(entries)

    def seedRSSIValues(self):
        entries: list[_RSSIClass] = []
        for name, entity_id in self.devicesRSSIList.items():
            try:
                endTime = datetime.now()
                startTime = endTime - timedelta(days=365)
                response = self.haData.requestHistory(
                    entity_id = entity_id,
                    startTime = startTime,
                    endTime = endTime
                )
                if response is not None:
                    if response.json():
                        data = response.json()[0]
                        for item in data:
                            rawState = item.get("state")
                            rawDate = item.get("last_updated")
                            if rawState in ("unavailable", "unknown", None):
                                rawState = "0"
                            if rawDate:
                                finalDate = datetime.fromisoformat(rawDate.replace("Z", "+00:00"))
                                entry = _RSSIClass(
                                    name = name,
                                    entity_id = entity_id,
                                    value = rawState,
                                    date = finalDate
                                )
                                entries.append(entry)
                    else:
                        print(f"No history available for {entity_id}.")
                else:
                    print(f"No history available for {entity_id}.")
            except Exception as e:
                print(f"Error while fetching history for {entity_id}: {e}")
        self.hadbData.addRSSIEntries(entries)
