import config_necron
from codex import Codex, Factions
from composition import *
from numpy import inf
from numpy.random import choice, randint, random


class Collection:


    def __init__(self, faction):
        self.faction = faction
        self.codex = Codex(faction)
        if faction == Factions.Necron:
            self.models = config_necron.models


    def pick(self, army, unit_type=None):
        """Pick a random unit of the specified type.
        """

        if unit_type is not None and unit_type.__class__ not in (Patrol_Composition, ):
            raise TypeError(f"[Error] Invalid unit type: {unit_type}.")

        points_limit = army.max_size - (army.size + army.margin)

        if unit_type is None:
            print(f" * Choosing a unit of at most {points_limit} points...")
        else:
            print(f" * Choosing a {unit_type.name} unit of at most {points_limit} points...")

        choices = []
        for model in self.models:
            unit_data = self.codex.data(model["name"])
            #print(f" * Model data: {model}")
            #print(f" * Codex data: {unit_data}")

            # If the minimum unit size costs <= points_limit
            if unit_data["ppm"] * unit_data["min"] <= points_limit:

                # If the available quantity is >= minimum unit size
                if model["qty"] >= unit_data["min"]:

                    # If the unit type wasn't specified or if it matches the one specified
                    if unit_type is None or unit_data["cat"].name == unit_type.name:

                        # Retrieve current unit type limits if it wasn't provided
                        if unit_type is None:
                            for key in army.limits.keys():
                                if key == unit_data["cat"].name:
                                    model_type = army.limits[key]
                                    #print(f"   - {model} is type {model_type}")
                                    break
                                #else:
                                    #print(f"{key} != {unit_data['cat'].name}")
                        else:
                            model_type = unit_type

                        # If the unit type is not already maxed
                        unit_min, unit_count, unit_max = army.check(model_type)
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

        if army.msu or random() < 0.75:
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
            unit_min, unit_count, unit_max = army.check(unit_data["cat"])
            if unit_count >= unit_max:
                continue

            entry_size = unit_data["min"] * unit_data["ppm"]
            if entry_size < smallest[0]:
                smallest = (entry_size, model["name"])

        return smallest
