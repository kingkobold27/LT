#!/usr/bin/env python3
import os
import math
import matplotlib.pyplot as plt

# -------------------------------
# Setup directories and files
# -------------------------------
dot_dir = os.path.expanduser("~/.dottracker")
os.makedirs(dot_dir, exist_ok=True)
count_file = os.path.join(dot_dir, "count")
dot_file = os.path.join(dot_dir, "dot.png")

# Initialize counter if missing
if not os.path.exists(count_file):
    with open(count_file, "w") as f:
        f.write("0")

# -------------------------------
# Update counter
# -------------------------------
with open(count_file, "r+") as f:
    count = int(f.read().strip())
    count += 1
    f.seek(0)
    f.write(str(count))
    f.truncate()

# -------------------------------
# Draw dot
# -------------------------------
radius = math.log(count + 1) * 2  # adjust multiplier for visual size
plt.figure(figsize=(4, 4))
plt.scatter(0, 0, s=(radius * 1000), color="black", alpha=0.8)
plt.axis("off")
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.savefig(dot_file, bbox_inches="tight", pad_inches=0)
plt.close()

# -------------------------------
# Add PROMPT_COMMAND to ~/.bashrc if not already present
# -------------------------------
bashrc_path = os.path.expanduser("~/.bashrc")
prompt_command_line = f'PROMPT_COMMAND="python3 {os.path.abspath(__file__)}"'

# Check if line already exists
with open(bashrc_path, "r") as f:
    bashrc_content = f.read()

if prompt_command_line not in bashrc_content:
    with open(bashrc_path, "a") as f:
        f.write(f"\n# Added by dottracker\n{prompt_command_line}\n")
