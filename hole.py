#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt

# Location of counter file
count_file = os.path.expanduser("~/.dottracker/count")

# Read and update count
with open(count_file, "r+") as f:
    count = int(f.read().strip())
    count += 1
    f.seek(0)
    f.write(str(count))
    f.truncate()

# Dot radius grows with sqrt for a smoother curve
radius = (count ** 0.5) / 5.0

# Draw dot
plt.figure(figsize=(4, 4))
plt.scatter(0, 0, s=(radius * 1000), color="black")
plt.axis("off")
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.savefig(os.path.expanduser("~/.dottracker/dot.png"), bbox_inches="tight", pad_inches=0)
plt.close()


os.execv("/bin/bash", ["/bin/bash"])

