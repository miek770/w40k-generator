from configparser import ConfigParser
from pathlib import Path
from sys import exit


class Codex:

    def __init__(self, faction):
        config = ConfigParser()
        config.read(Path("codices", f"{faction}.cfg"))
        self.faction = faction
        self.units = []
        for key in config:
            if key not in ("General", "DEFAULT"):
                self.units.append({
                    "name": key,
                    "ppm": config[key].getint("ppm"),
                    "min": config[key].getint("min"),
                    "max": config[key].getint("max"),
                    "cat": config[key]["cat"],
                    "units": config[key]["units"],
                    "unique": config[key].getboolean("unique")
                })

    def unit_type(self, unit_name):
        data = self.data(unit_name)
        return data["cat"]

    def data(self, unit_name):
        """Retrieve the codex data for a given unit.
        """
        for unit in self.units:
            if unit["name"] == unit_name:
                return unit
        print(f"[Error] {unit_name} not found in codex {self.faction}.cfg")
        exit()

    def is_unique(self, unit_name):
        return self.data(unit_name)["unique"]
