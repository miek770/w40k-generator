from numpy import inf
from codex import *
import config_necron


class Army:

    def __init__(self, faction):
        self.list = []
        self.faction = faction
        self.codex = Codex(faction)

        # !!!!!!!!!!!!!!!!!!!!!!!
        # Add other factions here
        # !!!!!!!!!!!!!!!!!!!!!!!
        if self.faction == Factions.Necron:
            self.detachment = config_necron.detachment
            self.max_size = config_necron.army_size
            self.margin = config_necron.margin
            self.msu = config_necron.msu

        # !!!!!!!!!!!!!!!!!!!!!!!!!!
        # Add other detachment types
        # !!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.detachment == Detachments.Patrol:
            self.limits = Patrol_Composition


    @property
    def size(self):
        """Count the current army size in points.

        :param army_list: [description]
        :type army_list: [type]
        """
        size = 0
        for entry in self.list:
            unit_data = self.codex.data(entry["name"])
            size += entry["qty"] * unit_data["ppm"]
        return size


    @property
    def is_full(self):
        if self.size + self.margin >= self.max_size:
            return True
        else:
            return False


    def count(self, unit_type_name):
        """Counts the number of units of a type in the army list.

        :param army_list: [description]
        :type army_list: [type]
        :param unit_type: [description]
        :type unit_type: [type]
        :return: [description]
        :rtype: [type]
        """
        count = 0
        for entry in self.list:
            unit_data = self.codex.data(entry["name"])
            if unit_data["cat"].name == unit_type_name:
                count += 1
        return count


    def check(self, unit_type_name):
        unit_count = self.count(unit_type_name)
        unit_min, unit_max = self.limits[unit_type_name]
        return unit_min, unit_count, unit_max


    @property
    def unit_types(self):
        types = set()
        for entry in self.list:
            types.add(self.codex.unit_type(entry["name"]))
        types = list(types)
        types.sort()
        return types


    def print(self):
        print()

        for unit_type in self.unit_types:
            print(f"{unit_type}:")
            for entry in self.list:
                entry_type = self.codex.unit_type(entry["name"])
                if entry_type == unit_type:
                    unit_data = self.codex.data(entry["name"])
                    print(f" - {entry['qty']} {entry['name']} ({entry['qty'] * unit_data['ppm']} pts)")
        print(f"\nTotal: {self.size}")
