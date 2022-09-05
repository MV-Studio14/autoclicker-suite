import os
from json import loads, dumps

from autoclick.Configuration import ClickStyle


class File:
    def __init__(self, file):
        self.file = file

    def read(self):
        while True:
            try:
                with open(self.file, "r") as f:
                    return loads(f.read())
            except:
                print("[Error] failed to load/set config file, retrying...")
                path = "\\".join(self.file.split("\\")[:-1])
                if not os.path.isdir(path):
                    os.makedirs(path)
                self.write({
                    "presets": {}
                })

    def write(self, dat):
        with open(self.file, "w") as f:
            f.write(dumps(dat))


class ConfigFile(File):
    def __init__(self):
        super().__init__(os.getenv("APPDATA") + "\\CheatStudio\\cheatclick_config.dat")
        self.dat = self.read()

    def delete(self, name):
        self.dat["presets"].pop(name)
        self.write(self.dat)

    def save(self, cs):
        self.dat["presets"].update(cs.export())
        self.write(self.dat)

    def load(self, name):
        if name == "b":
            return ClickStyle()
        elif name in self.dat["presets"]:
            cs = ClickStyle(name)
            cs.loadJson(self.dat["presets"][name])
            return cs
        return None

class PortableStyleFile(File):
    def __init__(self, file):
        super().__init__(file)
        self.dat = self.read()

    def styleImport(self):
        cs = ClickStyle(self.dat["name"])
        cs.loadJson(self.dat["content"])
        return cs

    def styleExport(self, cs):
        self.write({
            "name": cs.name,
            "content": cs.export()[cs.name]
        })