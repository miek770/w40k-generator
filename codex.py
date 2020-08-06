from enum import Enum
from importlib import import_module


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
        # !!!!!!!!!!!!!!!!!!
        # Add other factions
        # !!!!!!!!!!!!!!!!!!
        if faction == "necron":
            i = import_module("codices.necron")
            self.units = i.codex

    def unit_type(self, unit_name):
        data = self.data(unit_name)
        return data["cat"].name

    def data(self, unit_name):
        """Retrieve the codex data for a given unit.

        :param codex: Whole codex for a chosen faction.
        :type codex: List of dictionaries.
        :param name: Unit name.
        :type name: String.
        :return: Unit codex entry.
        :rtype: Dictionary.
        """
        for unit in self.units:
            if unit["name"] == unit_name:
                return unit
        else:
            return None
