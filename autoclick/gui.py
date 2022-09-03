import sys
import tkinter as tk
from threading import Thread
import pystray
from PIL import Image

class Window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("720x480")
        self.window.title("Click Studio")
        self.window.resizable(False, False)
        self.bg = "#04040A"
        self.window.config(background=self.bg)

    def build(self):
        l = tk.Label(self.window, text="Click Studio", fg="aqua", bg=self.bg, font=("Currier New", 20))
        l.pack(pady=10)

        # btn = tk.Button(text="text", command=function)
        # btn.grid(row=0, column=0)

    def show(self): self.window.mainloop()

class MenuIcon(Thread):
    def __init__(self):
        super().__init__(name="CheatClick icon")
        self.image = Image.open("../icons/icon.png")
        self.icon = pystray.Icon("CheatClick", self.image, menu=pystray.Menu(
            pystray.MenuItem("Exit", menuExit)
        ))

    def run(self):
        self.icon.run()

    def stop(self): self.icon.stop()

def menuExit():
    global menuIcon
    menuIcon.stop()
    sys.exit()

def main():
    global menuIcon, window

    window = Window()
    window.build()

    menuIcon = MenuIcon()
    menuIcon.start()

    window.show()
    quit()


if __name__ == "__main__":
    main()