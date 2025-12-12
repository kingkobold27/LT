#!/usr/bin/env python3
# redteam_after_every_command.py
# Shows RED TEAM banner right after EVERY command (no freeze, just shame)

import os
import sys
import time
import subprocess

SCRIPT     = os.path.abspath(__file__)
DELAY_FILE = os.path.expanduser("~/.rt_delay")
DEFAULT    = 3  # seconds to display banner after each command

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

def show_banner():
    time.sleep(0.1)  # tiny pause so command output appears first
    print(BANNER.center(120))
    time.sleep(get_delay())
    print()  # clean line after

def install():
    cmd = f'python3 "{SCRIPT}" postexec\n'
    profiles = ["~/.bashrc", "~/.zshrc"]
    for p in profiles:
        path = os.path.expanduser(p)
        if os.path.exists(path):
            with open(path, "a") as f:
                f.write(f'\nfunction __rt_hook {{ python3 "{SCRIPT}" postexec; }}\n')
                f.write('trap \'__rt_hook\' DEBUG\n')
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            install()
            print("[+] Red Team now appears after EVERY command")
            sys.exit(0)
        elif sys.argv[1] == "postexec":
            show_banner()
            sys.exit(0)
    else:
        show_banner()
