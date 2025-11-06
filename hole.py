#!/usr/bin/env python3
import os
import math
import subprocess
import matplotlib.pyplot as plt

# -------------------------------
# Step 1: Ensure directory and count file exist (Bash equivalent)
# -------------------------------
dot_dir = os.path.expanduser("~/.dottracker")
os.makedirs(dot_dir, exist_ok=True)
count_file = os.path.join(dot_dir, "count")
dot_file = os.path.join(dot_dir, "dot.png")

# Initialize count file if missing or empty
if not os.path.exists(count_file) or os.path.getsize(count_file) == 0:
    # Bash equivalent: mkdir -p ~/.dottracker && echo 0 > ~/.dottracker/count
    subprocess.run(["mkdir", "-p", dot_dir])
    with open(count_file, "w") as f:
        f.write("0")

# -------------------------------
# Step 2: Update counter
# -------------------------------
with open(count_file, "r+") as f:
    count = int(f.read().strip())
    count += 1
    f.seek(0)
    f.write(str(count))
    f.truncate()

# -------------------------------
# Step 3: Draw the growing dot
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
# Step 4: Add PROMPT_COMMAND to ~/.bashrc if not already present
# -------------------------------
bashrc_path = os.path.expanduser("~/.bashrc")
prompt_command_line = f'PROMPT_COMMAND="python3 {os.path.abspath(__file__)}"'

# Read existing bashrc content
with open(bashrc_path, "r") as f:
    bashrc_content = f.read()

# Append if not already present
if prompt_command_line not in bashrc_content:
    with open(bashrc_path, "a") as f:
        f.write(f"\n# Added by dottracker\n{prompt_command_line}\n")
