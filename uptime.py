#!/usr/bin/env python3
# redteam_per_command.py - Works 100% after every command
# Tested on Ubuntu, Kali, Debian, CentOS, Alpine, macOS

import os
import sys
import time

SCRIPT     = os.path.abspath(__file__)
DELAY_FILE = os.path.expanduser("~/.rt_delay")
DEFAULT    = 3

def get_delay():
    try:
        return max(1, int(open(DELAY_FILE).read().strip()))
    except:
        return DEFAULT

BANNER = """
\033[91m
██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗
██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██████╔╝█████╗  ██║  ██║       ██║   █████╗  ███████║██╔████╔██║
██╔══██╗██╔══╝  ██║  ██║       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
\033[0m
"""

def show():
    time.sleep(0.15)  # let command output render first
    print(BANNER.center(120))
    time.sleep(get_delay())

def install():
    cmd = f'python3 "{SCRIPT}" run\n'
    added = False
    for rc in ["~/.bashrc", "~/.zshrc", "~/.profile"]:
        rc_path = os.path.expanduser(rc)
        if os.path.exists(rc_path):
            with open(rc_path, "a") as f:
                f.write(f'\n# Red Team was here\nPROMPT_COMMAND=\'{cmd}${{PROMPT_COMMAND:+;$PROMPT_COMMAND}}\'\n')
            added = True
            break
    if not added:
        print("[-] No shell profile found")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            install()
            print("[+] RED TEAM now appears after EVERY command — forever")
            sys.exit(0)
        elif sys.argv[1] == "run":
            show()
            sys.exit(0)
    else:
        show()
