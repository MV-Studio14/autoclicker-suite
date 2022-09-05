
class ClickStyle:
    def __init__(self, name="b"):
        self.delay = 0.1
        self.repeat = 15
        self.anti_cheat_time = 200
        self.anti_cheat_delay = 1
        self.vol = 0
        self.name = name

    def base(self):
        self.delay = 0.1
        self.repeat = 15
        self.anti_cheat_time = 200
        self.anti_cheat_delay = 1
        self.vol = 0

    def loadJson(self, json):
        try:
            self.delay = float(json["delay"])
            self.repeat = int(json["repeat"])
            self.anti_cheat_time = int(json["act"])
            self.anti_cheat_delay = float(json["acd"])
            self.vol = int(json["vol"])
        except:
            self.base()

    def load(self, delay, repeat, anti_cheat_time, anti_cheat_delay, volatility):
        self.delay = delay
        self.repeat = repeat
        self.anti_cheat_time = anti_cheat_time
        self.anti_cheat_delay = anti_cheat_delay
        self.vol = volatility

    def export(self):
        return {
            self.name: {
                "delay": self.delay,
                "repeat": self.repeat,
                "act": self.anti_cheat_time,
                "acd": self.anti_cheat_delay,
                "vol": self.vol,
            }}

