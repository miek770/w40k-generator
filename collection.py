import config_necron
from army import Army
from codex import *
from unit import Unit
from numpy import inf
from numpy.random import choice, randint, random


class Collection:


    def __init__(self, faction):
        self.faction = faction
        self.codex = Codex(faction)
        if faction == Factions.Necron:
            self.models = config_necron.models


    def pick_type(self, army):
        """Pick a random valid unit type.
        """
        if army.__class__ is not Army:
            raise TypeError(f"[Error] Invalid army: {army}.")

        points_limit = army.max_size - (army.size + army.margin)
        print(f" * Choosing a unit type with at least 1 available unit of at most {points_limit} points...")

        choices = set()
        for model in self.models:
            print(f"   - Checking {model['name']}...")
            unit_data = self.codex.data(model["name"])
            limits = None

            # If the minimum unit size costs <= points_limit
            if unit_data["ppm"] * unit_data["min"] <= points_limit:

                # If the available quantity is >= minimum unit size
                if model["qty"] >= unit_data["min"]:

                    # If the unit type is not already maxed
                    unit_min, unit_count, unit_max = army.check(unit_data["cat"].name)
                    if unit_count < unit_max:
                        choices.add(unit_data["cat"])

                    else:
                        print(f"   - Skipping {unit_data['cat'].name} ({model['name']}), already maxed.")
                        pass
                else:
                    print(f"   - Skipping {unit_data['cat'].name} ({model['name']}), not enough model for MSU.")
                    pass
            else:
                print(f"   - Skipping {unit_data['cat'].name} ({model['name']}), too expensive.")
                pass

        if not len(choices):
            print(" * There is no valid unit type choice remaining.")
            return None

        return choice(list(choices))


    def pick_unit(self, army, unit_type_name):
        """Pick a random unit of the specified type.
        """
        points_limit = army.max_size - (army.size + army.margin)
        print(f" * Choosing a {unit_type_name} unit of at most {points_limit} points...")

        choices = []
        for model in self.models:
            unit_data = self.codex.data(model["name"])
            #print(f" * Model data: {model}")
            #print(f" * Codex data: {unit_data}")

            # If the minimum unit size costs <= points_limit
            if unit_data["ppm"] * unit_data["min"] <= points_limit:

                # If the available quantity is >= minimum unit size
                if model["qty"] >= unit_data["min"]:

                    # If the unit type matches the one specified
                    if unit_data["cat"].name == unit_type_name:

                        # If the unit type is not already maxed
                        unit_min, unit_count, unit_max = army.check(unit_type_name)
                        if unit_count < unit_max:
                            choices.append(model)
                            #print(f"   - Adding {model} to the choices.")

                    else:
                        #print(f"   - Skipping {model}, wrong unit type.")
                        pass
                else:
                    #print(f"   - Skipping {model}, not enough model for MSU.")
                    pass
            else:
                #print(f"   - Skipping {model}, too expensive.")
                pass

        if not len(choices):
            print(" * There is no valid choice remaining.")
            return None

        new_unit = choice(choices).copy()
        unit_data = self.codex.data(new_unit["name"])

        if army.msu or random() < 0.50:
            new_unit["qty"] = unit_data["min"]
        else:
            max_size = min(
                unit_data["max"],
                int(points_limit / unit_data["ppm"]),
            )
            new_unit["qty"] = randint(unit_data["min"], max_size + 1)

        self.remove(new_unit)
        return new_unit


    def remove(self, unit):
        """Remove the unit from the models collection (so that it isn't picked again).
        """
        #print(f"Removing {unit} from {models}")
        for i, model in enumerate(self.models):
            if model["name"] == unit["name"]:
                self.models[i]["qty"] -= unit["qty"]
                if self.models[i]["qty"] < 1:
                    self.models.pop(i)


    def smallest_unit(self, army):
        """Find the smallest unit that can be added to the list.
        """
        smallest = (inf, None)
        for model in self.models:
            unit_data = self.codex.data(model["name"])

            # Skip if there are not enough remaining models to build a unit
            if unit_data["min"] > model["qty"]:
                continue

            # Skip if the unit type is already maxed
            unit_min, unit_count, unit_max = army.check(unit_data["cat"].name)
            if unit_count >= unit_max:
                continue

            entry_size = unit_data["min"] * unit_data["ppm"]
            if entry_size < smallest[0]:
                smallest = (entry_size, model["name"])

        return smallest
