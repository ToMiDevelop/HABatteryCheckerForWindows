import subprocess
import os
import sys
from pathlib import Path

def setup_autostart(app_name="HABatteryMonitor"):
    """Dodaje plik wykonywalny do systemowego folderu Autostart użytkownika."""
    # Ścieżka do folderu shell:startup
    startup_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    bat_path = startup_dir / f"{app_name}.bat"

    # Wyznaczamy ścieżkę do .exe (lub skryptu .py w trybie dev)
    if getattr(sys, "frozen", False):
        exe_path = Path(sys.executable).resolve()
    else:
        exe_path = Path(__file__).resolve()

    # Tworzymy plik .bat uruchamiający aplikację
    if not bat_path.exists():
        try:
            with open(bat_path, "w", encoding="utf-8") as f:
                f.write(f'@start "" "{exe_path}"\n')
            print(f"Pomyślnie dodano {app_name} do Autostartu użytkownika.")
        except Exception as e:
            print(f"Błąd podczas dodawania do autostartu: {e}")

def remove_autostart(app_name="HABatteryMonitor"):
    """Usuwa plik uruchomieniowy z folderu Autostart użytkownika."""
    startup_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    bat_path = startup_dir / f"{app_name}.bat"

    if bat_path.exists():
        try:
            bat_path.unlink()
            print(f"Usunięto '{app_name}' z folderu Autostart.")
        except Exception as e:
            print(f"Błąd podczas usuwania wpisu z autostartu: {e}")
    else:
        print(f"Wpis '{app_name}' nie istnieje w folderze Autostart.")

# def setup_autostart(task_name="HABatteryMonitor"):
#     """Creates app Windows autostart task.."""
#     exe_path = os.path.abspath(sys.argv[0])
#     check_cmd = ["schtasks", "/Query", "/TN", task_name]
#     result = subprocess.run(
#         check_cmd,
#         capture_output=True,
#         text=True,
#         shell=False,
#         encoding="cp852",
#         errors="ignore",
#     )
#     if result.returncode != 0:
#         create_cmd = [
#             "schtasks",
#             "/Create",
#             "/TN",
#             task_name,
#             "/TR",
#             exe_path,
#             "/SC",
#             "ONLOGON",  # Uruchomienie przy zalogowaniu
#             "/F",
#         ]
#         create_result = subprocess.run(
#             create_cmd,
#             capture_output=True,
#             text=True,
#             shell=False,
#             encoding="cp852",
#             errors="ignore",
#         )
#         if create_result.returncode == 0:
#             print(f"Added '{task_name}' to autostartu (ONLOGON).")
#         else:
#             print(f"Error creating task: {create_result.stderr.strip()}")


# def remove_autostart(task_name="HABatteryMonitor"):
#     """Deletes task from Windows schedule"""
#     check_cmd = ["schtasks", "/Query", "/TN", task_name]
#     result = subprocess.run(
#         check_cmd,
#         capture_output=True,
#         text=True,
#         shell=False,
#         encoding="cp852",
#         errors="ignore"
#     )
#     if result.returncode == 0:
#         # Task exists - let's delete it
#         delete_cmd = ["schtasks", "/Delete", "/TN", task_name, "/F"]
#         subprocess.run(
#             delete_cmd,
#             capture_output=True,
#             text=True,
#             shell=False,
#             encoding="cp852",
#             errors="ignore"
#         )
#         print(f"Deleted task '{task_name}' from scheduler.")
#     else:
#         print(f"Task '{task_name}' does not exist and was not deleted.")