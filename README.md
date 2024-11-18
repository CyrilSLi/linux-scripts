# linux-scripts
A collection of personal scripts I use on Linux

## List of Scripts:
- `detect_onlywindow.py` - Hides SwayWM title bar if there is only one tiled window in a workspace (see [issue #4132](https://github.com/swaywm/sway/issues/4132)) Run it in the background with an `exec` command in Sway config.
    - Known issues:
        - **Warning** - Certain XWayland dialog windows (KiCad is the most affected program for me) will cause the script to **softlock the WM**. After the code has been changed, **this issue is currently being monitored**.

- `switch_desktop.py` - Prevents `swaymsg workspace left|right` from wrapping around the other direction and isolates the movement to each output (display).
    - Use the following commands for macOS-style three finger swipe navigation (note that left/right are reversed akin to 'natural scrolling'):
    - `bindgesture swipe:3:left exec "python /path/to/switch_desktop.py right`
    - `bindgesture swipe:3:right exec "python /path/to/switch_desktop.py left`

- `wlsunset.sh` - Script to use with waybar to enable/disable `wlsunset`
    - The script uses `ip-api` to get location, and will by default timeout after 30 tries every 2 seconds
    - Waybar config (if you have another widget which uses `signal` to update, ensure that each widget has a unique signal number):
```
    "custom/wlsunset": {
        "interval": "once",
        "exec": "if pgrep wlsunset >/dev/null 2>&1; then stdbuf -oL printf '{\"alt\": \"on\"}'; else stdbuf -oL printf '{\"alt\": \"off\"}'; fi",
        "on-click": "sh /path/to/wlsunset.sh",
        "signal": 1, // SIGRTMIN+1 or 35
        "return-type": "json",
        "format": "{icon}",
        "tooltip-format": "wlsunset: {alt}",
        "format-icons": {
            "off": "☀️",
            "on": "🌙"
        }
    }
```
