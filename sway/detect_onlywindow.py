import subprocess, json, time

window = {"change": None}

while True:
    pretty = subprocess.run (["swaymsg", "-pt", "get_tree"], capture_output = True)
    pretty.check_returncode ()
    pretty = [i [4 : ] for i in pretty.stdout.decode ().strip ().split ("\n") if i.startswith ("    ") and " floating_con " not in i]
    pretty.append ("#")

    raw = subprocess.run (["swaymsg", "-rt", "get_tree"], capture_output = True)
    raw.check_returncode ()
    raw = json.loads (raw.stdout.decode ())

    borders, focused = {}, None

    def recurse_node (node):
        global borders, focused
        if not node ["nodes"]:
            if "border" in node:
                borders [node ["id"]] = node ["border"]
            if node ["focused"]:
                focused = node ["id"]
        for i in node ["nodes"]:
            recurse_node (i)
    
    recurse_node (raw)

    b_rm, b_add = [], []

    for i, j, k in zip (pretty, pretty [1 : ], pretty [2 : ]):
        con_id = int (j.split (":") [0].strip () [1 : ])
        if k.index ("#") <= j.index ("#") and not j.startswith ("#"):
            if k.index ("#") < j.index ("#") and i.startswith ("#"):
                if borders.get (con_id) == "normal":
                    b_rm.append (con_id)
            elif borders.get (con_id) == "none":
                b_add.append (con_id)

    for i in b_rm:
        _ = subprocess.run (["swaymsg", f'[con_id="{i}"]', "focus"])
        _ = subprocess.run (["swaymsg", "border", "none"])
    for i in b_add:
        _ = subprocess.run (["swaymsg", f'[con_id="{i}"]', "focus"])
        _ = subprocess.run (["swaymsg", "border", "normal"])

    if focused and window ["change"] != "close":
        focus = subprocess.run (["swaymsg", f'[con_id="{focused}"]', "focus"])
    
    window ["change"] = None
    while window ["change"] not in ["new", "close", "floating", "title", "move"]:
        window = subprocess.run (["swaymsg", "-t", "subscribe", '[ "window" ]'], capture_output = True)
        window.check_returncode ()
        window = json.loads (window.stdout.decode ())
        time.sleep (0.1)
    time.sleep (0.1)