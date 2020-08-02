from numpy.random import choice, randint, random
from numpy import inf
from composition import Unit


def get_unit_data(codex, name):
    """Retrieve the codex data for a given unit.

    :param codex: Whole codex for a chosen faction.
    :type codex: List of dictionaries.
    :param name: Unit name.
    :type name: String.
    :return: Unit codex entry.
    :rtype: Dictionary.
    """
    for unit in codex:
        if unit["name"] == name:
            return unit
    else:
        return None


def pick_unit(models, points_limit, army_list, detachment=None, unit_type=None, msu=False):
    """Pick a random unit of the specified type.

    :param models: Remaining models list (player's collection).
    :type models: List of dictionaries.
    :param points_limit: Points limit for the picked unit.
    :type points_limit: Integer.
    :param unit_type: Unit type to pick, if any.
    :type unit_type: composition.Unit.
    :return: [description]
    :rtype: [type]
    """

    if unit_type is None:
        print(f" * Pickup a unit of at most {points_limit} points.")
    else:
        print(f" * Pickup a {unit_type.name} unit of at most {points_limit} points.")

    choices = []
    for entry in models:
        unit_data = get_unit_data(codex, entry["name"])
        #print(unit_data)
        #print(entry)

        # If the minimum unit size costs <= points_limit
        if unit_data["ppm"] * unit_data["min"] <= points_limit:

            # If the unit type wasn't specified or if it matches the one specified
            if unit_type is None or unit_data["cat"].name == unit_type.name:

                # If the available quantity is >= minimum unit size
                if entry["qty"] >= unit_data["min"]:

                    # Retrieve current unit type limits if it wasn't provided
                    if unit_type is None and detachment is not None:
                        for key in detachment.__members__:
                            if key == unit_data["cat"].name:
                                unit_type = detachment[key]
                                #print(f"{key} == {unit_data['cat'].name}")
                                break
                            #else:
                                #print(f"{key} != {unit_data['cat'].name}")

                    # If the unit type is not already maxed
                    unit_min, unit_count, unit_max = check_unit_type(army_list, unit_type)
                    if unit_count < unit_max:
                        choices.append(entry)

    if not len(choices):
        print(" * There is no valid choice remaining.")
        return None, models

    new_unit = choice(choices).copy()
    unit_data = get_unit_data(codex, new_unit["name"])

    if msu or random() < 0.75:
        new_unit["qty"] = unit_data["min"]
    else:
        max_size = min(
            unit_data["max"],
            int(points_limit / unit_data["ppm"]),
        )
        new_unit["qty"] = randint(unit_data["min"], max_size + 1)

    models = substract_unit(models, new_unit)
    return new_unit, models


def substract_unit(models, unit):
    """Remove the unit from the models collection (so that it isn't picked again).

    :param models: [description]
    :type models: [type]
    :param unit: [description]
    :type unit: [type]
    """
    #print(f"Removing {unit} from {models}")
    for i, entry in enumerate(models):
        if entry["name"] == unit["name"]:
            models[i]["qty"] -= unit["qty"]
            if models[i]["qty"] < 1:
                models.pop(i)
            return models


def count_army_size(army_list):
    """Count the current army size in points.

    :param army_list: [description]
    :type army_list: [type]
    """
    size = 0
    for entry in army_list:
        unit_data = get_unit_data(codex, entry["name"])
        size += entry["qty"] * unit_data["ppm"]
    return size


def count_unit_type(army_list, unit_type):
    """Counts the number of units of a type in the army list.

    :param army_list: [description]
    :type army_list: [type]
    :param unit_type: [description]
    :type unit_type: [type]
    :return: [description]
    :rtype: [type]
    """
    count = 0
    for entry in army_list:
        unit_data = get_unit_data(codex, entry["name"])
        if unit_data["cat"].name == unit_type.name:
            count += 1
    return count


def check_smallest_unit(models, codex, army_list, unit_type):
    """Find the smallest unit that can be added to the list.

    :param models: [description]
    :type models: [type]
    :param codex: [description]
    :type codex: [type]
    :return: [description]
    :rtype: [type]
    """
    smallest = (inf, None)
    for entry in models:
        unit_data = get_unit_data(codex, entry["name"])

        # Skip if there are not enough remaining models to build a unit
        if unit_data["min"] > entry["qty"]:
            continue

        # Skip if the unit type is already maxed
        unit_min, unit_count, unit_max = check_unit_type(army_list, unit_type)
        if unit_count >= unit_max:
            continue

        entry_size = unit_data["min"] * unit_data["ppm"]
        if entry_size < smallest[0]:
            smallest = (entry_size, entry["name"])

    return smallest


def print_army_list(army_list):
    print()
    for entry in army_list:
        unit_data = get_unit_data(codex, entry["name"])
        print(f"{entry['qty']} {entry['name']} ({entry['qty'] * unit_data['ppm']} pts)")
    print(f"\nTotal: {count_army_size(army_list)}")


def check_unit_type(army_list, unit_type):
    unit_count = count_unit_type(army_list, unit_type)
    unit_min = unit_type.value[0]
    unit_max = unit_type.value[1]
    return unit_min, unit_count, unit_max


# Change with CLI argument
faction = "necron"

army_list = []

# Add other factions
if faction == "necron":
    from codex_necron import codex
    from config_necron import *

# Debugging
#print(codex)
#print(models)

# First ensure we meet minimum composition requirements
# For each unit type
for unit_type in detachment.value:

    # If at least of unit of this type is required
    if unit_type.value[0] > 0:
        unit_min, unit_count, unit_max = check_unit_type(army_list, unit_type)
        print(f"Between {unit_min} and {unit_max} {unit_type.name} are required in a {detachment.name} detachment.")

        if unit_count == 0:
            print(f" * There is currently no {unit_type.name} in the army list.")
        elif unit_count == 1:
            print(f" * There is currently 1 {unit_type.name} unit in the army list.")
        else:
            print(f" * There are currently {unit_count} {unit_type.name} units in the army list.")

        # Add the minimum amount of units of this type
        for _ in range(unit_type.value[0] - unit_count):
            new_entry, models = pick_unit(
                models=models,
                points_limit=army_size - count_army_size(army_list) - margin,
                army_list=army_list,
                unit_type=unit_type,
            )
            if new_entry is not None:
                army_list.append(new_entry)
                print(f" * Adding {new_entry['qty']} {new_entry['name']} to the army list.")

# Next, fill the list
while True:
    current_army_size = count_army_size(army_list)
    print(f"Current army size: {current_army_size} / {army_size}")

    # If army list is full
    if current_army_size + margin >= army_size:
        break

    # If the smallest unit is bigger than the remaining points
    if check_smallest_unit(models, codex, army_list, unit_type)[0] > army_size - current_army_size - margin:
        break

    new_entry, models = pick_unit(
        models=models,
        points_limit=army_size - current_army_size - margin,
        army_list=army_list,
        detachment=detachment.value,
    )
    if new_entry is not None:
        army_list.append(new_entry)
        print(f" * Adding {new_entry['qty']} {new_entry['name']} to the army list.")

print_army_list(army_list)