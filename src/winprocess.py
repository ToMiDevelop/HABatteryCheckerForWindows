# main imports

import sys
from pathlib import Path
import win32com.client
import win32api

# COM API task name
TASK_NAME = "HABatteryMonitor"
# Task folder name
TASK_FOLDER = "\\HABatteryMonitor"

# Constant COM - from Task Scheduler API documentation
_TASK_TRIGGER_LOGON = 9
_TASK_ACTION_EXEC = 0
_TASK_CREATE_OR_UPDATE = 6
_TASK_LOGON_INTERACTIVE_TOKEN = 3

# Function to obtain produced exe path

# Internal function to get actual exe / main.py folder path
def _getExePath() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve()
    return Path(sys.argv[0]).resolve()

# Internal function to get / create a task folder
def _getOrCreateTaskFolder(scheduler) -> "win32com.client.CDispatch":
    root_folder = scheduler.GetFolder("\\")
    try:
        return scheduler.GetFolder(TASK_FOLDER)
    except Exception:
        # If folder does not exist we create it at first run
        return root_folder.CreateFolder(TASK_FOLDER.lstrip("\\"))

# Function to add exe file to autostart
def setupAutostart(task_name: str = TASK_NAME) -> None:
    exe_path = _getExePath()

    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()
    task_folder = _getOrCreateTaskFolder(scheduler)

    task_def = scheduler.NewTask(0)

    trigger = task_def.Triggers.Create(_TASK_TRIGGER_LOGON)
    trigger.Enabled = True
    trigger.UserId = win32api.GetUserNameEx(win32api.NameSamCompatible)

    action = task_def.Actions.Create(_TASK_ACTION_EXEC)
    action.Path = str(exe_path)
    action.WorkingDirectory = str(exe_path.parent)

    task_def.RegistrationInfo.Description = "HA Battery Monitor - autostart"
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False
    task_def.Settings.DisallowStartIfOnBatteries = False
    task_def.Settings.StartWhenAvailable = True

    task_folder.RegisterTaskDefinition(
        task_name,
        task_def,
        _TASK_CREATE_OR_UPDATE,
        "",
        "",
        _TASK_LOGON_INTERACTIVE_TOKEN,
    )
    print(f"Task '{task_name}' registered / updated in folder {TASK_FOLDER}: {exe_path}")

# Function to remove exe app from autostart
def removeAutostart(task_name: str = TASK_NAME) -> None:
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()
    try:
        task_folder = scheduler.GetFolder(TASK_FOLDER)
        task_folder.DeleteTask(task_name, 0)
        print(f"Removed task '{task_name}'.")
    except Exception:
        print(f"Task '{task_name}' does not exist.")