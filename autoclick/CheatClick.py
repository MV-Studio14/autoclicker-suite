import os
from time import sleep
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
from threading import Thread
from zlib import compress, decompress
from json import dumps, loads
from random import uniform


# CLI config thread
class Config(Thread):
    def __init__(self, file):
        super().__init__()
        self.delay, self.repeat, self.anti_cheat_time, self.anti_cheat_delay, self.vol, self.file = 0.0, 0, 0, 0.0, 0, file
        self.terminate = False

    def run(self):
        self.load()
        self.online()

    def stop(self):
        self.terminate = True

    def base(self):
        self.delay = 0.1
        self.repeat = 15
        self.anti_cheat_time = 200
        self.anti_cheat_delay = 1
        self.vol = 0

    def readFile(self):
        while True:
            try:
                with open(self.file, "rb") as f:
                    return loads(decompress(f.read()).decode())
            except:
                print("[Error] failed to load/set config file, retrying...")
                setup()
                self.base()

    def writeFile(self, dat):
        with open(self.file, "wb") as f: f.write(compress(dumps(dat).encode()))

    def list(self, dat, phrase):
        print(phrase)
        for i in dat["presets"]: print(f"- {i}")
        return input("> ")

    def load(self):
        dat = self.readFile()
        name = self.list(dat, "Choice a preset or load base (b): ")

        while not self.terminate:
            if name == "b":
                self.base();
                break
            elif not name in dat["presets"]:
                continue
            else:
                conf = dat["presets"][name]
                self.delay = float(conf["delay"])
                self.repeat = int(conf["repeat"])
                self.anti_cheat_time = int(conf["act"])
                self.anti_cheat_delay = float(conf["acd"])
                self.vol = int(conf["vol"])
                break
            name = input("> ")

    def online(self):
        while not self.terminate:
            cps = self.repeat / self.delay
            evg = self.anti_cheat_time / (self.anti_cheat_time * self.delay / self.repeat + self.anti_cheat_delay)

            choice = input(
                f"Choice what change ({int(cps)}cps, {int(evg)}evg):\n\t- delay (d) [{self.delay}]sec\n\t- repeat (r) [{self.repeat}]click\n\t- anti-cheat-time (t) [{self.anti_cheat_time}]click\n\t- anti-cheat-delay (a) [{self.anti_cheat_delay}]sec\n\t- humanoid volatility (h) [{self.vol}]%\n\n\t- save configuration (s)\n\t- load preset (l)\n\t- delete preset (e)\n> ")
            if choice == "s":
                self.save();
                continue
            elif choice == "l":
                self.load();
                continue
            elif choice == "e":
                self.delete();
                continue

            try:
                newVal = float(input("New value is: "))
            except:
                print("Enter a valid number (1234 12.34)");
                continue

            if choice == "d":
                self.delay = newVal
            elif choice == "r":
                self.repeat = int(newVal)
            elif choice == "t":
                self.anti_cheat_time = int(newVal)
            elif choice == "a":
                self.anti_cheat_delay = newVal
            elif choice == "h":
                self.vol = int(newVal)

    def save(self):
        dat = self.readFile()
        name = self.list(dat, "Configuration name (same name overwrite): ")

        dat["presets"].update({
            name: {
                "delay": self.delay,
                "repeat": self.repeat,
                "act": self.anti_cheat_time,
                "acd": self.anti_cheat_delay,
                "vol": self.vol,
            }})

        self.writeFile(dat)
        print("Configuration saved!")

    def delete(self):
        dat = self.readFile()
        name = self.list(dat, "Configuration name (for DELETING): ")
        dat["presets"].pop(name)
        self.writeFile(dat)
        print("Configuration deleted!")


class MouseClick(Thread):
    def __init__(self, button, mouse):
        super().__init__()
        self.button = button
        self.mouse = mouse
        self.running = False
        self.cont = 0
        self.terminate = False

    def start_click(self):
        self.running = True

    def stop_click(self):
        self.running = False

    def run(self):
        while not self.terminate:
            while self.running:
                for i in range(configThread.repeat): self.mouse.click(self.button)
                self.cont += configThread.repeat
                humanoid()
                if self.cont >= configThread.anti_cheat_time:
                    self.cont = 0
                    sleep(configThread.anti_cheat_delay)
                else:
                    sleep(configThread.delay)

    def stop(self):
        self.stop_click()
        self.terminate = True


def onPress(key):
    if key == left_click:
        if clickThread.button == Button.left:
            if clickThread.running:
                clickThread.stop_click()
            else:
                clickThread.start_click()

        elif clickThread.button == Button.right:
            if clickThread.running:
                clickThread.stop_click()
                clickThread.button = Button.left
                clickThread.start_click()
            else:
                clickThread.button = Button.left
                clickThread.start_click()

    elif key == right_click:
        if clickThread.button == Button.right:
            if clickThread.running:
                clickThread.stop_click()
            else:
                clickThread.start_click()

        elif clickThread.button == Button.left:
            if clickThread.running:
                clickThread.stop_click()
                clickThread.button = Button.right
                clickThread.start_click()
            else:
                clickThread.button = Button.right
                clickThread.start_click()


# Click frequency modifier
def humanoid():
    perc = (configThread.delay * (configThread.vol / 2)) / 100
    minSample = configThread.delay - perc
    maxSample = configThread.delay + perc
    configThread.delay = uniform(minSample, maxSample)

# Make config file
def setup():
    print("Setup...")
    with open(configThread.file, "wb") as f: f.write(compress("{}".encode()))


def main():
    global left_click, right_click, clickThread, configThread, listener

    print("Loading configs")
    configThread = Config(os.getenv("%APPDATA%") + "/CheatStudio/" + "cheatclick_config.dat")
    configThread.start()

    print("Auto-click is starting...\n")
    left_click = KeyCode(char="z")
    right_click = KeyCode(char="x")

    clickThread = MouseClick(Button.left, Controller())
    clickThread.start()
    with Listener(on_press=onPress) as listener: listener.join()


if __name__ == "__main__":
    main()
