import subprocess

spaces = subprocess.run (["swaymsg", "-pt", "get_workspaces"], capture_output = True)
spaces.check_returncode ()
spaces = [int (i.split () [1]) for i in spaces.stdout.decode ().split ("\n") if i.strip ().startswith ("Workspace ")]

min_space = 1 # Workspace 0 is not normally used
while min_space in spaces:
    min_space += 1
_ = subprocess.run (["swaymsg", "workspace", str (min_space)]).check_returncode ()