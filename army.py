from composition import *
from numpy import inf
from codex import Codex, Factions
import config_necron


class Army:


    def __init__(self, faction):
        self.list = []
        self.faction = faction
        self.codex = Codex(faction)

        # Add other factions here
        if self.faction == Factions.Necron:
            self.detachment = config_necron.detachment
            self.max_size = config_necron.army_size
            self.margin = config_necron.margin
            self.msu = config_necron.msu

        # Add other detachment types
        if self.detachment == Detachments.Patrol:
            self.limits = {
                "HQ": Patrol_Composition.HQ,
                "Troop": Patrol_Composition.Troop,
                "Elite": Patrol_Composition.Elite,
                "Fast_Attack": Patrol_Composition.Fast_Attack,
                "Heavy_Support": Patrol_Composition.Heavy_Support,
                "Flyer": Patrol_Composition.Flyer,
            }


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


    def count(self, unit_type):
        """Counts the number of units of a type in the army list.

        :param army_list: [description]
        :type army_list: [type]
        :param unit_type: [description]
        :type unit_type: [type]
        :return: [description]
        :rtype: [type]
        """
        if unit_type.__class__ not in (Patrol_Composition, ):
            raise TypeError(f"[Error] Invalid unit type: {unit_type}.")

        count = 0
        for entry in self.list:
            unit_data = self.codex.data(entry["name"])
            if unit_data["cat"].name == unit_type.name:
                count += 1
        return count


    def check(self, unit_type):
        if unit_type.__class__ in (Patrol_Composition, ):
            unit_type_composition = unit_type
        elif unit_type.__class__ == Unit:
            try:
                unit_type_composition = self.limits[unit_type.name]
            except KeyError:
                # This is a dirty hack, but basically any unit not defined in
                # the detachment's limits is considered as having no limit,
                # the reason being that their limits are more complex
                # (ex.: dedicated transports for certain troop types).
                return 0, 0, inf
        else:
            raise TypeError(f"[Error] Invalid unit type: {unit_type}.")

        unit_count = self.count(unit_type_composition)
        unit_min = unit_type_composition.value[0]
        unit_max = unit_type_composition.value[1]
        return unit_min, unit_count, unit_max


    def print(self):
        print()
        for entry in self.list:
            unit_data = self.codex.data(entry["name"])
            print(f"{entry['qty']} {entry['name']} ({entry['qty'] * unit_data['ppm']} pts)")
        print(f"\nTotal: {self.size}")
