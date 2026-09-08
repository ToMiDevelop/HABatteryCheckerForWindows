# A simple script to communicate with HA and ask for devices battery states
# and showing 'em as windows toasts

# basic imports

import requests
from windows_toasts import WindowsToaster, Toast, ToastDuration
import urllib3

# custom imports

import winprocess

# launch scheduled app process in Windows

winprocess.setup_autostart()

# disable invalid certificate warnings - app used in my local controlled home lab

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# HA authorization token

token = "YOUR TOKEN HERE"

# HA instance ip as string

haUrl = "YOUR URL HERE"

# batteries dictionary definition

batteries = {
    "Device 1 name": "battery sensor entity id for device 1",
    "Device 2 name": "battery sensor entity id for device 2",
    "Device 3 name": "battery sensor entity id for device 3",
    # you can put as many devices you want to this dictionary
    "Device n name": "battery sensor entity id for device n"
}

# set value of single battery percentage threshold

threshold = 10 # may be different for you - I like to have 10% as the borderline

# http get request request headers definition

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# initialization of WindowsToaster instance

Toaster = WindowsToaster("Home Assistant batteries monitor")

# remove any previous toasts from the active Toaster

Toaster.clear_toasts()

# Looping through batteries entries and downloading the battery state and showing windows toast if <= threshold

for name, entity_id in batteries.items():
    try:
        response = requests.get(
            url=f"{haUrl}/api/states/{entity_id}",
            headers=headers,
            timeout=10,
            verify=False
        )

        response.raise_for_status()
        state = response.json()["state"]

        if state == "unavailable":
            print(f"{name}: 0% battery")
            toast = Toast()
            toast.text_fields=[
                f"{name}",
                f"Battery empty :-("
            ]
            toast.group = entity_id
            toast.duration = ToastDuration.Long
            Toaster.show_toast(toast)
        else:
            try:
                battery = int(float(state))
                print(f"{name}: {battery}% battery")
            except ValueError:
                continue
            if battery == 0:
                toast = Toast()
                toast.text_fields=[
                    f"{name}",
                    f"Battery empty :-("
                ]
                toast.group = entity_id
                toast.duration = ToastDuration.Long
                Toaster.show_toast(toast)
            else:
                if battery <= threshold:
                    toast = Toast()
                    toast.text_fields=[
                        f"{name}",
                        f"Low battery state: {battery}%"
                    ]
                    toast.group = entity_id
                    toast.duration = ToastDuration.Long
                    Toaster.show_toast(toast)
                else:
                    toast = Toast()
                    toast.text_fields = [
                        f"{name}",
                        f"{battery}% battery"
                    ]
                    toast.group = entity_id
                    toast.duration = ToastDuration.Long
                    Toaster.show_toast(toast)
    except Exception as e:
        print(f"Error in {entity_id} data parsing: {e}")

# remove scheduled app process in Windows - uncomment bellow for testing purposes
# winprocess.remove_autostart()