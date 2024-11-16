import sys, subprocess

if len (sys.argv) != 2:
    sys.exit (1)
action = sys.argv [1].lower ()
if action not in ("switch", "move"):
    sys.exit (1)

spaces = subprocess.run (["swaymsg", "-pt", "get_workspaces"], capture_output = True)
spaces.check_returncode ()
spaces = [int (i.split () [1]) for i in spaces.stdout.decode ().split ("\n") if i.strip ().startswith ("Workspace ")]

min_space = 1 # Workspace 0 is not normally used
while min_space in spaces:
    min_space += 1

if action == "switch":
    subprocess.run (["swaymsg", "workspace", str (min_space)])
else:
    subprocess.run (["swaymsg", "move", "workspace", str (min_space)])