import subprocess, json, time, sys

window = {"change": None}
ignore = [
    "Picture-in-picture"
]

while True:
    pretty = subprocess.run (["swaymsg", "-pt", "get_tree"], capture_output = True)
    pretty.check_returncode ()
    pretty = [i [4 : ] for i in pretty.stdout.decode ().strip ().split ("\n") if i.startswith ("    ")] + ["#"]

    raw = subprocess.run (["swaymsg", "-rt", "get_tree"], capture_output = True)
    raw.check_returncode ()
    raw = json.loads (raw.stdout.decode ())

    borders = {}
    def recurse_node (node):
        global borders, focused
        if node ["name"] in ("__i3", "__i3_scratch"):
            return
        if not node ["nodes"]:
            if "border" in node and node ["name"] not in ignore:
                borders [node ["id"]] = node ["border"]
        for i in node ["nodes"] + node ["floating_nodes"]:
            recurse_node (i)
    recurse_node (raw)

    containers, onlys = [], []
    for i in pretty:
        if i.startswith ("#"):
            if len (containers) == 1:
                onlys.append (containers [0])
            containers = []
        else:
            container = i.strip ().split (" ")
            num = int (container [0] [1 : -1])
            if num in borders and container [1] == "con":
                containers.append (num)

    for k, v in borders.items ():
        if k in onlys:
            if v == "normal":
                _ = subprocess.run (["swaymsg", f'[con_id="{k}"]', "border", "none"])
        elif v == "none":
            _ = subprocess.run (["swaymsg", f'[con_id="{k}"]', "border", "normal"])
    
    window ["change"] = None
    while window ["change"] not in ["new", "close", "floating", "title", "move"]:
        window = subprocess.run (["swaymsg", "-t", "subscribe", '[ "window" ]'], capture_output = True)
        window.check_returncode ()
        window = json.loads (window.stdout.decode ())
        time.sleep (0.3)