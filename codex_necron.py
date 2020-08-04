from unit import Unit

default = {
    "name": None,
    "ppm": 0,
    "min": 1,
    "max": 1,
    "cat": Unit.HQ,
}

#model = default.copy()
#model["name"] = ""
#model["ppm"] =
#model["cat"] = Unit.Troop
#codex.append(model)

codex = []

# HQ

model = default.copy()
model["name"] = "Catacomb Command Barge"
model["ppm"] = 150
codex.append(model)

model = default.copy()
model["name"] = "Cryptek"
model["ppm"] = 85
codex.append(model)

model = default.copy()
model["name"] = "Destroyer Lord"
model["ppm"] = 110
codex.append(model)

model = default.copy()
model["name"] = "Lord"
model["ppm"] = 70
codex.append(model)

model = default.copy()
model["name"] = "Overlord"
model["ppm"] = 90  # Indomitus
codex.append(model)

model = default.copy()
model["name"] = "Plasmancer"
model["ppm"] = 80
codex.append(model)

model = default.copy()
model["name"] = "Royal Warden"
model["ppm"] = 80
codex.append(model)

model = default.copy()
model["name"] = "Skorpekh Lord"
model["ppm"] = 130
codex.append(model)

# Troop

model = default.copy()
model["name"] = "Warrior"
model["ppm"] = 12  # Indomitus
model["min"] = 10
model["max"] = 20
model["cat"] = Unit.Troop
codex.append(model)

model = default.copy()
model["name"] = "Immortal"
model["ppm"] = 18  # CA 2020 (lequel?)
model["min"] = 5
model["max"] = 10
model["cat"] = Unit.Troop
codex.append(model)

# Elites

model = default.copy()
model["name"] = "C'tan Shard of the Deceiver"
model["ppm"] = 190
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "C'tan Shard of the Nightbringer"
model["ppm"] = 165
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "Canoptek Reanimator"
model["ppm"] = 110
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "Canoptek Tomb Stalker"
model["ppm"] = 130
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "Cryptothrall"
model["ppm"] = 20
model["min"] = 2
model["max"] = 2
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "Deathmark"
model["ppm"] = 16
model["min"] = 5
model["max"] = 10
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "Flayed One"
model["ppm"] = 14
model["min"] = 5
model["max"] = 20
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "Lychguard"
model["ppm"] = 30
model["min"] = 5
model["max"] = 10
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "Skorpekh Destroyer"
model["ppm"] = 40
model["min"] = 3
model["max"] = 3
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "Triarch Praetorian"
model["ppm"] = 23
model["min"] = 5
model["max"] = 10
model["cat"] = Unit.Elite
codex.append(model)

model = default.copy()
model["name"] = "Triarch Stalker"
model["ppm"] = 125
model["cat"] = Unit.Elite
codex.append(model)

# Fast Attack

model = default.copy()
model["name"] = "Canoptek Acanthrite"
model["ppm"] = 55
model["min"] = 3
model["max"] = 9
model["cat"] = Unit.Fast_Attack
codex.append(model)

model = default.copy()
model["name"] = "Canoptek Scarab Swarm"
model["ppm"] = 15
model["min"] = 3
model["max"] = 6
model["cat"] = Unit.Fast_Attack
codex.append(model)

model = default.copy()
model["name"] = "Canoptek Tomb Sentinel"
model["ppm"] = 150
model["cat"] = Unit.Fast_Attack
codex.append(model)

model = default.copy()
model["name"] = "Canoptek Wraith"
model["ppm"] = 45
model["min"] = 3
model["max"] = 6
model["cat"] = Unit.Fast_Attack
codex.append(model)

model = default.copy()
model["name"] = "Destroyer"
model["ppm"] = 55
model["max"] = 6
model["cat"] = Unit.Fast_Attack
codex.append(model)

model = default.copy()
model["name"] = "Tomb Blade"
model["ppm"] = 27
model["min"] = 3
model["max"] = 9
model["cat"] = Unit.Fast_Attack
codex.append(model)

# Heavy Support

model = default.copy()
model["name"] = "Annihilation Barge"
model["ppm"] = 115
model["cat"] = Unit.Heavy_Support
codex.append(model)

model = default.copy()
model["name"] = "Canoptek Spyder"
model["ppm"] = 45
model["max"] = 3
model["cat"] = Unit.Heavy_Support
codex.append(model)

model = default.copy()
model["name"] = "Doomsday Ark"
model["ppm"] = 180
model["cat"] = Unit.Heavy_Support
codex.append(model)

model = default.copy()
model["name"] = "Heavy Destroyer"
model["ppm"] = 40
model["max"] = 3
model["cat"] = Unit.Heavy_Support
codex.append(model)

model = default.copy()
model["name"] = "Monolith"
model["ppm"] = 270
model["cat"] = Unit.Heavy_Support
codex.append(model)

model = default.copy()
model["name"] = "Sentry Pylon"
model["ppm"] = 115
model["max"] = 3
model["cat"] = Unit.Heavy_Support
codex.append(model)

model = default.copy()
model["name"] = "Tesseract Ark"
model["ppm"] = 210
model["cat"] = Unit.Heavy_Support
codex.append(model)

model = default.copy()
model["name"] = "Transcendent C'tan"
model["ppm"] = 195
model["cat"] = Unit.Heavy_Support
codex.append(model)

# Flyer

model = default.copy()
model["name"] = "Doom Scythe"
model["ppm"] = 170
model["cat"] = Unit.Flyer
codex.append(model)

model = default.copy()
model["name"] = "Night Scythe"
model["ppm"] = 135
model["cat"] = Unit.Flyer
codex.append(model)

model = default.copy()
model["name"] = "Night Shroud"
model["ppm"] = 210
model["cat"] = Unit.Flyer
codex.append(model)

# Dedicated Transport

model = default.copy()
model["name"] = "Ghost Ark"
model["ppm"] = 140
model["cat"] = Unit.Dedicated_Transport
codex.append(model)
