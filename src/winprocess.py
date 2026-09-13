# main imports

import sys
from pathlib import Path
import win32com.client

# COM API task name

TASK_NAME = "HABatteryMonitor"

# Constant COM - from Task Scheduler API documentation
_TASK_TRIGGER_LOGON = 9
_TASK_ACTION_EXEC = 0
_TASK_CREATE_OR_UPDATE = 6
_TASK_LOGON_INTERACTIVE_TOKEN = 3

# Function to obtain produced exe path

def _getExePath() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve()
    return Path(sys.argv[0]).resolve()

# Function to add exe file to autostart

def setupAutostart(task_name: str = TASK_NAME) -> None:
    """
    Creates a Windows Task Scheduler task (to run at logon) and, if it already exists,
    updates its path to the current .exe location.
    Call this on every app startup so that if the file is moved,
    the task path will automatically be "fixed" on the next launch.
    """
    exe_path = _getExePath()

    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()
    root_folder = scheduler.GetFolder("\\")

    task_def = scheduler.NewTask(0)

    trigger = task_def.Triggers.Create(_TASK_TRIGGER_LOGON)
    trigger.Enabled = True

    action = task_def.Actions.Create(_TASK_ACTION_EXEC)
    action.Path = str(exe_path)
    action.WorkingDirectory = str(exe_path.parent)

    task_def.RegistrationInfo.Description = "HA Battery Monitor - autostart"
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False
    task_def.Settings.DisallowStartIfOnBatteries = False
    task_def.Settings.StartWhenAvailable = True

    root_folder.RegisterTaskDefinition(
        task_name,
        task_def,
        _TASK_CREATE_OR_UPDATE,
        "",  # empty user entry = current logged-in user
        "",  # without password
        _TASK_LOGON_INTERACTIVE_TOKEN,
    )
    print(f"Zadanie '{task_name}' zarejestrowane/zaktualizowane: {exe_path}")

# Function to remove exe app from autostart

def removeAutostart(task_name: str = TASK_NAME) -> None:
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()
    root_folder = scheduler.GetFolder("\\")
    try:
        root_folder.DeleteTask(task_name, 0)
        print(f"Usunięto zadanie '{task_name}'.")
    except Exception:
        print(f"Zadanie '{task_name}' nie istnieje.")