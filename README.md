# linux-scripts
A collection of personal scripts I use on Linux

## List of Scripts:
- `detect_onlywindow.py` - Hides SwayWM title bar if there is only one tiled window in a workspace (see [issue #4132](https://github.com/swaywm/sway/issues/4132)) Run it in the background with an `exec` command in Sway config.
    - Known issues:
        - Changing the container layout doesn't automatically update title bars
        - **Warning** - Certain XWayland dialog windows (KiCad is the most affected program for me) will cause the script to **softlock the WM**. It appears to have been solved by adding a `sleep (0.1)` to prevent infinite loops.

- `switch_desktop.py` - Prevents `swaymsg workspace left|right` from wrapping around the other direction and isolates the movement to each output (display).
    - Use the following commands for macOS-style three finger swipe navigation (note that left/right are reversed akin to 'natural scrolling'):
    - `bindgesture swipe:3:left exec "python /path/to/switch_desktop.py right`
    - `bindgesture swipe:3:right exec "python /path/to/switch_desktop.py left`

- `wlsunset.sh` - Script to use with waybar to enable/disable `wlsunset`
    - Known issues:
        - The state toggles every time a new output is connected
        - The waybar icon does not sync between outputs
        - The script uses `ip-api` to get location, and will by default timeout after 30 tries every 2 seconds
        - The following options are required in `swayidle` for the script to work with system suspend and resume:
        - `before-sleep 'echo sleep > /tmp/wlsunset; [other commands if applicable]'`
        - `after-resume '[other commands if applicable;] rm /tmp/wlsunset'`
    - Waybar config:
```
    "custom/wlsunset": {
        "interval": "once",
        "exec-on-event": true,
        "exec": "sh /path/to/wlsunset.sh",
        "exec-if": "true",
        "on-click": "true",
        "return-type": "json",
        "format": "{icon}",
        "tooltip-format": "wlsunset: {alt}",
        "format-icons": {
            "off": "☀️",
            "on": "🌙"
        }
    }
```
