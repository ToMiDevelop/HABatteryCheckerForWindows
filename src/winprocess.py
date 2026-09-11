import sys
import subprocess
import os


def setup_autostart(task_name="HABatteryMonitor"):
    """Creates app Windows autostart task.."""
    exe_path = os.path.abspath(sys.argv[0])
    check_cmd = ["schtasks", "/Query", "/TN", task_name]
    result = subprocess.run(
        check_cmd,
        capture_output=True,
        text=True,
        shell=False,
        encoding="cp852",
        errors="ignore",
    )
    if result.returncode != 0:
        create_cmd = [
            "schtasks",
            "/Create",
            "/TN",
            task_name,
            "/TR",
            exe_path,
            "/SC",
            "ONLOGON",  # Uruchomienie przy zalogowaniu
            "/F",
        ]
        create_result = subprocess.run(
            create_cmd,
            capture_output=True,
            text=True,
            shell=False,
            encoding="cp852",
            errors="ignore",
        )
        if create_result.returncode == 0:
            print(f"Added '{task_name}' to autostartu (ONLOGON).")
        else:
            print(f"Error creating task: {create_result.stderr.strip()}")


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