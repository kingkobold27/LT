#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
import time

SCRIPT_PATH = os.path.abspath(__file__)
# Use a user-writable location for the PID file
PID_FILE = os.path.expanduser("~/.search_cmd")

def launch_overlay():
    """
    Parent watchdog loop: keeps relaunching the overlay if it dies.
    """
    while True:
        proc = subprocess.Popen([sys.executable, SCRIPT_PATH, "--child"])
        try:
            proc.wait()  # wait for overlay to exit
        except KeyboardInterrupt:
            proc.terminate()
        time.sleep(1)  # prevent rapid respawn if crash happens immediately

def run_overlay():
    """
    Child process: the actual fullscreen overlay with text.
    """
    import tkinter as tk

    # Kill previous overlay if PID file exists
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
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
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Toggle overlay hide/show
    def toggle_overlay():
        root.withdraw()
        root.after(10000, lambda: root.deiconify())
        root.after(20000, toggle_overlay)

    root.after(10000, toggle_overlay)

    # Restart if window is closed
    def on_close():
        root.destroy()
        sys.exit(0)  # allow parent watchdog to respawn

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    if "--child" in sys.argv:
        run_overlay()
    else:
        launch_overlay()
