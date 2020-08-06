from army import Army
from collection import Collection

from gooey import Gooey

from argparse import ArgumentParser
from configparser import ConfigParser
from os.path import exists
from sys import exit


@Gooey
def main():
    parser = ArgumentParser(description="Warhammer 40,000 army list generator")
    parser.add_argument("config", help="Configuration file path")
    parser.add_argument(
        "-s", "--size", default=500, type=int, help="Army size in points"
    )
    parser.add_argument(
        "-d", "--detachment", default="patrol", type=str, help="Detachment type"
    )
    parser.add_argument(
        "-m", "--msu", default=False, type=bool, help="Force minimum size units"
    )
    args = parser.parse_args()

    if not exists(args.config):
        print(f"[Error] Invalid configuration file, exiting: {args.config}")
        exit()

    config = ConfigParser()
    config.read(args.config)

    army = Army(config["General"]["faction"], args.size, args.msu, args.detachment)
    collection = Collection(config)

    # First ensure we meet minimum composition requirements
    # For each unit type
    for unit_type_name in army.limits.keys():

        unit_min, unit_max = army.limits[unit_type_name]

        # If at least of unit of this type is required
        if unit_min > 0:
            print(f"Between {unit_min} and {unit_max} {unit_type_name}", end="")
            print(f" are required in a {args.detachment} detachment.")

            # Add the minimum amount of units of this type
            for _ in range(unit_min):
                new_entry = collection.pick_unit(army, unit_type_name)
                if new_entry is not None:
                    army.list.append(new_entry)
                    print(f" * Adding {new_entry['qty']} {new_entry['name']}", end="")
                    print(f" to the army list.")

    # Next, fill the list
    while True:
        print(f"Current army size: {army.size} / {army.max_size}")

        # If army list is full
        if army.is_full:
            print("Army is full.")
            break

        # If the smallest unit is bigger than the remaining points
        if collection.smallest_unit(army)[0] > army.max_size - army.size:
            print("The smallest remaining unit is bigger than the remaining points.")
            break

        unit_type = collection.pick_type(army)
        if unit_type is None:
            print("This is no valid unit type remaining.")
            break

        new_entry = collection.pick_unit(army, unit_type)
        if new_entry is not None:
            army.list.append(new_entry)
            print(f" * Adding {new_entry['qty']} {new_entry['name']} to the army list.")

        else:
            print("There is no valid unit remaining.")
            break

    army.print()


if __name__ == "__main__":
    main()
