# custom imports

from database import _BatteryPercentClass, _LQIClass, _RSSIClass, HADBData
from homeassistant import HAData
from mytoastspl import MyToastsPL
from datetime import datetime
from spreadsheetprocessor import ExcelProcessor

class NormalRun:
    def __init__(self):
        self.excelProcessor = ExcelProcessor()
        self.devicesData = self.excelProcessor.processSheets()
        self.devicesBatteryValueList = self.devicesData["devicesBatteryValueList"]
        self.devicesBatteryTypeList = self.devicesData["devicesBatteryTypeList"]
        self.devicesLQIList = self.devicesData["devicesLQIList"]
        self.devicesRSSIList = self.devicesData["devicesRSSIList"]
        self.haData = HAData()
        self.hadbData = HADBData()
        self.myToasts = MyToastsPL()
        self.thresholdDict = self.devicesData["batteryThreshold"]
        self.batteryThreshold = self.thresholdDict["batteryThreshold"]

    def normalBatteryValueUpdate(self):
        for name, entity_id in self.devicesBatteryValueList.items():
            try:
                response = self.haData.requestOne(
                    entity_id = entity_id
                )
                if response is not None:
                    if response.json():
                        data = response.json().get("state")
                        if data is not None:
                            if data == "unavailable":
                                print(f"{name}: battery empty :-(")
                                #self.myToasts.emptyBattery(name, entity_id)
                                entry = _BatteryPercentClass(
                                    name = name,
                                    entity_id = entity_id,
                                    value = data,
                                    date = datetime.now()
                                )
                                self.hadbData.addBatteryPercentEntry(entry)
                            else:
                                try:
                                    data = int(float(data))
                                    print(f"{name}: battery {data}%")
                                except ValueError:
                                    continue
                                if data == 0:
                                    #self.myToasts.emptyBattery(name, entity_id)
                                    entry = _BatteryPercentClass(
                                        name=name,
                                        entity_id=entity_id,
                                        value = str(data),
                                        date=datetime.now()
                                    )
                                    self.hadbData.addBatteryPercentEntry(entry)
                                else:
                                    if data <= self.batteryThreshold:
                                        #self.myToasts.lowBattery(name, entity_id, data)
                                        entry = _BatteryPercentClass(
                                            name=name,
                                            entity_id=entity_id,
                                            value=str(data),
                                            date=datetime.now()
                                        )
                                        self.hadbData.addBatteryPercentEntry(entry)
                                    else:
                                        #self.myToasts.normalBattery(name, entity_id, data)
                                        entry = _BatteryPercentClass(
                                            name=name,
                                            entity_id=entity_id,
                                            value=str(data),
                                            date=datetime.now()
                                        )
                                        self.hadbData.addBatteryPercentEntry(entry)
                        else:
                            print(f"No battery state for {entity_id}.")
                    else:
                        print(f"No battery state for {entity_id}.")
                else:
                    print(f"No battery state for {entity_id}.")
            except Exception as e:
                print(f"Error while fetching data for {entity_id}: {e}")

    def normalLQIUpdate(self):
        for name, entity_id in self.devicesLQIList.items():
            try:
                response = self.haData.requestOne(
                    entity_id = entity_id
                )
                if response is not None:
                    if response.json():
                        data = response.json().get("state")
                        if data is not None:
                            rawDate = response.json().get("last_updated")
                            if rawDate:
                                finalDate = datetime.fromisoformat(rawDate.replace("Z", "+00:00"))
                                entity = _LQIClass(
                                    name = name,
                                    entity_id = entity_id,
                                    value = data,
                                    date = finalDate
                                )
                                self.hadbData.addLQIEntry(entity)
                            else:
                                print(f"No LQI state for {entity_id}.")
                        else:
                            print(f"No LQI state for {entity_id}.")
                    else:
                        print(f"No LQI state for {entity_id}.")
            except Exception as e:
                print(f"Error while fetching data for {entity_id}: {e}")

    def normaRSSIIUpdate(self):
        for name, entity_id in self.devicesRSSIList.items():
            try:
                response = self.haData.requestOne(
                    entity_id = entity_id
                )
                if response is not None:
                    if response.json():
                        data = response.json().get("state")
                        if data is not None:
                            rawDate = response.json().get("last_updated")
                            if rawDate:
                                finalDate = datetime.fromisoformat(rawDate.replace("Z", "+00:00"))
                                entity = _RSSIClass(
                                    name = name,
                                    entity_id = entity_id,
                                    value = data,
                                    date = finalDate
                                )
                                self.hadbData.addRSSIEntry(entity)
                            else:
                                print(f"No RSSI state for {entity_id}.")
                        else:
                            print(f"No RSSI state for {entity_id}.")
                    else:
                        print(f"No RSSI state for {entity_id}.")
            except Exception as e:
                print(f"Error while fetching RSSI data for {entity_id}: {e}")

    def normalBatteryValueUpdateToasts(self):
        for name, entity_id in self.devicesBatteryValueList.items():
            try:
                response = self.haData.requestOne(
                    entity_id = entity_id
                )
                if response is not None:
                    if response.json():
                        data = response.json().get("state")
                        if data is not None:
                            if data == "unavailable":
                                print(f"{name}: battery empty :-(")
                                self.myToasts.emptyBattery(name, entity_id)
                                entry = _BatteryPercentClass(
                                    name = name,
                                    entity_id = entity_id,
                                    value = data,
                                    date = datetime.now()
                                )
                                self.hadbData.addBatteryPercentEntry(entry)
                            else:
                                try:
                                    data = int(float(data))
                                    print(f"{name}: battery {data}%")
                                except ValueError:
                                    continue
                                if data == 0:
                                    self.myToasts.emptyBattery(name, entity_id)
                                    entry = _BatteryPercentClass(
                                        name=name,
                                        entity_id=entity_id,
                                        value = str(data),
                                        date=datetime.now()
                                    )
                                    self.hadbData.addBatteryPercentEntry(entry)
                                else:
                                    if data <= self.batteryThreshold:
                                        self.myToasts.lowBattery(name, entity_id, data)
                                        entry = _BatteryPercentClass(
                                            name=name,
                                            entity_id=entity_id,
                                            value=str(data),
                                            date=datetime.now()
                                        )
                                        self.hadbData.addBatteryPercentEntry(entry)
                                    else:
                                        self.myToasts.normalBattery(name, entity_id, data)
                                        entry = _BatteryPercentClass(
                                            name=name,
                                            entity_id=entity_id,
                                            value=str(data),
                                            date=datetime.now()
                                        )
                                        self.hadbData.addBatteryPercentEntry(entry)
                        else:
                            print(f"No battery state for {entity_id}.")
                    else:
                        print(f"No battery state for {entity_id}.")
                else:
                    print(f"No battery state for {entity_id}.")
            except Exception as e:
                print(f"Error while fetching data for {entity_id}: {e}")

    def geminiReport(self) -> None:
        from ai import Gemini
        from reporter import Reporter
        from reportsgui import ReportWindow
        gemini = Gemini(self.batteryThreshold)
        htmlReporter = Reporter(gemini.askGemini())
        htmlPath = htmlReporter.saveAnalysisToHml()
        reportWindow = ReportWindow(htmlPath)
        reportWindow.showReport()