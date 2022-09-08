import os
from time import sleep
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
from threading import Thread

# CLI config thread
from autoclick.Componets import comp_humanoid
from autoclick.Configuration import ClickStyle
from autoclick.Files import ConfigFile, PortableStyleFile


class Config(Thread):
    def __init__(self):
        super().__init__()
        self.file = ConfigFile()
        self.cs = ClickStyle()
        self.terminate = False

    def run(self):
        self.load()
        self.online()

    def stop(self):
        self.terminate = True

    def listPresets(self, phrase):
        print(phrase)
        for i in self.file.dat["presets"]:
            print(f"- {i}")
        return input("> ")

    def load(self):
        while not self.terminate:
            name = self.listPresets("Select a clickStyle or load base (b): ")
            cs = self.file.load(name)
            if cs is None:
                print("Invalid clickStyle name")
                continue
            self.cs = cs
            break

    def save(self):
        name = self.listPresets("ClickStyle name (same name overwrite): ")
        self.cs.name = name
        self.file.save(self.cs)
        print("ClickStyle saved!")

    def delete(self):
        name = self.listPresets("ClickStyle name (for DELETING!!!): ")
        self.file.delete(name)
        print("ClickStyle deleted!")

    def online(self):
        while not self.terminate:
            cps = self.cs.repeat / self.cs.delay
            evg = self.cs.anti_cheat_time / (self.cs.anti_cheat_time * self.cs.delay / self.cs.repeat + self.cs.anti_cheat_delay)

            command = input(f"{self.cs.name if self.cs.name != 'b' else '- BASE -'}: ({int(cps)}cps, {int(evg)}evg):\n" +
                           f"\t- (d) delay [{self.cs.delay}]sec\n" +
                           f"\t- (r) repeat [{self.cs.repeat}]clicks\n" +
                           f"\t- (t) anti-cheat-time [{self.cs.anti_cheat_time}]clicks\n" +
                           f"\t- (a) anti-cheat-delay [{self.cs.anti_cheat_delay}]sec\n" +
                           f"\t- (h) humanoid volatility [{self.cs.vol}]%\n\n" +
                           f"\t- (s) save clickStyle\n" +
                           f"\t- (l) load clickStyle\n" +
                           f"\t- (i) import clickStyle\n" +
                           f"\t- (e) export clickStyle\n" +
                           f"\t- (x) delete clickStyle\n> "
                           )

            params = command.split(" ")
            cmd = params[0]
            params.pop(0)

            if cmd == "s":
                self.save()
                continue
            elif cmd == "l":
                self.load()
                continue
            elif cmd == "x":
                self.delete()
                continue
            elif cmd == "e":
                self.exp()
                continue
            elif cmd == "i":
                self.imp()
                continue

            try:
                newVal = float(params[0])
            except:
                print("Enter a valid number (1234 12.34)")
                continue

            if cmd == "d":
                self.cs.delay = newVal
            elif cmd == "r":
                self.cs.repeat = int(newVal)
            elif cmd == "t":
                self.cs.anti_cheat_time = int(newVal)
            elif cmd == "a":
                self.cs.anti_cheat_delay = newVal
            elif cmd == "h":
                self.cs.vol = int(newVal)

    def imp(self):
        file = input("file> ")
        psf = PortableStyleFile(file)
        self.cs = psf.styleImport()
        print(f"ClickStyle {self.cs.name} imported!")

    def exp(self):
        psf = PortableStyleFile(os.path.expanduser("~/Desktop") + f"\\{self.cs.name}.csi")
        psf.styleExport(self.cs)


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
        global configThread
        while not self.terminate:
            while self.running:
                for i in range(configThread.cs.repeat): self.mouse.click(self.button)
                self.cont += configThread.cs.repeat
                configThread.cs = comp_humanoid(configThread.cs)
                if self.cont >= configThread.cs.anti_cheat_time:
                    self.cont = 0
                    sleep(configThread.cs.anti_cheat_delay)
                else:
                    sleep(configThread.cs.delay)

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

def main():
    global left_click, right_click, clickThread, configThread, listener

    print("Loading configs")
    configThread = Config()
    configThread.start()

    left_click = KeyCode(char="z")
    right_click = KeyCode(char="x")

    clickThread = MouseClick(Button.left, Controller())
    clickThread.start()
    with Listener(on_press=onPress) as listener: listener.join()


if __name__ == "__main__":
    main()
