# PY.TOOL

A small Windows command-line utility written in Python that provides a compact menu for a few network / process utilities.

**Features**

* IP Lookup (uses `ip-api.com`)
* Launch Angry IP Scanner (if present at `./Functions/Angry IP scanner/ipscan.exe`)
* Launch Process Hacker (if present at `./Functions/ProcessHacker/ProcessHacker.exe`)
* Launch Wireshark (if present at `./Functions/Wireshark/Wireshark.exe`)

---

## Table of contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Running the tool](#running-the-tool)
* [Menu options & behavior](#menu-options--behavior)
* [How the code works (detailed)](#how-the-code-works-detailed)
* [Common issues & fixes](#common-issues--fixes)
* [Extending / customizing](#extending--customizing)
* [Security & safety notes](#security--safety-notes)
* [License](#license)

---

## Requirements

* Windows (the script uses `os.startfile()` and `cls`)
* Python 3.8+ recommended
* Python package: `requests`

Install `requests` with:

```powershell
pip install requests
```

---

## Installation

1. Place the Python script (e.g. `pytool.py`) into a folder on your Windows machine.
2. (Optional) Create a `Functions` subfolder and put the executables you want the script to launch:

   * `./Functions/Angry IP scanner/ipscan.exe`
   * `./Functions/ProcessHacker/ProcessHacker.exe`
   * `./Functions/Wireshark/Wireshark.exe`

Make sure folder names match exactly (spaces and capitalization) if you keep the script as-is.

---

## Running the tool

Open PowerShell or Command Prompt and run:

```powershell
python pytool.py
```

The script clears the terminal, shows the ASCII logo, and asks you to choose an option:

```
[1] : IP Lookup
[2] : IP Scanner
[3] : Process Hacker
[4] : Wireshark
Option:
```

Type the option number and press Enter.

---

## Menu options & behavior

### Option 1 — IP Lookup

* Prompts for an IP or hostname.
* Queries `http://ip-api.com/json/<input>` and repeats prompt until the API returns `status: "success"`.
* When successful, prints details: IP, Country, Country Code, Region, Region Name, City, Latitude, Longitude, ISP, ORG.

Example valid input: `8.8.8.8`

If the API returns an error (invalid IP / rate-limited / blocked), the script asks you to re-enter until `ip-api` responds with success.

### Options 2–4 — Launch external executables

* For each option the script builds an absolute path relative to the script location:

  * Option 2: `./Functions/Angry IP scanner/ipscan.exe`
  * Option 3: `./Functions/ProcessHacker/ProcessHacker.exe`
  * Option 4: `./Functions/Wireshark/Wireshark.exe`
* If the `.exe` exists, `os.startfile()` is used to open it and the script prints a success message.
* If the file is not found, the script prints `Not found: <path>` and exits.

---

## How the code works (detailed)

1. **Startup / Main loop**

   * The script uses `while Is_running:` to keep the menu active, but the current implementation exits after an action that shows IP results or fails to find a requested executable.
   * `os.system("title PY.TOOL")` sets the console window title (Windows). `os.system("cls")` clears the console.

2. **Menu**

   * Uses Python `match` (pattern-matching on `choice`) to select behavior for options `"1"`–`"4"`.

3. **IP Lookup (option 1)**

   * Prompts `ip = input("Enter IP: ")`.
   * Calls `requests.get(f"http://ip-api.com/json/{ip}")` and `r.json()` to parse the JSON response into `data`.
   * Checks `while data.get("status") != "success":` and keeps prompting for an IP until the API returns status `success`.
   * When `status == "success"`, the script prints several values from `data` (e.g. `data['country']`, `data['city']`, etc.).

4. **Executable launching (options 2–4)**n   - Uses `Path(__file__).resolve().parent` to find the folder the script lives in and constructs the path for each exe.

   * Checks `if exe.exists(): os.startfile(exe)` else prints not found.

---

## Common issues & fixes

### 1) `SyntaxError: f-string: unmatched '['`

**Cause**: Using double quotes inside an f-string that is also delimited by double quotes. Example:

```py
print(f"IP : {data["query"]}")  # ❌ causes SyntaxError
```

**Fix**: Use single quotes inside the braces or escape the inner quotes:

```py
print(f"IP : {data['query']}")  # ✅ correct
```

Make sure all `print(f"...{data[...]}" )` lines use single quotes for the dictionary keys.

### 2) `KeyError` when accessing `data[...]`

**Cause**: The code tries to access keys (like `data['country']`) that don't exist in the API response (for example when `status` is `"fail"` or the API returns an unexpected format).

**Mitigation already in the script**:

* The script includes a loop that re-prompts until `status == "success"` which prevents printing `data[...]` prematurely.

**Alternative approaches**:

* Use `.get()` with defaults:

```py
country = data.get('country', 'N/A')
```

* Explicitly check `status` before printing.

### 3) Network or API errors (requests exceptions)

* If your network is offline or `requests.get()` fails, `requests` may raise exceptions like `requests.exceptions.RequestException`.
* Consider wrapping network calls in `try/except` to show a friendly error message.

Example:

```py
try:
    r = requests.get(url, timeout=5)
    data = r.json()
except requests.exceptions.RequestException:
    print("Network error — check your connection.")
    continue
```

### 4) `os.startfile` / `cls` in non-Windows environments

* These calls are Windows-specific. Running on Linux/macOS will fail or do nothing. Run this script on Windows.

---

## Extending / customizing

* **Change search behavior**: To stop the script from repeatedly prompting on bad input, replace the `while` loop with a single request and a graceful error message.
* **Use a different API**: Replace `ip-api.com` URL with another geo-IP API and adjust fields accordingly.
* **Add more tools**: Add new menu options and place exe paths in `Functions/...` similarly. Use `subprocess.Popen()` instead of `os.startfile()` if you want to capture output.
* **Add logging**: Use the `logging` module to keep a log of lookups and launched programs.

---

## Troubleshooting checklist

* If you see `SyntaxError` — check your f-strings and internal quotes (use single quotes inside `{}`).
* If IP lookups never return success:

  * Confirm you can reach `http://ip-api.com` from your machine.
  * Check for rate limiting; `ip-api.com` free tier has limits.
* If executables don’t launch:

  * Verify the path exactly matches `./Functions/...`.
  * Double-check your exe filenames and folder capitalization/spaces.
  * Confirm script has permission to open programs.

---

## Security & safety notes

* **Only launch executables you trust.** Running untrusted EXEs can compromise your system.
* The tool uses a public API; avoid sending sensitive/private IPs if that is a concern.
* The script does not elevate privileges; if an exe requires admin rights, Windows UAC will prompt separately.

---

## License

Provided as-is for educational and personal use. No warranty.

---

If you want any wording changed or additional sections (examples, screenshots, or a one-line install script) say so and I will update this README.
