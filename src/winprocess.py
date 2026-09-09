import sys
import subprocess
import os


def setup_autostart(task_name="HABatteryMonitor", interval_hours=1):
    """Creates new task in system scheduler."""
    exe_path = os.path.abspath(sys.argv[0])
    # Check if task exists
    check_cmd = ["schtasks", "/Query", "/TN", task_name]
    result = subprocess.run(
        check_cmd,
        capture_output=True,
        text=True,
        shell=False,
        encoding="cp852",
        errors="ignore"
    )
    if result.returncode != 0:
        # Creating task
        # arguments list takes care of spaces in path
        create_cmd = [
            "schtasks", "/Create",
            "/TN", task_name,
            "/TR", exe_path,
            "/SC", "HOURLY",
            "/MO", str(interval_hours),
            "/F"
        ]
        create_result = subprocess.run(
            create_cmd,
            capture_output=True,
            text=True,
            shell=False,
            encoding="cp852",
            errors="ignore"
        )
        if create_result.returncode == 0:
            print(f"Added task '{task_name}' to scheduler.")
        else:
            print(f"Error while adding task: {create_result.stderr.strip()}")


def remove_autostart(task_name="HABatteryMonitor"):
    """Deletes task from Windows schedule"""
    check_cmd = ["schtasks", "/Query", "/TN", task_name]
    result = subprocess.run(
        check_cmd,
        capture_output=True,
        text=True,
        shell=False,
        encoding="cp852",
        errors="ignore"
    )
    if result.returncode == 0:
        # Task exists - let's delete it
        delete_cmd = ["schtasks", "/Delete", "/TN", task_name, "/F"]
        subprocess.run(
            delete_cmd,
            capture_output=True,
            text=True,
            shell=False,
            encoding="cp852",
            errors="ignore"
        )
        print(f"Deleted task '{task_name}' from scheduler.")
    else:
        print(f"Task '{task_name}' does not exist and was not deleted.")