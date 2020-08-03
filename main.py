from composition import Unit
from codex import Codex
from army import Army
from collection import Collection


# Change with CLI argument
from config_necron import *

codex = Codex(faction)
army = Army(faction)
collection = Collection(faction)

# Debugging
#print(codex)
#print(models)

# First ensure we meet minimum composition requirements
# For each unit type
for unit_type_name in army.limits.keys():

    unit_min, unit_max = army.limits[unit_type_name].value

    # If at least of unit of this type is required
    if unit_min > 0:
        print(f"Between {unit_min} and {unit_max} {unit_type_name} are required in a {army.detachment.name} detachment.")

        # Add the minimum amount of units of this type
        for _ in range(unit_min):
            new_entry = collection.pick(army, army.limits[unit_type_name])
            if new_entry is not None:
                army.list.append(new_entry)
                print(f" * Adding {new_entry['qty']} {new_entry['name']} to the army list.")

# Next, fill the list
while True:
    print(f"Current army size: {army.size} / {army.max_size}")

    # If army list is full
    if army.is_full:
        break

    # If the smallest unit is bigger than the remaining points
    if collection.smallest_unit(army)[0] > army.max_size - (army.size + army.margin):
        break

    new_entry = collection.pick(army)
    if new_entry is not None:
        army.list.append(new_entry)
        print(f" * Adding {new_entry['qty']} {new_entry['name']} to the army list.")

    else:
        break

army.print()