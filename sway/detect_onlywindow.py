import subprocess, json, time, os

window = {"change": None}
count = 0 # Debugging
ignore = [
    "Picture-in-picture"
]
reload = False
if not os.path.exists ("/tmp/custom-sway-window"):
    os.mkdir ("/tmp/custom-sway-window")

while True:
    pretty = subprocess.run (["swaymsg", "-pt", "get_tree"], capture_output = True)
    pretty.check_returncode ()
    pretty = [i [4 : ] for i in pretty.stdout.decode ().strip ().split ("\n") if i.startswith ("    ") or i.startswith ("  #")] + ["# EOF"]

    raw = subprocess.run (["swaymsg", "-rt", "get_tree"], capture_output = True)
    raw.check_returncode ()
    raw = json.loads (raw.stdout.decode ())

    borders, currentspaces, names = {}, {}, {}
    def recurse_node (node, workspace = None):
        global borders, currentspaces, names
        if node ["type"] == "output" and "current_workspace" in node:
            currentspaces [node ["current_workspace"]] = node ["name"]
        if node ["name"] in ("__i3", "__i3_scratch"):
            return
        if not node ["nodes"] and "con" in node ["type"]:
            if "border" in node and node ["name"] not in ignore:
                borders [node ["id"]] = node ["border"]
            names [node ["id"]] = node ["name"]
        for i in node ["nodes"] + node ["floating_nodes"]:
            recurse_node (i, i ["name"] if i ["type"] == "workspace" else workspace) # Workspace is the parent workspace
    recurse_node (raw)

    allcontainers, workspace, containers, onlys, output = [], None, [], [], None
    for i in pretty:
        if i.startswith ("#"):
            if len (containers) == 1:
                onlys.append (containers [0])
            if workspace in currentspaces: # Workspace is visible
                with open ("/tmp/custom-sway-window/" + buffered_output, "w") as f:
                    if len (allcontainers) == 1 and allcontainers [0] in names:
                        f.write (names [allcontainers [0]])
            allcontainers, containers = [], []
            workspace = i.split () [2] [1 : -1] if i != "# EOF" else None
            buffered_output = output
        elif i.split () [1] == "output":
            output = i.split (" ") [2] [1 : -1]
        else:
            container = i.strip ().split (" ")
            num = int (container [0] [1 : -1])
            if container [1] == "con":
                if num in borders:
                    containers.append (num)
                allcontainers.append (num)

    _ = subprocess.run (["pkill", "-36", "waybar"])
    if window ["change"] != "focus": # reload or ("current" not in window and (window ["change"] in ("new", "close", "floating", "title", "move") or window ["change"] == "focus" and window ["container"] ["type"] == "floating_con")):
        for k, v in borders.items ():
            if k in onlys:
                if v == "normal":
                    _ = subprocess.run (["swaymsg", f'[con_id="{k}"]', "border", "none"])
            elif v == "none":
                _ = subprocess.run (["swaymsg", f'[con_id="{k}"]', "border", "normal"])
    if reload:
        time.sleep (0.3)
        reload = False
    else:
        window = subprocess.run (["swaymsg", "-t", "subscribe", '[ "window", "workspace" ]'], capture_output = True)
        window.check_returncode ()
        window = json.loads (window.stdout.decode ())
        reload = True