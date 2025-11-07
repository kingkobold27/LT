#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
import time
import random

SCRIPT_PATH = os.path.abspath(__file__)
PID_FILE = os.path.expanduser("~/.search_cmd")

# List of fun facts to display
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
    "Did you know that strawberries aren't actually berries but bananas are?",
    "Did you know that lobsters taste with their feet?",
    "Did you know that sloths can rotate their heads almost 270 degrees?",
    "Did you know that some cats are allergic to humans?",
    "Did you know that a group of crows is called a 'murder'?",
    "Did you know that giraffes have no vocal cords?",
    "Did you know that some fish can walk on land?",
    "Did you know that penguins propose with pebbles?",
    "Did you know that sea stars can regrow their arms?",
    "Did you know that dragonflies can live underwater for years as nymphs?",
    "Did you know that humans share 60% of their DNA with bananas?",
    "Did you know that butterflies can taste with their feet?",
    "Did you know that the moon has moonquakes?",
    "Did you know that there’s a species of jellyfish that is immortal?",
    "Did you know that sharks existed before trees?",
    "Did you know that a cloud can weigh over a million pounds?",
    "Did you know that rabbits can see behind them without turning their heads?",
    "Did you know that the unicorn is Scotland’s national animal?",
    "Did you know that sea cucumbers fight predators by shooting out their own organs?",
    "Did you know that koalas sleep up to 22 hours a day?",
    "Did you know that there are more stars in the universe than grains of sand on Earth?",
    "Did you know that frogs can freeze without dying?",
    "Did you know that a snail can sleep for three years?",
    "Did you know that armadillos always give birth to identical quadruplets?",
    "Did you know that the first oranges weren’t orange?",
    "Did you know that water can boil and freeze at the same time?",
    "Did you know that a group of owls is called a 'parliament'?",
    "Did you know that sea lions can bark like dogs?",
    "Did you know that hummingbirds can fly backwards?",
    "Did you know that some turtles never leave the water?",
    "Did you know that a crocodile can't stick its tongue out?",
    "Did you know that giraffes only need 10 minutes of sleep a day?",
    "Did you know that lobsters can live up to 100 years?",
    "Did you know that elephants can’t jump?",
    "Did you know that cows have best friends?",
    "Did you know that the heart of a shrimp is located in its head?",
    "Did you know that bamboo can grow up to 91 cm in a day?",
    "Did you know that cheetahs can't roar like other big cats?",
    "Did you know that flamingos can only eat with their heads upside down?",
    "Did you know that some sea snakes can breathe through their skin?",
    "Did you know that owls don’t have eyeballs but tubes?",
    "Did you know that the fingerprints of a koala are so similar to humans that they can confuse crime scenes?",
    "Did you know that humans and giraffes have the same number of neck vertebrae?",
    "Did you know that the tongue of a blue whale can weigh as much as an elephant?",
    "Did you know that penguins can jump up to 6 feet in the air?",
    "Did you know that a goldfish has a memory span of at least three months?",
    "Did you know that elephants are pregnant for almost two years?",
    "Did you know that a sneeze can travel over 100 miles per hour?",
    "Did you know that sea otters have a pouch under their arms to store food?",
    "Did you know that some frogs can change sex during their lifetime?",
    "Did you know that the platypus lays eggs despite being a mammal?",
    "Did you know that the fingerprints of a human and a chimpanzee are nearly identical?",
    "Did you know that octopuses can taste with their arms?",
    "Did you know that the average cumulus cloud weighs over a million pounds?",
    "Did you know that cats have over 20 muscles in their ears?",
    "Did you know that an ostrich’s eye is bigger than its brain?",
    "Did you know that dolphins have unique names for each other?",
    "Did you know that ants never sleep?",
    "Did you know that the first oranges were green?",
    "Did you know that crocodiles can’t stick out their tongues?",
    "Did you know that dragonflies can live for years as larvae underwater?",
    "Did you know that sharks can live up to 500 years?",
    "Did you know that honeybees can recognize human faces?",
    "Did you know that koalas have fingerprints almost indistinguishable from humans?",
    "Did you know that sloths can hold their breath longer than dolphins?",
    "Did you know that spiders can’t fly but some can travel by 'ballooning'?",
    "Did you know that seahorses are the only animals where males give birth?",
    "Did you know that the heart of a shrimp is in its head?",
    "Did you know that butterflies can taste with their feet?",
    "Did you know that a bolt of lightning contains enough energy to toast 100,000 slices of bread?",
    "Did you know that there’s a species of ant that can swim?",
    "Did you know that some turtles can breathe through their butts?",
    "Did you know that koalas sleep 22 hours a day?",
    "Did you know that a single strand of human hair can hold 100 grams?",
    "Did you know that Venus rotates clockwise?",
    "Did you know that sea stars can regrow lost arms?",
    "Did you know that wombat poop is cube-shaped?",
    "Did you know that the moon has moonquakes?",
    "Did you know that the fingerprints of a koala are almost identical to humans?",
    "Did you know that the unicorn is Scotland’s national animal?",
    "Did you know that sea lions can bark like dogs?",
    "Did you know that a group of crows is called a 'murder'?",
    "Did you know that rabbits can see behind them without turning their heads?",
    "Did you know that flamingos are naturally white and turn pink from their diet?",
    "Did you know that there are more stars in the universe than grains of sand on Earth?",
    "Did you know that humans share 60% of their DNA with bananas?",
    "Did you know that dolphins have names for each other?",
    "Did you know that the blue whale is the largest animal to ever exist?",
    "Did you know that some jellyfish are biologically immortal?",
    "Did you know that sharks existed before trees?",
    "Gumper?"
]


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
    import tkinter as tk

    # Kill old overlay if running
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, signal.SIGTERM)
        except:
            pass

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(),
                       height=root.winfo_screenheight(),
                       bg="black", highlightthickness=0)
    canvas.pack()

    x = root.winfo_screenwidth() // 2
    y = root.winfo_screenheight() // 2

    # Initial random word
    current_word = random.choice(FUN_FACTS)
    text_item = canvas.create_text(x, y, text=current_word, fill="green",
                                   font=("Comic Sans MS", 50, "bold"))

    # Write PID to file
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    def toggle_overlay():
        """Hide overlay, then show again with a new fun fact."""
        root.withdraw()  # hide overlay
        new_word = random.choice(FUN_FACTS)
        canvas.itemconfig(text_item, text=new_word)
        root.after(20000, lambda: (root.deiconify(), root.after(20000, toggle_overlay)))

    # Start the first hide/show cycle after 20 seconds
    root.after(20000, toggle_overlay)

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
