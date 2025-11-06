#!/usr/bin/env python3
import os
import signal
import subprocess
import tkinter as tk

# -------------------------------
# Ensure tkinter is installed via apt
# -------------------------------
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

# -------------------------------
# Files to track command count and overlay PID
# -------------------------------
count_file = os.path.expanduser("~/.dottracker_count")
pid_file = os.path.expanduser("~/.dottracker_overlay_pid")
os.makedirs(os.path.dirname(count_file), exist_ok=True)

# -------------------------------
# Kill previous overlay if exists
# -------------------------------
if os.path.exists(pid_file):
    try:
        with open(pid_file, "r") as f:
            old_pid = int(f.read().strip())
        os.kill(old_pid, signal.SIGTERM)
    except:
        pass

# -------------------------------
# Update command count
# -------------------------------
if os.path.exists(count_file):
    with open(count_file, "r") as f:
        count = int(f.read().strip())
else:
    count = 0
count += 1
with open(count_file, "w") as f:
    f.write(str(count))

# -------------------------------
# Calculate dot size
# -------------------------------
radius = 10 + int(count ** 0.5 * 5)

# -------------------------------
# Fullscreen overlay setup
# -------------------------------
root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg="black")

canvas = tk.Canvas(root, width=root.winfo_screenwidth(),
                   height=root.winfo_screenheight(),
                   bg="black", highlightthickness=0)
canvas.pack()

# Draw dot in center
x = root.winfo_screenwidth() // 2
y = root.winfo_screenheight() // 2
canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="black")

# Save current PID
with open(pid_file, "w") as f:
    f.write(str(os.getpid()))

# -------------------------------
# Function to toggle overlay
# -------------------------------
def toggle_overlay():
    root.withdraw()  # hide overlay
    os.system("clear")  # clear terminal while hidden
    # Re-show after 10 seconds
    root.after(10000, lambda: root.deiconify())
    # Schedule next hide in 20 seconds (10 visible + 10 hidden)
    root.after(20000, toggle_overlay)

# Start toggling after initial 10 seconds visible
root.after(10000, toggle_overlay)

# -------------------------------
# Start main loop
# -------------------------------
root.mainloop()
