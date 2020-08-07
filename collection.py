from army import Army
from codex import *
from enums import Unit, Verbose

from random import choice, randint, random
from configparser import ConfigParser


class Collection:
    def __init__(self, config, verbose):
        self.codex = Codex(config["General"]["faction"])
        self.models = []
        self.verbose = verbose
        for key in config:
            if key not in ("General", "DEFAULT"):
                self.models.append({
                    "name": key,
                    "qty": config[key].getint("qty"),
                    "painted": config[key].getboolean("painted"),
                    "proxy": config[key].getboolean("proxy"),
                    "proxied_from": config[key]["proxied_from"],
                })

    def pick_type(self, army):
        """Pick a random valid unit type.
        """
        if army.__class__ is not Army:
            raise TypeError(f"[Error] Invalid army: {army}.")

        points_limit = army.max_size - army.size
        if self.verbose:
            print(f" * Choosing a unit type with at least 1 available", end="")
            print(f" unit of at most {points_limit} points...")

        choices = set()
        for model in self.models:
            # print(f"   - Checking {model['name']}...")
            unit_data = self.codex.data(model["name"])
            limits = None

            # If the minimum unit size costs > points_limit
            if unit_data["ppm"] * unit_data["min"] > points_limit:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {unit_data['cat']}", end="")
                    print(f" ({model['name']}), too expensive.")
                continue

            # If the available quantity is < minimum unit size
            if model["qty"] < unit_data["min"]:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {unit_data['cat']}", end="")
                    print(f" ({model['name']}), not enough model for MSU.")
                continue

            # If the unit type is already maxed
            unit_min, unit_count, unit_max = army.check(unit_data["cat"], model["name"])
            if unit_count >= unit_max:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {unit_data['cat']}", end="")
                    print(f" ({model['name']}), already maxed.")
                continue

            # If proxies are ignored and it is a proxy
            if army.no_proxy and model["proxy"]:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {unit_data['cat']}", end="")
                    print(f" ({model['name']}), is a proxy.")
                continue

            choices.add(unit_data["cat"])

        if not len(choices):
            if self.verbose:
                print(" * There is no valid unit type choice remaining.")
            return None

        return choice(list(choices))

    def pick_unit(self, army, unit_type_name):
        """Pick a random unit of the specified type.
        """
        points_limit = army.max_size - army.size
        if self.verbose:
            print(
                f" * Choosing a {unit_type_name} unit of at most {points_limit} points..."
            )

        choices = []
        for model in self.models:
            unit_data = self.codex.data(model["name"])
            # print(f" * Model data: {model}")
            # print(f" * Codex data: {unit_data}")
            # print(f" * Unit type name: {unit_type_name}")

            # If the minimum unit size costs > points_limit
            if unit_data["ppm"] * unit_data["min"] > points_limit:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model}, too expensive.")
                continue

            # If the available quantity is < minimum unit size
            if model["qty"] < unit_data["min"]:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model}, not enough model for MSU.")
                continue

            # If the unit type doesn't match the one specified
            if unit_data["cat"] != unit_type_name:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model}, wrong unit type.")
                continue

            # If proxies are ignored and it is a proxy
            if army.no_proxy and model["proxy"]:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {unit_data['cat']}", end="")
                    print(f" ({model['name']}), is a proxy.")
                continue

            # If the unit type is not already maxed
            unit_min, unit_count, unit_max = army.check(
                unit_type_name, model["name"]
            )
            if unit_count < unit_max:
                choices.append(model)
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Adding {model} to the choices.")
            else:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model}, the unit type is full.")
                pass

        if not len(choices):
            if self.verbose:
                print(" * There is no valid choice remaining.")
            return None

        new_unit = choice(choices).copy()
        unit_data = self.codex.data(new_unit["name"])

        if army.force_msu or random() < 0.50:
            new_unit["qty"] = unit_data["min"]
        else:
            max_size = min(unit_data["max"], int(points_limit / unit_data["ppm"]),)
            new_unit["qty"] = randint(unit_data["min"], max_size)

        self.remove(new_unit)
        return new_unit

    def remove(self, unit):
        """Remove the unit from the models collection (so that it isn't picked again).
        """
        # print(f"Removing {unit} from {models}")
        for i, model in enumerate(self.models):
            if model["name"] == unit["name"]:
                self.models[i]["qty"] -= unit["qty"]
                if self.models[i]["qty"] < 1:
                    self.models.pop(i)

    def smallest_unit(self, army):
        """Find the smallest unit that can be added to the list.
        """
        smallest = (9e9, None)
        for model in self.models:
            unit_data = self.codex.data(model["name"])

            # Skip if there are not enough remaining models to build a unit
            if unit_data["min"] > model["qty"]:
                continue

            # Skip if the unit type is already maxed
            unit_min, unit_count, unit_max = army.check(
                unit_data["cat"], model["name"]
            )
            if unit_count >= unit_max:
                continue

            entry_size = unit_data["min"] * unit_data["ppm"]
            if entry_size < smallest[0]:
                smallest = (entry_size, model["name"])

        return smallest
