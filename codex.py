from enum import Enum
from configparser import ConfigParser
from pathlib import Path


Patrol_Composition = {
    "HQ": (1, 2),
    "Troop": (1, 3),
    "Elite": (0, 2),
    "Fast_Attack": (0, 2),
    "Heavy_Support": (0, 2),
    "Flyer": (0, 2),
    "Dedicated_Transport": (0, 9e9),
    "Lord_of_War": (0, 0),
    "Fortification": (0, 0),
    "Other": (0, 9e9),
}


class Codex:

    def __init__(self, faction):
        config = ConfigParser()
        config.read(Path("codices", f"{faction}.cfg"))
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
        else:
            return None
