from enum import Enum
import codex_necron


class Factions(Enum):
    Necron = 0

class Codex:


    def __init__(self, faction):
        self.faction = faction

        # Add other factions here
        if faction == Factions.Necron:
            self.units = codex_necron.codex


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
