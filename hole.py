#!/usr/bin/env python3
import os
import signal
import subprocess
import tkinter as tk

# Ensure tkinter is installed via apt
try:
    import tkinter as tk
except ImportError:
    print("tkinter not found, attempting to install via apt...")
    try:
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "-y", "python3-tk"])
        import tkinter as tk
    except Exception:
        print("Failed to install tkinter. Please install manually with:")
        print("sudo apt install python3-tk")
        exit(1)

# File to track overlay PID
pid_file = os.path.expanduser("~/.tools_pid")
os.makedirs(os.path.dirname(pid_file), exist_ok=True)

# Kill previous overlay if exists
if os.path.exists(pid_file):
    try:
        with open(pid_file, "r") as f:
            old_pid = int(f.read().strip())
        os.kill(old_pid, signal.SIGTERM)
    except:
        pass

# Fullscreen overlay setup
root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg="black")

canvas = tk.Canvas(root, width=root.winfo_screenwidth(),
                   height=root.winfo_screenheight(),
                   bg="black", highlightthickness=0)
canvas.pack()

# Display text in the center
x = root.winfo_screenwidth() // 2
y = root.winfo_screenheight() // 2
canvas.create_text(x, y, text="Loading...", fill="white",
                   font=("Arial", 50, "bold"))

# Save current PID
with open(pid_file, "w") as f:
    f.write(str(os.getpid()))

# Function to toggle overlay (hide/show)
def toggle_overlay():
    root.withdraw()  # hide overlay (terminal accessible)
    root.after(10000, lambda: root.deiconify())  # show again after 10s
    root.after(20000, toggle_overlay)  # repeat

# Start toggling after initial 10 seconds visible
root.after(10000, toggle_overlay)

# Start main loop
root.mainloop()
