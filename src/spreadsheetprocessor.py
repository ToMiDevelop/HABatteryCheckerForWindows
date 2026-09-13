import sys
from pathlib import Path
from typing import Any
import openpyxl

def getBase_dir() -> Path:
    """Returns app main directory (where .exe or main.py is kept)."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable)
    return Path(__file__).parent

class ExcelProcessor:
    def __init__(self, fileName: str = "devices.xlsx"):
        self.BASE_DIR = getBase_dir()
        self.DATA_DIR = self.BASE_DIR / "devices"
        self.FILE_PATH = self.DATA_DIR / fileName

    def processSheets(self) -> dict[str, Any]:
        """
        Opens spreadsheet and iterates on all sheets
        and returns a dictionary of dictionaries like bellow.
        devices = {
            "devicesBatteryValueList": {
                "Device 1 Name": "Device 1 entity id",
                "Device 2 Name": "Device 2 entity id",
                "Device 3 Name": "Device 3 entity id",
                ...
                "Device n Name": "Device n entity id",
            },
            "devicesBatteryTypeList": {
                "Device 1 Name": "Device 1 entity id",
                "Device 2 Name": "Device 2 entity id",
                "Device 3 Name": "Device 3 entity id",
                ...
                "Device n Name": "Device n entity id",
            },
            "devicesLQIList": {
                "Device 1 Name": "Device 1 entity id",
                "Device 2 Name": "Device 2 entity id",
                "Device 3 Name": "Device 3 entity id",
                ...
                "Device n Name": "Device n entity id",
            },
            "devicesRSSIList": {
                "Device 1 Name": "Device 1 entity id",
                "Device 2 Name": "Device 2 entity id",
                "Device 3 Name": "Device 3 entity id",
                ...
                "Device n Name": "Device n entity id",
            },
            "batteryThreshold": 10
        }
        """

        # check if we have the Excel file
        if not self.FILE_PATH.exists():
            raise FileNotFoundError(
                f"File not found: {self.FILE_PATH}\n"
                f"App needs devices.xlsx in: {self.DATA_DIR}"
            )

        # data_only=True forces to read only values - not formulas behind 'em
        # trying to open workbook
        workbook = None
        try:
            workbook = openpyxl.load_workbook(self.FILE_PATH, data_only=True)
        except Exception as e:
            print(f"Error opening file {self.FILE_PATH}: {e}")

        # Allocating a whole dict to be returned
        wholeDict: dict[str, Any] = {}

        # Processing the workbook
        if workbook is not None:
            for sheetName in workbook.sheetnames:
                if sheetName == "batteryThreshold":
                    sheet = workbook[sheetName]
                    thresholdDict: dict[str, int] = {}
                    rawName = sheet["A2"].value
                    rawValue = sheet["B2"].value
                    if rawName is not None and rawValue is not None:
                        thresholdDict[str(rawName).strip()] = int(str(rawValue).strip())
                    wholeDict[f"{sheetName}"] = thresholdDict
                else:
                    sheet = workbook[sheetName]
                    devicesDict: dict[str, str] = {}
                    # We do not use headers (min_row=2) and read data only from first 2 columns
                    for row in sheet.iter_rows(min_row=2, max_col=2, values_only=True):
                        # We bypass empty or not full rows
                        if not row or row[0] is None or row[1] is None:
                            continue
                        deviceName = str(row[0]).strip()
                        entityId = str(row[1]).strip()
                        devicesDict[deviceName] = entityId
                        wholeDict[f"{sheetName}"] = devicesDict
            return wholeDict
        else:
            raise FileNotFoundError(
                f"File not found: {self.FILE_PATH}\n"
            )