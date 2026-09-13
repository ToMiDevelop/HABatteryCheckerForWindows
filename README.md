# Home Assistant Battery Monitor

## Overview

This is a Windows application that monitors the battery levels of your chosen
Home Assistant entities and displays the information as native Windows toast
notifications. In addition, the application generates a detailed battery
health report powered by an LLM (Google Gemini), based on the historical data
collected over time.

Usage is straightforward: launch the app, fill in the required information in
the first-run configuration window, and you're done. The application
registers itself to launch automatically at every login and will keep
delivering battery status toasts along with a nicely styled AI-generated
report, shown in a popup webview window.

## Screenshots

All screenshots are taken with the current Polish version of the ui.

### Configuration window - first run wizard

[![Configuration window](https://github.com/ToMiDevelop/HABatteryCheckerForWindows/raw/main/pics/config.png)](/ToMiDevelop/HABatteryCheckerForWindows/blob/main/pics/config.png)

### Popup report window

[![Example AI report – part 1](https://github.com/ToMiDevelop/HABatteryCheckerForWindows/raw/main/pics/report1.png)](/ToMiDevelop/HABatteryCheckerForWindows/blob/main/pics/report1.png)

### Popup report window

[![Example AI report – part 2](https://github.com/ToMiDevelop/HABatteryCheckerForWindows/raw/main/pics/report2.png)](/ToMiDevelop/HABatteryCheckerForWindows/blob/main/pics/report2.png)

### System toasts

[![Example toast notifications](https://github.com/ToMiDevelop/HABatteryCheckerForWindows/raw/main/pics/toasts.png)](/ToMiDevelop/HABatteryCheckerForWindows/blob/main/pics/toasts.png)

## Operating system and programming language

This application is written in Python and is intended exclusively for
Windows 11. At the code level, it relies on invoking certain Windows shell
commands.

## Source code structure

The application's source code is located in the **`src`** folder and consists
of the following files:

- **`main.py`** – the main entry point of the application
- **`configwindow.py`** – handles the first-run configuration window
- **`winprocess.py`** – manages adding the application to Windows autostart
  (and removing it, for testing purposes)
- **`database.py`** – manages the connection to the local SQLite database and
  basic database operations
- **`devices.py`** – to be edited by the user before building the Windows
  executable; defines device names and their corresponding Home Assistant
  entity IDs
- **`firstrun.py`** – handles the application's first-run logic
- **`normalrun.py`** – handles regular (non-first) run logic
- **`homeassistant.py`** – handles data retrieval from the Home Assistant API
- **`messages.py`** – holds UI and prompt strings; currently available in
  Polish only
- **`mytoastspl.py`** – manages custom Windows toast notifications
- **`ai.py`** – handles communication with the Gemini API
- **`reporter.py`** – converts the Gemini response into a styled HTML report
- **`reportsgui.py`** – displays the generated report in a webview window

The **`pics`** folder contains the application author's avatar image, used in
the initial configuration window.

## Application usage and running logic overview

### Data preparation

To use the application you need to prepare these:
- ***Home Assistant URL*** - can be found in your web browser.
- ***Home Assistant long-lived access token*** - to be generated in users security settings.
- ***Gemini API Key*** - can be created in [Google AI studio](https://aistudio.google.com/), even a free tier plan is
completely ok.
- ***LLM model name*** - one of the names of models supported by Gemini API. If using free plans `gemini-3.5-flash-lite`
is highly recommended.
- ***HA devices configuration spreadsheet*** - a xlsx spreadsheet with a strict logic containing 5 sheets and only 2 data columns
in each sheet. More details can be read bellow.

### HA devices configuration spreadsheet

This spreadsheet is an ordinary xlsx spreadsheet. Can be created directly in Microsoft Excel or in any other office
software supporting the xlsx file format.

The spreadsheet should contain only 5 sheets with EXACTLY these names:
- `devicesBatteryValueList`
- `devicesBatteryTypeList`
- `devicesLQIList`
- `devicesRSSIList`
- `batteryThreshold`

#### Sheets structure

##### 1. `devicesBatteryValueList`

| Device name   | Device battery % value entity id |
|---------------|----------------------------------|
| Devoce 1 name | Device 1 battery value entity id |
| Devoce 2 name | Device 2 battery value entity id |
| Devoce 3 name | Device 3 battery value entity id |
| ...           | ...                              |
| Devoce n name | Device n battery value entity id |

##### 2. `devicesBatteryTypeList`

| Device name   | Device battery type entity id         |
|---------------|---------------------------------------|
| Devoce 1 name | Device 1 battery type value entity id |
| Devoce 2 name | Device 2 battery type value entity id |
| Devoce 3 name | Device 3 battery type value entity id |
| ...           | ...                                   |
| Devoce n name | Device n battery type value entity id |

##### 3. `devicesLQIList`

| Device name   | Device LQI entity id   |
|---------------|------------------------|
| Devoce 1 name | Device 1 LQI entity id |
| Devoce 2 name | Device 2 LQI entity id |
| Devoce 3 name | Device 3 LQI entity id |
| ...           | ...                    |
| Devoce n name | Device n LQI entity id |

##### 4. `devicesRSSIList`

| Device name   | Device RSSI entity id   |
|---------------|-------------------------|
| Devoce 1 name | Device 1 RSSI entity id |
| Devoce 2 name | Device 2 RSSI entity id |
| Devoce 3 name | Device 3 RSSIentity id  |
| ...           | ...                     |
| Devoce n name | Device n RSSI entity id |

##### 5. `batteryThreshold`

| Parameter name   | Value                |
|------------------|----------------------|
| batteryThreshold | Integer number value |

#### Spreadsheets name

The name of the spreadsheet must be EXACTLY this:`devices.xlsx`

#### Spreadsheet example

And example of the spreadsheet can be found in `examples` folder - direct [link](/examples/devices.xlsx).

### Usage

Just download the latest release and open the `.exe` file. Remember to save in some kind of reasonable place. 

### Whole process overview

```mermaid
graph TD
HAApi@{shape: lean-l, label: "Prepare Home Assistant URL and long-lived access token"}
GeminiApi@{shape: lean-l, label: "Prepare Gemini API key"}
Excel@{shape: lean-l, label: "Prepare HA devices configuration spreadsheet"}
Start((Application start))
Stop((Application stop))
TaskOn[Register autostart entry]
TaskOff[Remove autostart entry]
ConstructRequest[Build HTTP request]
Api(Home Assistant API)
BatUnav{Is battery unavailable?};
Low@{shape: lean-r, label: "Low battery toast"}
Full@{shape: lean-r, label: "Battery status toast"}
Empty@{shape: lean-r, label: "Empty battery toast"}
Zero{Is battery = 0?}
Threshold{Is battery <= threshold?}
Loop[Start main loop]
Gemini@{shape: lean-r, label: "Generate and display Gemini report from data stored in the local database"}
LocalDB[Save JSON response to the local SQLite database]
subgraph preparation [0. Data preparation phase]
    GeminiApi
    Excel
    HAApi
end
subgraph start [1. Home Assistant API call phase]
    GeminiApi --> Start
    Excel --> Start
    HAApi --> Start
    Start --> TaskOn
    TaskOn --> ConstructRequest
    ConstructRequest -->|HTTP request| Api
    Api -->|JSON response| LocalDB
    LocalDB --> Loop
end
subgraph for [2. For each device entity in the JSON response]
    Loop --> BatUnav
    BatUnav -->|YES| Empty
    BatUnav -->|NO| Zero
    Zero -->|YES| Empty
    Zero -->|NO| Threshold
    Threshold -->|YES| Low
    Threshold -->|NO| Full
    Empty --> Gemini
    Low --> Gemini
    Full --> Gemini
end
subgraph optional [3.1 Optional autostart entry removal]
    Gemini -.-> TaskOff
end
subgraph normal [3.2 Normal application shutdown]
    TaskOff -.-> Stop
    Gemini --> Stop
end
```
## Notes on the autostart mechanism

The application registers itself for autostart through the Windows Task
Scheduler, using the `pywin32` COM API (`Schedule.Service`). A task is
created to run the executable at user logon, using the current user's
context — no administrator privileges are required.

This registration step runs on every application launch and always updates
the task's target path to the executable's current location. This means
that if you move the `.exe` file to a different folder, the scheduled task
is automatically corrected the next time you run the application manually —
there is no stale, broken autostart entry to clean up.

Removing the scheduled task is optional and intended for testing purposes
only. To enable automatic removal on application exit, uncomment the
following line in `main.py`:

```python
# winprocess.remove_autostart()
```

## Required Python packages

All required packages are pinned in the [`requirements.txt`](requirements.txt)
file in the root of this repository. Install them all at once, inside your
virtual environment, with:

```
pip install -r requirements.txt
```

The table below lists the same packages individually, together with the
module names used to import them in the source code — useful if you only
need to install a subset of them, or if you're troubleshooting a missing
dependency (module names used in `import` statements are not always
identical to their PyPI package names).

| Import name(s)                    | Install with `pip install ...` | Notes                                             |
|-----------------------------------|--------------------------------|---------------------------------------------------|
| `requests`                        | `requests`                     |                                                   |
| `windows_toasts`                  | `windows-toasts`               |                                                   |
| `urllib3`                         | `urllib3`                      | Typically installed as a dependency of `requests` |
| `sqlalchemy`                      | `SQLAlchemy`                   |                                                   |
| `google`, `google.genai`          | `google-genai`                 |                                                   |
| `customtkinter`                   | `customtkinter`                |                                                   |
| `PIL` (used in `configwindow.py`) | `Pillow`                       |                                                   |
| `dotenv`                          | `python-dotenv`                |                                                   |
| `markdown`                        | `Markdown`                     |                                                   |
| `webview`                         | `pywebview`                    |                                                   |
| `win32com`                        | `pywin32`                      | Used for Task Scheduler autostart registration    |
| `openpyxl`                        | `openpyxl`                     | Used to process Excel spreadsheets                |

The following modules are part of the Python standard library and do **not**
require a separate `pip install`:

`sys`, `subprocess`, `os`, `json`, `dataclasses`, `pathlib`, `datetime`, `shutil`, `typing`.

## Customizing the application for your needs

To customize the application to your specific needs feel free to clone this repository and go on with coding :)
As the author of this project I'm open your contributions to this repo - especially with translations to other
languages.

At this point all the GUI messages are shown in Polish. If you wish to help just go on, contact or just
translate the messages which can be found in `messages.py` and create a merge request into the dev branch of this
repository.

In case of any contributions to the project feel free to contact me over email: ***ToMiDevelop@outlook.com***.

## Security considerations

This application makes two deliberate security trade-offs, aimed at a
single-user, home-lab environment. Please review them before using the app
in any other context:

- **Unencrypted credentials file.** The Home Assistant long-lived access
  token and the Gemini API key are stored in plain text in
  `data/secrets.env`. This file is not encrypted at rest. Anyone with file
  system access to the machine (or to a backup of it) can read these
  credentials. Do not use this application on a shared or multi-user
  computer, and make sure the machine itself is adequately secured (disk
  encryption, user account access controls, etc.).
- **Disabled SSL certificate verification.** All requests to the Home
  Assistant REST API are made with certificate verification turned off
  (`verify=False`). This is intentional, since Home Assistant instances in
  home-lab setups commonly use self-signed certificates. However, it also
  means the application will not detect a man-in-the-middle attack on the
  connection to your Home Assistant instance. Only use this application over
  a trusted local network, and avoid exposing your Home Assistant instance
  to the public internet without a properly signed certificate and a
  reverse proxy.

## Building a standalone Windows executable (.exe)

You can build a standalone `.exe` file that runs natively on Windows without
requiring a separate Python installation.

### Prerequisites

`pyinstaller` is already included in `requirements.txt`, so if you've
followed the installation step above, it is already available in your
virtual environment. Otherwise, install it separately with:

```
python -m pip install pyinstaller
```
### Cloning repository

This project assumes you've got `git` installed and configured in your Windows system. If you are new to `git`
please visit its [website](https://git-scm.com/) and install it accordingly to the documentation.

To clone this projects repository run the following command in a folder of your choice:

```
git clone https://github.com/ToMiDevelop/HABatteryCheckerForWindows.git
```
It will created a new folder named exactly as the repository. Please move to in the terminal and follow next steps.

### Build command

Run the following command from the directory containing cloned repository:

```
pyinstaller --noconsole --onefile --name "HA Battery Monitor" --add-data "pics/author.png;pics" src/main.py
```

Once the build completes, you will find the resulting
`HA Battery Monitor.exe` file inside the newly created `dist` folder. The
executable can be freely moved to a location of your choice. Launch it once,
and — as long as you do not move it afterwards — Windows will relaunch it
automatically on every subsequent login.

### Build options explained

- `--onefile` – bundles the entire application and its dependencies into a
  single, standalone `.exe` file.
- `--noconsole` – hides the console window, allowing the application to run
  in the background and display native Windows toast notifications only.
- `--name` – sets the name of the output executable.

## Notice on Python virtual environments

This project assumes familiarity with Python virtual environments (`venv`)
and best practices around dependency isolation. If you are new to virtual
environments, check out the official
[Python Virtual Environments tutorial](https://docs.python.org/3/tutorial/venv.html)
or this beginner-friendly guide on
[Real Python](https://realpython.com/python-virtual-environments-a-primer/).

## License

Distributed under the GPL-3.0 License. See `LICENSE` for details.
