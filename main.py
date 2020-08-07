from army import Army
from collection import Collection
from enums import Verbose

from gooey import Gooey, GooeyParser

from configparser import ConfigParser
from os.path import exists
from sys import exit, stdin
from enum import Enum


__title__ = "W40k Generator"
__description__ = "Warhammer 40,000 Army List Generator - 9th Edition"
__version__ = "0.1.0"


@Gooey(
    program_name=__title__,
    default_size=(500, 600),
    menu=[
        {
            "name": "Help",
            "items": [
                {
                    "type": "AboutDialog",
                    "menuTitle": "About",
                    "name": __title__,
                    "description": __description__,
                    "version": __version__,
                    "copyright": "2020",
                    "website": "https://github.com/miek770/w40k-generator",
                    "developer": "Michel Lavoie",
                    "license": "MIT",
                },
            ],
        },
    ],
)
def main():
    parser = GooeyParser(description=__description__)
    parser.add_argument("config", help="Configuration file path", widget="FileChooser")
    parser.add_argument(
        "-s", "--size", default=500, type=int, help="Army size in points"
    )
    parser.add_argument(
        "-d",
        "--detachment",
        default="patrol",
        type=str,
        help="Detachment type",
        choices=["patrol",],
    )
    parser.add_argument(
        "-m", "--msu", action="store_true", help="Force minimum size units"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store",
        type=int,
        default=Verbose.Error.value,
        choices=[Verbose.Error.value, Verbose.Info.value, Verbose.Debug.value],
        help="Print more information during execution (0 = Errors only, 1 = Info, 2 = Debug",
    )
    args = parser.parse_args()

    if not exists(args.config):
        print(f"[Error] Invalid configuration file, exiting: {args.config}")
        exit()

    config = ConfigParser()
    config.read(args.config)

    army = Army(config["General"]["faction"], args.size, args.msu, args.detachment, args.verbose)
    collection = Collection(config, args.verbose)

    # First ensure we meet minimum composition requirements
    # For each unit type
    for unit_type_name in army.limits.keys():

        unit_min, unit_max = army.limits[unit_type_name]

        # If at least of unit of this type is required
        if unit_min > 0:
            if args.verbose:
                print(f"Between {unit_min} and {unit_max} {unit_type_name}", end="")
                print(f" are required in a {args.detachment} detachment.")

            # Add the minimum amount of units of this type
            for _ in range(unit_min):
                new_entry = collection.pick_unit(army, unit_type_name)
                if new_entry is not None:
                    army.list.append(new_entry)
                    if args.verbose:
                        print(
                            f" * Adding {new_entry['qty']} {new_entry['name']}", end=""
                        )
                        print(f" to the army list.")

    # Next, fill the list
    while True:
        if args.verbose:
            print(f"Current army size: {army.size} / {army.max_size}")

        # If army list is full
        if army.is_full:
            if args.verbose:
                print("Army is full.")
            break

        # If the smallest unit is bigger than the remaining points
        if collection.smallest_unit(army)[0] > army.max_size - army.size:
            if args.verbose:
                print(
                    "The smallest remaining unit is bigger than the remaining points."
                )
            break

        unit_type = collection.pick_type(army)
        if unit_type is None:
            if args.verbose:
                print("This is no valid unit type remaining.")
            break

        new_entry = collection.pick_unit(army, unit_type)
        if new_entry is not None:
            army.list.append(new_entry)
            if args.verbose:
                print(
                    f" * Adding {new_entry['qty']} {new_entry['name']} to the army list."
                )

        else:
            if args.verbose:
                print("There is no valid unit remaining.")
            break

    army.print()


if __name__ == "__main__":
    main()
