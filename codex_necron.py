from composition import Unit

default = {
    "name": None,
    "ppm": 0,
    "min": 1,
    "max": 1,
    "cat": Unit.HQ,
}

codex = []

overlord = default.copy()
overlord["name"] = "Overlord"
overlord["ppm"] = 90  # Indomitus
codex.append(overlord)

destroyer_lord = default.copy()
destroyer_lord["name"] = "Destroyer Lord"
destroyer_lord["ppm"] = 110
codex.append(destroyer_lord)

warrior = default.copy()
warrior["name"] = "Warrior"
warrior["ppm"] = 12  # Indomitus
warrior["min"] = 10
warrior["max"] = 20
warrior["cat"] = Unit.Troop
codex.append(warrior)

immortal = default.copy()
immortal["name"] = "Immortal"
immortal["ppm"] = 18  # CA 2020 (lequel?)
immortal["min"] = 5
immortal["max"] = 10
immortal["cat"] = Unit.Troop
codex.append(immortal)

destroyer = default.copy()
destroyer["name"] = "Destroyer"
destroyer["ppm"] = 55
destroyer["max"] = 6
destroyer["cat"] = Unit.Fast_Attack
codex.append(destroyer)