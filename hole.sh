#!/usr/bin/env python3
import os
import tkinter as tk

# ------------------------------
# Step 1: Track command count
# ------------------------------
count_file = os.path.expanduser("~/.dottracker_count")
os.makedirs(os.path.dirname(count_file), exist_ok=True)

if os.path.exists(count_file):
    with open(count_file, "r") as f:
        count = int(f.read().strip())
else:
    count = 0

count += 1
with open(count_file, "w") as f:
    f.write(str(count))

# ------------------------------
# Step 2: Calculate dot size
# ------------------------------
radius = 10 + int(count ** 0.5 * 5)

# ------------------------------
# Step 3: Fullscreen opaque overlay
# ------------------------------
root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg="black")  # completely black

# Draw dot in center
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="black", highlightthickness=0)
canvas.pack()
x = root.winfo_screenwidth() // 2
y = root.winfo_screenheight() // 2
canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="black")

# Optional: Press ESC to exit (safe kill)
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
