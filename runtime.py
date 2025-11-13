#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
import time
import random
import tkinter as tk

SCRIPT_PATH = os.path.abspath(__file__)
PID_FILE = os.path.expanduser("~/.search_cmd")

# Full list of fun facts
FUN_FACTS = [
    "Did you know that honey never spoils?",
    "Did you know that a group of flamingos is called a 'flamboyance'?",
    "Did you know that octopuses have three hearts?",
    "Did you know that bananas are berries but strawberries aren't?",
    "Did you know that sea otters hold hands while sleeping to keep from drifting apart?",
    "Did you know that wombat poop is cube-shaped?",
    "Did you know that sloths can hold their breath longer than dolphins?",
    "Did you know that Scotland has 421 words for 'snow'?",
    "Did you know that some turtles can breathe through their butts?",
    "Did you know that a day on Venus is longer than a year on Venus?",
    "Did you know that a single strand of spaghetti is called a 'spaghetto'?",
    "Did you know that the Eiffel Tower can be 15 cm taller during summer?",
    "Did you know that sea horses are monogamous?",
    "Did you know that koalas have fingerprints similar to humans?",
    "Did you know that the shortest war in history lasted 38 minutes?",
    "Did you know that lobsters taste with their feet?",
    "Did you know that some cats are allergic to humans?",
    "Did you know that a group of crows is called a 'murder'?",
    "Did you know that giraffes have no vocal cords?",
    "Did you know that penguins propose with pebbles?",
    "Did you know that dragonflies can live underwater for years as nymphs?",
    "Did you know that humans share 60% of their DNA with bananas?",
    "Did you know that dolphins have unique names for each other?",
    "Did you know that the blue whale is the largest animal to ever exist?",
    "Did you know that some jellyfish are biologically immortal?",
    "Gumper?"
]

def get_font_name():
    """Return Comic Sans if available, else DejaVu Sans."""
    try:
        available_fonts = list(tk.font.families())
    except Exception:
        available_fonts = []

    if "Comic Sans MS" in available_fonts:
        return "Comic Sans MS"
    return "DejaVu Sans"

def launch_overlay():
    """Parent loop: relaunch the overlay if it dies."""
    while True:
        proc = subprocess.Popen([sys.executable, SCRIPT_PATH, "--child"])
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
        time.sleep(1)

def run_overlay():
    font_name = get_font_name()

    # Kill old overlay if running
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, signal.SIGTERM)
        except Exception:
            pass

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
    canvas.pack()

    x = screen_width // 2
    y = screen_height // 2
    text_color = "#7CFC00"
    font_weight = "bold"

    # Create a single text item
    initial_word = random.choice(FUN_FACTS)
    text_item = canvas.create_text(
        x, y,
        text=initial_word,
        fill=text_color,
        font=(font_name, 50, font_weight),
        width=screen_width - 100,
        justify="center"
    )

    def scale_text():
        """Auto-scale text to fit the screen."""
        font_size = 50
        canvas.itemconfig(text_item, font=(font_name, font_size, font_weight))
        bbox = canvas.bbox(text_item)
        while bbox[3] - bbox[1] > screen_height - 100 and font_size > 10:
            font_size -= 2
            canvas.itemconfig(text_item, font=(font_name, font_size, font_weight))
            bbox = canvas.bbox(text_item)

    scale_text()

    # Save PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Fade in/out effect
    def fade_text(new_text, steps=20, delay=50):
        """Fade out, change text, then fade in."""
        for i in range(steps):
            alpha = 1 - (i / steps)
            canvas.itemconfig(text_item, fill=f"#{int(124*alpha+0):02x}{int(252*alpha+0):02x}{int(0*alpha+0):02x}")
            root.update()
            time.sleep(delay / 1000)
        canvas.itemconfig(text_item, text=new_text)
        scale_text()
        for i in range(steps):
            alpha = i / steps
            canvas.itemconfig(text_item, fill=f"#{int(124*alpha+0):02x}{int(252*alpha+0):02x}{int(0*alpha+0):02x}")
            root.update()
            time.sleep(delay / 1000)

    # Update text every 20 seconds
    def update_text():
        new_word = random.choice(FUN_FACTS)
        fade_text(new_word)
        root.after(20000, update_text)

    root.after(20000, update_text)

    def on_close():
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        root.destroy()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    if "--child" in sys.argv:
        run_overlay()
    else:
        launch_overlay()
