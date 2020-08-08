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
            unit_data = self.codex.data(model["name"])
            limits = None

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

            # If the minimum unit size costs > points_limit
            if unit_data["ppm"] * unit_data["min"] > points_limit:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {unit_data['cat']}", end="")
                    print(f" ({model['name']}), too expensive.")
                continue

            # If the available quantity is < minimum unit size
            if self.qty(model["name"]) < unit_data["min"]:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {unit_data['cat']}", end="")
                    print(f" ({model['name']}), not enough model for MSU.")
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

            # If the unit type doesn't match the one specified
            if unit_data["cat"] != unit_type_name:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model['name']}, wrong unit type.")
                continue

            # If the unit type is not already maxed
            unit_min, unit_count, unit_max = army.check(unit_type_name, model["name"])
            if unit_count >= unit_max:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model['name']}, the unit type is full.")
                continue

            # If proxies are ignored and it is a proxy
            if army.no_proxy and model["proxy"]:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {unit_data['cat']}", end="")
                    print(f" ({model['name']}), is a proxy.")
                continue

            # If the minimum unit size costs > points_limit
            if unit_data["ppm"] * unit_data["min"] > points_limit:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model['name']}, too expensive.")
                continue

            # If the available quantity is < minimum unit size
            if self.qty(model["name"]) < unit_data["min"]:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model['name']}, not enough model for MSU.")
                continue

            # All good, adding
            choices.append(model)
            if self.verbose >= Verbose.Debug.value:
                print(f"   - Adding {model} to the choices.")

        if not len(choices):
            if self.verbose:
                print(" * There is no valid choice remaining.")
            return None

        new_unit = choice(choices).copy()

        if self.verbose >= Verbose.Debug.value:
            print(f" * Chose {new_unit['name']}")

        unit_data = self.codex.data(new_unit["name"])

        if army.force_msu or random() < 0.50:
            new_unit["qty"] = unit_data["min"]
        else:
            max_size = min(
                self.qty(new_unit["name"]),
                unit_data["max"],
                int(points_limit / unit_data["ppm"]),
                )
            new_unit["qty"] = randint(unit_data["min"], max_size)

        self.remove(new_unit)
        return new_unit

    def qty(self, model_name):
        """Return the number of remaining models of a given name. For proxies, check
        for the proxy source quantities and update the proxy's model count accordingly.
        """
        for i, model in enumerate(self.models):
            if model["name"] == model_name:
                if self.verbose >= Verbose.Debug.value:
                    print(f" * Checking quantity for {model_name}")

                # If this model is proxied from another model
                if model["proxied_from"] != "":
                    qty = 0
                    for proxy in model["proxied_from"].split(","):
                        if self.verbose >= Verbose.Debug.value:
                            print(f"   - {model_name} is proxied from {proxy.strip()}")
                        qty += self.qty(proxy.strip())
                    self.models[i]["qty"] = qty

                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Remaining {model_name}: {self.models[i]['qty']}")
                return self.models[i]["qty"]

        # Return None if there is no matching model
        return None

    def remove(self, unit):
        """Remove the unit from the models collection (so that it isn't picked again).
        """
        for i, model in enumerate(self.models):
            if model["name"] == unit["name"]:

                # If this model is proxied from another model
                if model["proxied_from"] != "":
                    qty = unit["qty"]
                    for proxy in model["proxied_from"].split(","):

                        removed = min(qty, self.qty(proxy.strip()))
                        if removed < 1:
                            break

                        self.remove({"name": proxy, "qty": removed})
                        qty -= removed
                        if qty < 1:
                            break

                elif self.verbose >= Verbose.Info.value:
                    print(f" * Removing {unit['qty']} {unit['name']}")

                self.models[i]["qty"] -= unit["qty"]
                break

    def smallest_unit(self, army):
        """Find the smallest unit that can be added to the list.
        """
        if self.verbose >= Verbose.Debug.value:
            print(" * Looking for the smallest remaining unit in the collection")

        smallest = (9e9, None)
        for model in self.models:
            unit_data = self.codex.data(model["name"])

            # Skip if the unit type is already maxed
            unit_min, unit_count, unit_max = army.check(unit_data["cat"], model["name"])
            if unit_count >= unit_max:
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model['name']} - Unit type", end="")
                    print(f" already maxed: {unit_count} / {unit_max}")
                continue

            # Skip if there are not enough remaining models to build a unit
            if unit_data["min"] > self.qty(model["name"]):
                if self.verbose >= Verbose.Debug.value:
                    print(f"   - Skipping {model['name']}, not enough remaining models")
                continue

            # All good
            entry_size = unit_data["min"] * unit_data["ppm"]
            if entry_size < smallest[0]:
                smallest = (entry_size, model["name"])

        return smallest
