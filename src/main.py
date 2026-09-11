# A simple script to communicate with HA and ask for devices battery states
# and showing 'em as windows toasts

# basic imports

import urllib3
from pathlib import Path
from dotenv import load_dotenv
import sys


# custom imports

import winprocess
from firstrun import InitialSeed
from normalrun import NormalRun
import configwindow

# launch scheduled app process in Windows

winprocess.setup_autostart()

# disable invalid certificate warnings - app used in my local controlled home lab

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# special helper function

def get_base_dir() -> Path:
    """Returns folder, in which .exe lies (or main.py in developer mode)."""
    if getattr(sys, "frozen", False):
        # Aplikacja uruchomiona jako .exe z PyInstallera
        return Path(sys.executable).resolve().parent
    else:
        # Aplikacja uruchomiona z kodu źródłowego .py
        return Path(__file__).resolve().parent

# Check (for the app first run - and just in case of moving the app id hadbdata.db exists

BASE_DIR = get_base_dir()
DATA_DIR = BASE_DIR / "data"
DB_FILE = BASE_DIR / "data" / "hadbdata.db"
ENV_FILE = BASE_DIR / "data" / "secrets.env"

# check if data folder exists

dataFolderNotExists = not DATA_DIR.exists()

if dataFolderNotExists:
    print("No data folder, creating one...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

firstRun = not DB_FILE.exists()
envNotExists = not ENV_FILE.exists()

# Deciding if running the app first time or data folder deleted

if envNotExists:
    print("No secrets.env file - Launching config window...")
    configwindow.showConfigWindow(ENV_FILE)
    if not ENV_FILE.exists():
        print("No configuration saved, exiting app")
        sys.exit(0)

# Loading secrets from secrets.env

load_dotenv(ENV_FILE)

# creating NormalRun instance

normalRun = NormalRun()

if firstRun:
    # First run or data folder deleted
    print("Initial app seed run, seeding first data to DB")
    initialSeed = InitialSeed()
    initialSeed.seedBatteryValues()
    initialSeed.seedBatteryTypes()
    initialSeed.seedLQIValues()
    initialSeed.seedRSSIValues()
    normalRun.normalBatteryValueUpdateToasts()
else:
    # Normal run
    normalRun.normalBatteryValueUpdateToasts()
    normalRun.normalLQIUpdate()
    normalRun.normaRSSIIUpdate()

print("Opening Gemini report...")
normalRun.geminiReport()



# remove scheduled app process in Windows - uncomment bellow for testing purposes
# winprocess.remove_autostart()