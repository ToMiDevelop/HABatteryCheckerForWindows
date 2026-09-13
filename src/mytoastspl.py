# basic imports

from windows_toasts import WindowsToaster, Toast, ToastDuration
from messages import toastsMessage
from typing import Any
import threading

class MyToastsPL:
    def __init__(self):
        self.Toaster = WindowsToaster(f"{toastsMessage["plToastTitle"]}")
        self.Toaster.clear_toasts()
        self.report_requested = threading.Event()

    def _handleToastClick(self, even_args: Any) -> None:
        self.report_requested.set()

    def clearToasts(self) -> None:
        self.Toaster.clear_toasts()

    def emptyBattery(
            self,
            name: str,
            entity_id: str,
    ) -> None:
        toast = Toast()
        toast.text_fields=[
            f"{name}",
            f"{toastsMessage["plEmptyBattery"]}"
        ]
        toast.group = entity_id
        toast.duration = ToastDuration.Long
        toast.on_activated = self._handleToastClick
        self.Toaster.show_toast(toast)

    def lowBattery(
            self,
            name: str,
            entity_id: str,
            battery: int
    ) -> None:
        toast = Toast()
        toast.text_fields=[
            f"{name}",
            f"{toastsMessage["plLowBattery"]}: {battery}%"
        ]
        toast.group = entity_id
        toast.duration = ToastDuration.Long
        toast.on_activated = self._handleToastClick
        self.Toaster.show_toast(toast)

    def normalBattery(
            self,
            name: str,
            entity_id: str,
            battery: int
    ) -> None:
        toast = Toast()
        toast.text_fields=[
            f"{name}",
            f"{toastsMessage["plNormalBattery"]}: {battery}%"
        ]
        toast.group = entity_id
        toast.duration = ToastDuration.Long
        toast.on_activated = self._handleToastClick
        self.Toaster.show_toast(toast)